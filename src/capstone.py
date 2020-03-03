import os.path
import re
import spacy
import sys

from enum import Enum


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


"""
def getTokens(inp):
    Placeholder function to help set up PyTest
    #SpaCy can tokenize.
    return nlp(inp)
"""


def get_grammar(tokens: spacy.tokens.doc.Doc) -> dict:
    """ Placeholder function to help set up PyTest"""
    # SpaCy can find tokens and parts of speech at the same time
    grammar = {}

    # Creates a dictionary with keys being the input words and their values being that input word's P.O.S.
    for token in tokens:
        grammar[(token.text).lower()] = [(token.lemma_).lower(),
                                         (token.pos_).lower(),
                                         (token.dep_).lower()]

    # Remove punctuation from the grammar
    keys_to_remove = []
    for key in grammar:
        if 'punct' in grammar[key]:
            keys_to_remove.append(key)

    for key in keys_to_remove:
        del grammar[key]

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


def has_access_action(dictionary: dict) -> bool:
    """
    Searches a dictionary of words to identify if it contains an access word.
    """
    has_access = False
    for key in dictionary:
        if 'root' in dictionary[key]:

            access_words = [item.value for item in AccessWords]
            for key2 in dictionary[key]:
                if key2 in access_words:
                    has_access = True

    return has_access


def has_negation(dictionary: dict) -> bool:
    """
    Searches a dictionary of words to identify if it contains a negating word.
    """
    negation_exists = False
    for key in dictionary:
        if 'neg' in dictionary[key]:
            negation_exists = True

    return negation_exists


if __name__ == "__main__":
    main(sys.argv)
