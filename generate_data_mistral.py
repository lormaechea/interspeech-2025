#!/usr/bin/env python

import re, json, glob
import sys, os, time
from modules.functions_mistral import *
from modules.templates.generation import *
from collections import defaultdict
from mistralai import Mistral

# ------------------------------------------

def main():
	# gen_models = ["open-mistral-7b", "open-mistral-nemo-2407", "mistral-small-2409", "mistral-large-2407"]
	
	gen_model = "open-mistral-7b"
	eval_model = "open-mixtral-8x7b"

	with open(".key", "r") as file: # Add Mistral key 
		api_key = file.read().strip()
	
	gen_client, eval_client = Mistral(api_key=api_key), Mistral(api_key=api_key)

	inFiles = glob.glob("data/orfeo/conversations/*/*")
	folder_dict = defaultdict(list)

	for path in inFiles:
		folder = os.path.dirname(path)
		folder_dict[folder].append(path)

	for folder, files in folder_dict.items():
		for file in files:
			print(f">>> FILE: {file}")

			outFile = file.replace("data/orfeo/conversations", f"results/{gen_model}_{eval_model}")
			os.makedirs(os.path.dirname(outFile), exist_ok=True)

			for template in gen_templates:
				for prompt_id, prompt in template.items():
					# Check if the output file already exists:
					if os.path.exists(f"{outFile}-{prompt_id}.tsv"):
						print(f"Skipping {outFile}-{prompt_id}.tsv, already processed.")
						continue

					print(f"PROMPT STRATEGY --> {prompt_id}")
 
					with open(file, "r", encoding="utf-8") as f:
						# We reset the history to [] every new conversation:
						history = []

						# We reinitialize the results list:
						conversation_results = []
						
						# Total time tracker (per conversation):
						total_time = 0
						
						for line in f:
							line = line.strip()
							sentence_id, sentence = line.split("\t", 1)

							if re.search(r"suites? de syllabes", sentence):
								print(f"WE DO NOT PROCEED TO SIMPLIFICATION: {line}")
								continue

							else:
								print(f"LINE : {line}")
								start_time = time.time()

								results, history = process_simplifications(gen_client, eval_client, sentence_id, sentence, prompt_id, prompt, history, gen_model, eval_model)
								conversation_results.extend(results)

								end_time = time.time()

								elapsed_time = end_time - start_time
								total_time += elapsed_time
								print(f"Time taken for this sentence: {elapsed_time:.2f} seconds")

						save_dataframe_per_conversation(conversation_results, outFile, prompt_id)

						print(f"Time taken for this conversation: {total_time:.2f} seconds")
						print("------------------")

if __name__ == '__main__':
	main()
