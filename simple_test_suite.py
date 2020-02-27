"""
Run all test files:
    pytest
Run one test file:
    pytest test.py
Run one test function in one test file:
    pytest test.py::test_func
"""

import pytest
import spacy
import capstone as cp

nlp = spacy.load("en_core_web_sm")

@pytest.fixture
def simpleInput():
    inp =  'Bob can edit my documents'
    wordList = ['Bob', 'can', 'edit', 'my', 'documents']
    
    # Heavily edited, needs review
    grammarInfo = {
        'bob': ['propn', 'nsubj'],
        'can': ['verb', 'aux'],
        'edit': ['verb', 'root'],
        'my': ['det', 'poss'],
        'documents': ['noun', 'dobj']
    }
    
    syntaxInfoLong = {
        'bob': ['noun', 'subject'],
        'can edit': ['verb', 'main'],
        'my': ['adjective', 'possessive'],
        'documents': ['noun', 'plural']
    }

    # t1 is a timestamp, this may not always be t1
    syntaxInfoShort = {
        't1': 0,
        'bob': ['subject', '∃', 'accessing user'], 
        'edit': ['action', 'edit'],
        'my': ['object', '∃', 'target user'], 
        'documents': ['object', '∀', 'target recourse']
    }

    # We want to keep the rule as one whole string because that's what's going into the policy file
    rule = '{(∃ user (name: Bob)), (action (name: edit)), (∀ target_resource (name: document), \
        ∃ target_user (name: _myself)), (environment_conditions (time: >office hour, weekend))} - t1'

    return [inp, wordList, grammarInfo, syntaxInfoLong, syntaxInfoShort, rule]

#def test_tokens(simpleInput):
#    assert cp.getTokens(simpleInput[0]) == simpleInput[1]

def test_grammar(simpleInput):
    tokens = nlp(simpleInput[0])
    assert cp.getGrammar(tokens) == simpleInput[2]

def test_syntaxLong(simpleInput):
    assert cp.getSyntaxLong(simpleInput[2]) == simpleInput[3]

def test_syntaxShort(simpleInput):
    assert cp.getSyntaxShort(simpleInput[3]) == simpleInput[4]

def test_rule(simpleInput):
    assert cp.getRule(simpleInput[4]) == simpleInput[5]

def test_writeToFile(simpleInput):
    """ This test is currently failing because:
    1) We do not have functionality for generating the rule properly
    2) Our rule is defined using invalid unicode characters"""
    # Collect the current contents of the policy file
    policyFile = open("policy.txt", "r")
    oldFileContents = policyFile.read()
    policyFile.close()

    # Append the new policy
    cp.writeToFile(simpleInput[5])

    # Assert that the policy has been appended correctly
    policyFile = open("policy.txt", "r")
    newFileContents = policyFile.read()
    assert newFileContents == (oldFileContents + "\n" + str(simpleInput[5]))