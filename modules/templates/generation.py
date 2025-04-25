#!/usr/bin/env python

gen_templates = [
{"zero-shot": """
# Context:
For the creation of a simplification corpus, you are asked to simplify sentences by removing spontaneous speech elements and making the text clear and concise.

# Instructions:
Your task is to simplify and remove spontaneous speech elements in the sentence in French and provide a simplified version in French.
"""
},
{"one-shot": """
# Context:
For the creation of a simplification corpus, you are asked to simplify sentences by removing spontaneous speech elements and making the text clear and concise.

# Instructions:
Your task is to simplify and remove spontaneous speech elements in the sentence in French and provide a simplified version in French.

Here is an example:
Sentence: \"Alors, euh, à la suite de la dislocation de l'URSS en, euh, en 1991, ben, l'Ukraine, euh... enfin, l'Ukraine a retrouvé son indépendance, voilà.\"
Simplification: \"En 1991, l'Ukraine gagne son indépendance de l'Union soviétique.\"
"""},
{"few-shot": """
# Context:
For the creation of a simplification corpus, you are asked to simplify sentences by removing spontaneous speech elements and making the text clear and concise.

# Instructions:
Your task is to simplify and remove spontaneous speech elements in the sentence in French and provide a simplified version in French.

Here are some examples:
Sentence: \"Alors, euh, à la suite de la dislocation de l'URSS en, euh, en 1991, ben, l'Ukraine, euh... enfin, l'Ukraine a retrouvé son indépendance, voilà.\"
Simplification: \"En 1991, l'Ukraine gagne son indépendance de l'Union soviétique.\"

Sentence: \"Ben, euh, un jour férié, c'est un jour de fête, euh, civile, religieuse, ou, euh, qui commémore un événement.\"
Simplification: \"Un jour férié est un jour de fête civile ou religieuse.\"

Sentence: \"Durant, durant les années soixante, euh, elle est le mannequin le mieux payé au monde.\"
Simplification: \"Elle est la mannequin la mieux payée du monde pendant les années soixante.\"

Sentence: \"Un androïde, c'est un robot construit à l'image d'un homme, euh, et par extension sémantique, euh, d'un être humain.\"
Simplification: \"Un androïde est un robot à forme humaine.\"

Sentence: \"Alors, euh, un arbre fruitier, c'est un arbre, euh, cultivé spécialement pour ses fruits, euh, comestibles.\"
Simplification: \"Un arbre fruitier est un arbre qui produit des fruits comestibles.\"
"""},
{"multistep": """
# Context:
For the creation of a simplification corpus, you are asked to simplify sentences by removing spontaneous speech elements and making the text clear and concise.

# Steps:
1. Rewrite the sentence to make it more understandable.
2. Remove the spontaneous traits.
3. If needed, restore its grammaticality.

# Instructions:
Your task is to simplify and remove spontaneous speech elements in the sentence in French and provide a simplified version in French.
"""},
{"cot": """
# Context:
For the creation of a simplification corpus, you are asked to simplify sentences by removing spontaneous speech elements and making the text clear and concise.

# Steps:
1. Identify the Main Idea: Read the sentence carefully and determine its main idea or key message.
2. Remove Extraneous Details: Eliminate any words or phrases that are not essential to conveying the main idea. Focus on removing spontaneous or off-topic comments.
3. Simplify Vocabulary: Replace complex or technical words with simpler, more common alternatives that retain the original meaning.
4. Clarify Sentence Structure: Reorganize the sentence to improve clarity and flow. Ensure the subject, verb, and object are clear and concise.
5. Check for Consistency: Ensure that the sentence maintains a consistent tone and style with the rest of the text.
6. Final Review: Read the simplified sentence to ensure it accurately conveys the original meaning without the spontaneous speech.

# Instructions:
Your task is to simplify and remove spontaneous speech elements in the sentence in French and provide a simplified version in French. Let's think step by step.
"""},
{"cot-self": """
# Context:
For the creation of a simplification corpus, you are asked to simplify sentences by removing spontaneous speech elements and making the text clear and concise. Three completely independent linguists who reason differently need to perform this task. The final answer is obtained by majority vote.

# Steps:
1. Identify the Main Idea: Read the sentence carefully and determine its main idea or key message.
2. Remove Extraneous Details: Eliminate any words or phrases that are not essential to conveying the main idea. Focus on removing spontaneous or off-topic comments.
3. Simplify Vocabulary: Replace complex or technical words with simpler, more common alternatives that retain the original meaning.
4. Clarify Sentence Structure: Reorganize the sentence to improve clarity and flow. Ensure the subject, verb, and object are clear and concise.
5. Check for Consistency: Ensure that the sentence maintains a consistent tone and style with the rest of the text.
6. Final Review: Read the simplified sentence to ensure it accurately conveys the original meaning without the spontaneous speech.

# Instructions:
Your task is to simplify and remove spontaneous speech elements in the sentence in French and provide a simplified version in French. Let's think step by step.
"""},
{"tree-of-thought": """
# Context:
For the creation of a simplification corpus, you are asked to simplify sentences by removing spontaneous speech elements and making the text clear and concise. During the task, three experts from different fields are brought to work together:
Linguist: Specializes in the linguistic phenomena of language.
Content Strategist: Specializes in organizing and presenting content in a way that is clear, concise, and user-focused.
Educator: Specializes in adapting text to match the reading level and comprehension abilities of students.

# Instructions:
Your task is to simplify and remove spontaneous speech elements in the sentence in French and provide a simplified version in French. Let's think step by step.
"""}
]
