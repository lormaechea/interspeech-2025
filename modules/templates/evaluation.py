#!/usr/bin/env python

REFINE = """
# Context:
In a previous iteration, you generated a simplification that was suboptimal.

# Instructions:
Your task is to refine the given synthetic simplification according to the feedback that is provided below.

Here is the original sentence and the previously generated simplification:
Original sentence: {sentence}
Previous simplification: {simplification}

And here's the feedback to enhance the simplification:
{feedback}

Correct the previously generated simplification according to the feedback above.

"""

SIMP_PROMPT = """
# Context:
You are an evaluator scoring the simplicity gain of a given sentence with respect to a reference.

# Instructions:
Your task is to provide a 'simplicity score' rating how much simpler is the following simplification with respect to its corresponding reference. Use a scale from 1 to 3, 1 being the worst and 3 being the best.

Here is the scale you should use to build your answer:
A score of 3 means that the proposed simplification is indeed simpler than the original reference.
A score of 2 means that the proposed simplification has the same level of complexity than the original reference.
A score of 1 means that the proposed simplification is more complex than the original reference.

Provide a score and the reasoning for your score as follows:
- After "score: ", provide your score, as an integer between 1 and 3.
- After "explanation: ", provide the reasoning for your score.

Now here are the reference and simplification:
Reference: {reference}
Simplification: {simplification}

# Output format:
Return json format with the following JSON schema: 
{{
        "explanation": {{
            "type": "string"
        }},
        "score": {{
            "type": "integer",
            "enum": [1, 2, 3]
        }}
}}
"""

MEAN_PROMPT = """
# Context:
You are an evaluator scoring the meaning preservation of a given sentence with respect to a reference.

# Instructions:
Your task is to provide a 'meaning score' rating how well the following simplification retains the meaning of the corresponding reference. Use a scale from 1 to 3, 1 being the worst and 3 being the best.

Here is the scale you should use to build your answer:
A score of 3 means that the information of the proposed simplification is mostly preserved from the original reference.
A score of 2 means that the information of the proposed simplification is partially preserved from the original reference.
A score of 1 means that the information of the proposed simplification is different from the original reference.

Provide a score and the reasoning for your score as follows:
- After "score: ", provide your score, as an integer between 1 and 3.
- After "explanation: ", provide the reasoning for your score.

Now here are the reference and simplification:
Reference: {reference}
Simplification: {simplification}

# Output format:
Return json format with the following JSON schema: 
{{
        "explanation": {{
            "type": "string"
        }},
        "score": {{
            "type": "integer",
            "enum": [1, 2, 3]
        }}
}}
"""

GRAM_PROMPT = """
# Context:
You are an evaluator rating the grammaticality of a given sentence.

# Instructions:
Your task is to provide a 'grammaticality score' rating the grammatical correctness of a sentence. Use a binary value of 0 and 1.

Here is the scale you should use to build your answer:
A score of 0 means that the proposed sentence is grammatical and conforms to the syntactic and morphological norms of French.
A score of 1 means that the proposed sentence is not grammatical because it does not conform to the syntactic and morphological norms of French.

Provide a score and the reasoning for your score as follows:
- After "score: ", provide your score, as an integer between 0 and 1.
- After "explanation: ", provide the reasoning for your score.

Now here is the sentence:
Sentence: {simplification}

# Output format:
Return json format with the following JSON schema: 
{{
        "explanation": {{
            "type": "string"
        }},
        "score": {{
            "type": "integer",
            "enum": [0, 1]
        }}
}}
"""
