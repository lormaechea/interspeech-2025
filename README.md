# Interspeech submission

### Supplementary materials for our submitted paper to Interspeech 2025

---

### 1. Repo structure: 

This repository provides supplementary materials for our submission entitled "__Towards High-Quality LLM-Based Data for French Spontaneous Speech Simplification: an Exo-Refinement Approach__" for  the next edition of Interspeech. The main goal is to provide all the codes and prompt templates to generate reproducible results. 

To this end, we include:
- The designed code along with the different generative prompting templates to implement the iterative generation-evaluation workflow and thus produce synthetic simplifications.
- The set of collected expert-based simplifications, that allowed to evaluate the quality of the generated outputs under different automatic metrics.

```
interspeech-2025/
├── README.md
├── data/
│   ├── experts/ 
│   │   └── expert_simplifications_all.tsv  # Collected reference simplifications
│   └── orfeo/
│       └── conversations/    # Set of 240 sentences from orfeo-cefc set
├── generate_data_mistral.py  # Script to run Mistral-based LLMs
├── generate_data_openai.py   # Script to run OpenAI-based LLMs
├── modules/
│   ├── functions_mistral.py
│   ├── functions_openai.py
│   └── templates/
│       ├── evaluation.py     # Evaluation prompts
│       ├── generation.py     # Generation prompts
│       └── topeval.py        # Top-evaluator prompt
└── requirements.txt
```

---

### 2. Installation:

__Prerequisites__: 
- Python 3.10.8 or above.
- Obtain a MistralAI API key: https://console.mistral.ai/api-keys/ (alternatively, run LLMs locally).
- Obtain an OpenAI API key: https://openai.com/index/openai-api/.

```
$ git clone git@github.com:lormaechea/interspeech-2025.git
$ cd interspeech-2025
$ pip install -e requirements.txt
```

---

### 3. How to use:

```
$ python generate_data_mistral.py # To generate Mistral-based synthetic simplifications
$ python generate_data_openai.py  # To generate OpenAI-based synthetic simplifications
```

### 4. Authors

<!-- If you find this repository helpful, feel free to cite our publication [Towards High-Quality LLM-Based Data for French Spontaneous Speech Simplification: an Exo-Refinement Approach](https://to_appear):-->

```bibtex 
@inproceedings{ormaechea-2025-speech-simplification,
    title = {Towards High-Quality LLM-Based Data for French Spontaneous Speech Simplification: an Exo-Refinement Approach},
    author = {Lucía Ormaechea, Nikos Tsourakis, Pierrette Bouillon, Benjamin Lecouteux and Didier Schwab},
    booktitle = {Proc. Interspeech 2025},
    year = {2025},
    location = {Rotterdam, Netherlands},
    url = {To appear},
}
``` 

__Contact person__: [Lucía Ormaechea](https://luciaormaechea.com/), [lucia.ormaecheagrijalba@unige.ch](mailto:lucia.ormaecheagrijalba@unige.ch)

If you have further questions, don't hesitate to send us an email.
