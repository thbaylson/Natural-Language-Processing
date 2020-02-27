import os.path
import re
import spacy
import sys

def main(inp):
    nlp = spacy.load("en_core_web_sm")

    processedInput = processInput(inp)
    print("\nMain [After processInput()]:", processedInput)

    #tokens = getTokens(processedInput)
    #print("\nMain [After getTokens()]:", tokens)

    # The call nlp() uses the default model. To speed things up, we may want to define our own model
    tokens = nlp(processedInput)
    grammar = getGrammar(tokens)
    print("\nMain [After getGrammar()]:", grammar)

    syntaxLong = getSyntaxLong(grammar)
    print("\nMain [After getSyntaxLong()]:", syntaxLong)

    syntaxShort = getSyntaxShort(syntaxLong)
    print("\nMain [After getSyntaxShort()]:", syntaxShort)

    rule = getRule(syntaxShort)
    print("\nMain [After getRule()]:", rule)

    writeToFile(rule)

def processInput(inp):
    """ 
    Recieve command line input, search for errors, and split the input on
    word boundaries.
    TODO: Write usage notes into README
    """

    # Match the first command line argument independent of OS
    matchObject = re.search('capstone.py', '.\\capstone.py')
    if matchObject != None:
        # Trims off the command line file call
        inp = inp[1:]
    return str(inp)

"""
def getTokens(inp):
    Placeholder function to help set up PyTest
    #SpaCy can tokenize.
    return nlp(inp)
"""

def getGrammar(tokens):
    """ Placeholder function to help set up PyTest"""
    # SpaCy can find tokens and parts of speech at the same time
    grammar = {}

    # Creates a dictionary with keys being the input words and their values being that input word's P.O.S.
    for token in tokens:
        grammar[(token.text).lower()] = [(token.pos_).lower(), (token.dep_).lower()]

    # Remove punction from the grammar
    keys_to_remove = []
    for key in grammar:
        if 'punct' in grammar[key]:
            keys_to_remove.append(key)
  
    for key in keys_to_remove:
        del grammar[key]

    print(grammar)
    return grammar

def getSyntaxLong(grammar):
    """ Placeholder function to help set up PyTest"""
    return grammar

def getSyntaxShort(synLong):
    """ Placeholder function to help set up PyTest"""
    return synLong

def getRule(synShort):
    """ Placeholder function to help set up PyTest"""
    return synShort

def writeToFile(rule):
    """ Prints the policy rule to the policy file"""
    policyFile = open("policy.txt", "a")
    policyFile.write("\n" + str(rule))
    policyFile.close()

if __name__ == "__main__":
    main(sys.argv)