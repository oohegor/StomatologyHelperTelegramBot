import json
from fuzzywuzzy import fuzz
from pymystem3 import Mystem

"""The algorithm for answering the question will be as follows:

1. We get the text of the question from the user;
2. Lemmatize all the words in the user's text;
3. Compare the resulting text with all the lemmatized questions from the knowledge base (Levenshtein distance);
4. We select the most “similar” question from the knowledge base;
5. We send the answer to the selected question to the user;

To implement our plans, we need libraries: fuzzywuzzy (for fuzzy comparisons) and pymystem3 (for lemmatization).
"""

# morphological analyzer object creation
morph = Mystem()

# loading knowledge base
with open("knowledge_base.json") as json_file:
    faq = json.load(json_file)


def classify_question(text):
    # lemmatization of user text
    text = ' '.join(morph.lemmatize(text))

    # we take questions from the knowledge base
    questions = list(faq.keys())
    scores = list()

    # cycle on all questions from the knowledge base
    for question in questions:
        # lemmatization of a question from a knowledge base
        norm_question = ' '.join(morph.lemmatize(question))
        # comparison of a user’s question and a knowledge base question
        scores.append(fuzz.token_sort_ratio(norm_question.lower(), text.lower()))

    # getting an answer
    answer = faq[questions[scores.index(max(scores))]]

    return answer
