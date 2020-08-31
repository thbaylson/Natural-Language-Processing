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
import controller as cp

nlp = spacy.load("en_core_web_sm")


@pytest.fixture
def simple_input():
    inp = 'Bob can edit my documents'
    word_list = ['Bob', 'can', 'edit', 'my', 'documents']

    # Heavily edited, needs review
    grammar_info = {
        'bob': ['propn', 'nsubj'],
        'can': ['verb', 'aux'],
        'edit': ['verb', 'root'],
        'my': ['det', 'poss'],
        'documents': ['noun', 'dobj']
    }

    # Around this point kick out unneccesary words
    syntax_info_long = {
        'bob': ['noun', 'subject'],
        'edit': ['verb', 'main'],
        'my': ['adjective', 'possessive'],
        'documents': ['noun', 'plural']
    }

    # t1 is a timestamp, this may not always be t1
    syntax_info_short = {
        't1': 0,
        'bob': ['subject', '∃', 'accessing user'],
        'edit': ['action', 'edit'],
        'my': ['object', '∃', 'target user'],
        'documents': ['object', '∀', 'target recourse']
    }

    # We want to keep the rule as one whole string because that's what's going into the policy file
    # This rule is modeled after Dr. Kate Morovat's policy file
    rule = 'Rule1 {(X user (name: Bob)), (action (name: edit)), (X target_resource (name: document)), (X target_user (name: Alice))}'


    return [inp, word_list, grammar_info, syntax_info_long, syntax_info_short, rule]


# def test_tokens(simpleInput):
#    assert cp.getTokens(simpleInput[0]) == simpleInput[1]

# Parts of speech checker test ie: A sentence should have at least a subject, a verb, etc

# Test subjects and resources against xml mock-database

# Test negations of access words

def test_grammar(simple_input):
    tokens = nlp(simple_input[0])
    assert cp.get_grammar(tokens) == simple_input[2]


def test_syntax_long(simple_input):
    assert cp.get_syntax_long(simple_input[2]) == simple_input[3]


def test_syntax_short(simple_input):
    assert cp.get_syntax_short(simple_input[3]) == simple_input[4]


def test_rule(simple_input):
    assert cp.get_rule(simple_input[4]) == simple_input[5]


def test_write_to_file(simple_input):
    """ This test is currently failing because:
    1) We do not have functionality for generating the rule properly
    2) Our rule is defined using invalid unicode characters"""
    # Collect the current contents of the policy file
    policy_file = open("../policy.txt", "r")
    old_file_contents = policy_file.read()
    policy_file.close()

    # Append the new policy
    cp.write_to_file(simple_input[5])

    # Assert that the policy has been appended correctly
    policy_file = open("../policy.txt", "r")
    new_file_contents = policy_file.read()
    assert new_file_contents == (old_file_contents + "\n" + str(simple_input[5]))
