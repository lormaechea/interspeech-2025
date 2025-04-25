#!/usr/bin/env python

import re, json
import pandas as pd
from mistralai import UserMessage
from modules.templates.evaluation import *
from modules.templates.topeval import *

params = {
	'gen': {
		'temperature': 0.2,
		'max_new_tokens': 256,
		'top_p': 0.9,
	},
	'eval': {
		'temperature': 0.2,
		'max_new_tokens': 256,
		'top_p': 0.9,
	}
}

# -------------------------------------------------------------

def process_simplifications(gen_client, eval_client, sentence_id, sentence, prompt_id, prompt, history, gen_model, eval_model):
	limit = 11
	results = [] 
	simplification = None

	print(f">>> TEMPLATE ID {prompt_id}")
	# print(f">>> TEMPLATE {prompt}")

	for iteration in range(1, 6):
		print(f">>> ITERATION {iteration}")

		history = history[-limit:] if len(history) > limit else history

		# Insert the new message at the top of the list
		system_prompt = {"role": "system", "content": prompt}

		# Add the system prompt if not already present
		if not history or history[0] != system_prompt:
			history.insert(0, system_prompt)

		print(f"HISTORY LENGTH: {len(history)}")

		try:
			if iteration == 1:
				simplification, history = run_gen_mistral(gen_client, sentence, history, gen_model)
			
			else:
				feedback = final_score["top"]["reasoning"]
				feedback += "\n".join(reasoning)
				
				print("----------------")
				# print(gen_client)
				# print(sentence)
				# print(simplification)
				# print(feedback)
				# print(history)
				
				simplification, history = run_feedback_mistral(gen_client, sentence, simplification, feedback, history, gen_model)

			print(f"Simplification: {simplification}")
			
			scores = run_eval_mistral(eval_client, sentence, simplification, eval_model)
			print(f"Evaluation {iteration}: {scores}")

			reasoning = []
			
			if scores["simp"]["score"] <= 2.0 and scores["simp"]["score"] != -1.0:
				reasoning.append(scores["simp"]["reasoning"])

			if scores["mean"]["score"] <= 2.0 and scores["mean"]["score"] != -1.0:
				reasoning.append(scores["mean"]["reasoning"])
				
			if scores["gram"]["score"] == 1.0 and scores["gram"]["score"] != -1.0:
				reasoning.append(scores["gram"]["reasoning"])

			# -------------------------------------------------

			if None in [scores["simp"]["score"], scores["mean"]["score"], scores["gram"]["score"]]:
				print("!!!!!! Candidate simplification is DISCARDED")
				return results, history  # Simplification discarded, return the results

			else:
				final_score = run_topeval_mistral(eval_client, sentence, simplification, eval_model, 
					scores["simp"]["reasoning"], scores["mean"]["reasoning"], scores["gram"]["reasoning"],
					scores["simp"]["score"], scores["mean"]["score"], scores["gram"]["score"]
				)

				results.append({
					'sentence_id': sentence_id,
					'sentence': sentence,
					'iteration': iteration,
					'simplification': simplification,
					'gram_score': scores["gram"]["score"],
					'simp_score': scores["simp"]["score"],
					'mean_score': scores["mean"]["score"],
					'gram_reasoning': scores["gram"]["reasoning"],
					'simp_reasoning': scores["simp"]["reasoning"],
					'mean_reasoning': scores["mean"]["reasoning"],
					'prompt_id': prompt_id,
					'top_score': final_score["top"]["score"],
					'top_reasoning': final_score["top"]["reasoning"]
				})

				if final_score["top"]["score"] == 0:
					print("!!!!!! Candidate simplification is OPTIMAL")
					return results, history  # Simplification is optimal, return the results

				elif final_score["top"]["score"] == 1:
					print("!!!!!! Candidate simplification can be IMPROVED")

				else:
					print("!!!!!! Check top evaluator score for debugging: " + final_score["top"]["score"])
				# -------------------------------------------------
		
		except Exception as e:
			print(f"Exception: {e}")
			return results, history # Discard simplification if any error occurs

	return results, history # Return the results after 5 iterations

# -------------------------------------------------------------

def save_dataframe_per_conversation(conversation_results, file_path, prompt_id):
	df = pd.DataFrame(conversation_results)
	csv_file_path = f"{file_path}-{prompt_id}.tsv"
	df.to_csv(csv_file_path, 
		index=False, 
		encoding="utf-8",
		sep="\t"
	)
	print(f"### Output file saved to: {csv_file_path}")

# -------------------------------------------------------------

def extract_judge_score(result):
	pattern = r'\{.*?\}'
	match = re.search(pattern, result, re.DOTALL)
	if match:
		json_text = match.group()
		try:
			data = json.loads(json_text)
			return data["score"], data["explanation"]

		except Exception as e:
			print(f"Exception: {e}")
			return None, None

# -------------------------------------------------------------

def extract_gen_sentence(result):
	print("----")
	print(result)
	# Find the JSON block manually
	start = result.find('{')
	end = result.rfind('}') + 1
	if start != -1 and end != -1:
		json_text = result[start:end]
		try:
			data = json.loads(json_text)
			if isinstance(data["simplification"], dict) and "value" in data["simplification"]:
				return data["simplification"]["value"]
			elif isinstance(data["simplification"], dict) and "content" in data["simplification"]:
				return data["simplification"]["content"]
			elif isinstance(data["simplification"], dict) and "type" in data["simplification"]:
				return data["simplification"]["type"]
			else:
				return data["simplification"]
		except json.JSONDecodeError as e:
			print(f"JSON decoding error: {e}")
			return None
		
# -------------------------------------------------------------

def run_feedback_mistral(client, sentence, simplification, feedback, history, model):
	prompt = REFINE.format(sentence=sentence, simplification=simplification, feedback=feedback)
	history.append({"role": "user", "content": prompt}) # Append the current user prompt to the history

	# print(">>> History (feedback)")
	# print(history)
	# print("<<< History")

	response = client.chat.complete(
		model=model, 
		messages=history, # Pass the conversation history, including system/user/assistant messages
		temperature=params["gen"]["temperature"],
		max_tokens=params["gen"]["max_new_tokens"], 
		top_p=params["gen"]["top_p"],  
		# repetition_penalty=params["gen"]["rep_penalty"],
		response_format={"type": "json_object"}
	)

	# Append the assistant's response to the history
	assistant_response = response.choices[0].message.content
	history.append({"role": "assistant", "content": assistant_response})

	print("REFINE: " + assistant_response)

	# Extract the generated sentence
	simplification = extract_gen_sentence(assistant_response)

	return simplification, history

# -------------------------------------------------------------

def run_gen_mistral(client, sentence, history, model):
	user_prompt = """

Here is the sentence to be simplified:
Sentence: {sentence}

# Output format:
Return json format with the following JSON schema: 
{{
	"simplification": {{
		"type": "string"
	}}
}}
"""

	formatted_prompt = user_prompt.format(sentence=sentence)
	history.append({"role": "user", "content": formatted_prompt}) # Append the current user prompt to the history

	# print(">>> History (gen)")
	# print(history)
	# print("<<< History")

	response = client.chat.complete(
		model=model,  
		messages=history, # Pass the conversation history, including system/user/assistant messages
		temperature=params["gen"]["temperature"],
		max_tokens=params["gen"]["max_new_tokens"], 
		top_p=params["gen"]["top_p"],  
		#presence_penalty=params["gen"]["rep_penalty"],
		response_format={"type": "json_object"}
	)

	assistant_response = response.choices[0].message.content

	history.append({"role": "assistant", "content": assistant_response}) # Append the assistant's response to the history

	print("GEN: " + assistant_response)

	# Extract the generated sentence
	simplification = extract_gen_sentence(assistant_response)

	return simplification, history

# -------------------------------------------------------------

def run_eval_mistral(client, sentence, simplification, model):
	prompt = SIMP_PROMPT.format(reference=sentence, simplification=simplification)
	simp_response = client.chat.complete(
		model=model,
		messages=[
			{"role": "user", "content": prompt}
		],
		temperature=params["eval"]["temperature"],
		max_tokens=params["eval"]["max_new_tokens"],
		top_p=params["eval"]["top_p"], 
		# repetition_penalty=params["eval"]["rep_penalty"],
		response_format={"type": "json_object"}
	)

	simp_score, simp_reasoning = extract_judge_score(simp_response.choices[0].message.content)

	prompt = MEAN_PROMPT.format(reference=sentence, simplification=simplification)
	mean_response = client.chat.complete(
		model=model,
		messages=[
			{"role": "user", "content": prompt}
		],
		temperature=params["eval"]["temperature"],
		max_tokens=params["eval"]["max_new_tokens"], 
		top_p=params["eval"]["top_p"],  
		# repetition_penalty=params["eval"]["rep_penalty"],
		response_format={"type": "json_object"}
	)

	mean_score, mean_reasoning = extract_judge_score(mean_response.choices[0].message.content)
	
	prompt = GRAM_PROMPT.format(simplification=simplification)
	gram_response = client.chat.complete(
		model=model,
		messages=[
			{"role": "user", "content": prompt}
		],
		temperature=params["eval"]["temperature"],
		max_tokens=params["eval"]["max_new_tokens"], 
		top_p=params["eval"]["top_p"],  
		# repetition_penalty=params["eval"]["rep_penalty"],
		response_format={"type": "json_object"}
	)

	gram_score, gram_reasoning = extract_judge_score(gram_response.choices[0].message.content)

	print(f"\nSIMP:\n{simp_response.choices[0].message.content}\nMEAN:\n{mean_response.choices[0].message.content}\nGRAM:\n{gram_response.choices[0].message.content}\n")

	scores = {
	"simp": {
		"score": float(simp_score) if simp_score is not None else -1.0,
		"reasoning": simp_reasoning},
	"mean": {
		"score": float(mean_score) if mean_score is not None else -1.0,
		"reasoning": mean_reasoning},
	"gram": {
		"score": float(gram_score) if gram_score is not None else -1.0,
		"reasoning": gram_reasoning}
	}

	return scores

# -------------------------------------------------------------

def run_topeval_mistral(client, sentence, simplification, model, s, m, g, s_score, m_score, g_score):

	prompt = TOP_EVAL_USR.format(
		reference=sentence, 
		simplification=simplification,
		s=s, m=m, g=g,
		s_score=s_score,
		m_score=m_score,
		g_score=g_score
	)

	# print("TOP_EVAL: "+ prompt)
	
	response = client.chat.complete(	
		model=model,
		messages=[
			{"role": "system", "content": TOP_EVAL_SYS},
			{"role": "user", "content": prompt}
		],
		temperature=params["eval"]["temperature"],
		max_tokens=params["eval"]["max_new_tokens"],
		top_p=params["eval"]["top_p"], 
		# repetition_penalty=params["eval"]["rep_penalty"],
		response_format={"type": "json_object"}
	)

	final_score, final_reasoning = extract_judge_score(response.choices[0].message.content)

	score = {
	"top": {
		"score": float(final_score) if final_score is not None else -1.0,
		"reasoning": final_reasoning}
	}

	return score
