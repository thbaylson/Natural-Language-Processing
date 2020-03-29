import re
import sys
from enum import Enum

import spacy


class AccessWords(Enum):
    access = "access"
    append = "append"
    change = "change"
    edit = "edit"
    manipulate = "manipulate"
    modify = "modify"
    read = "read"
    update = "update"
    use = "use"
    write = "write"


def main(inp: list) -> None:
    nlp = spacy.load("en_core_web_sm")

    processed_input = process_input(inp)
    print("[After processInput()]:", processed_input)

    # tokens = getTokens(processedInput)
    # print("\nMain [After getTokens()]:", tokens)

    # The call nlp() uses the default model. To speed things up, we may want to define our own model
    tokens = nlp(processed_input)

    grammar = get_grammar(tokens)
    print("\n[After getGrammar()]:", grammar)

    syntax_long = get_syntax_long(grammar)
    print("\n[After getSyntaxLong()]:", syntax_long)

    syntax_short = get_syntax_short(syntax_long)
    print("\n[After getSyntaxShort()]:", syntax_short)

    rule = get_rule(syntax_short)
    print("\n[After getRule()]:", rule)

    print("Access: ", has_access_action(syntax_short))
    print("Negation: ", has_negation(syntax_short))

    print_grammar(grammar)

    write_to_file(rule)


def process_input(inp: list) -> str:
    """ 
    Recieve command line input, search for errors, and split the input on
    word boundaries.
    TODO: Write usage notes into README
    """

    # Match the first command line argument independent of OS
    match_object = re.search('capstone.py', '.\\capstone.py')
    if match_object is not None:
        # Trims off the command line file call
        inp = inp[1:]
    return str(inp)


def print_grammar(grammar: dict) -> None:
    col_width = 0
    for word in grammar:
        if len(word) > col_width:
            col_width = len(word) + 2

    print("Processed Info:")
    print('{0:<{col_width}} {1:<{col_width}} {2:^10} {3:^8}'.format("Word", "Part of Speech",
                                                                    "Negation", "Access",
                                                                    col_width=col_width))
    word_index = 0
    part_of_speech_index = 1

    for word in grammar:
        word_str = grammar[word][word_index]
        pos_str = grammar[word][part_of_speech_index]
        neg = ""
        acc = ""
        if is_negation_word(grammar[word]):
            neg = "-"
        if is_access_word(word):
            acc = "*"
        print('{0:<{col_width}} {1:<{col_width}} {2:^10} {3:^8}'.format(word_str, pos_str, neg,
                                                                        acc, col_width=col_width))

"""
def getTokens(inp):
    Placeholder function to help set up PyTest
    #SpaCy can tokenize.
    return nlp(inp)
"""


def get_grammar(tokens: list) -> dict:
    """ Placeholder function to help set up PyTest"""
    # SpaCy can find tokens and parts of speech at the same time
    grammar = {}

    # Creates a dictionary with keys being the input words and their values being that input
    # word's P.O.S.
    for token in tokens:
        grammar[token.text.lower()] = [token.pos_.lower(),
                                       token.dep_.lower()]

    # Remove punctuation from the grammar
    words_to_remove = []
    for word in grammar:
        if 'punct' in grammar[word]:
            words_to_remove.append(word)

    for word in words_to_remove:
        del grammar[word]

    return grammar


def get_syntax_long(grammar: dict) -> dict:
    """ Placeholder function to help set up PyTest"""
    return grammar


def get_syntax_short(syn_long: dict) -> dict:
    """ Placeholder function to help set up PyTest"""
    return syn_long


def get_rule(syn_short: dict) -> dict:
    """ Placeholder function to help set up PyTest"""
    return syn_short


def write_to_file(rule: dict) -> None:
    """ Prints the policy rule to the policy file"""
    policy_file = open("./policy.txt", "a")
    policy_file.write("\n" + str(rule))
    policy_file.close()


def has_access_action(grammar: dict) -> bool:
    """
    Searches a dictionary of words to identify if it contains an access word.
    """
    has_access = False
    for word in grammar:
        if 'root' in grammar[word]:
            if is_access_word(word):
                has_access = True

    return has_access


def is_access_word(word: str) -> bool:
    has_access = False
    access_words = [item.value for item in AccessWords]
    if word in access_words:
        has_access = True
    return has_access


def has_negation(grammar: dict) -> bool:
    """
    Searches a dictionary of words to identify if it contains a negating word.
    """
    negation_exists = False
    for word in grammar:
        if is_negation_word(grammar[word]):
            negation_exists = True
    return negation_exists


def is_negation_word(word: list) -> bool:
    return 'neg' in word


if __name__ == "__main__":
    main(sys.argv)
