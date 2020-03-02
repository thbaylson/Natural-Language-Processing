"""
Run all test files:
    pytest
Run one test file:
    pytest test.py
Run one test function in one test file:
    pytest test.py::test_func
"""

import pytest
import capstone as cp

@pytest.fixture
def complexInput():
    inp =  'only Bob is allowed to edit my documents after office hour and during the weekend'
    wordList = ['only', 'Bob', 'is', 'allowed', 'to', 'edit', 'my', 'documents', 'after', 'office', 
        'hour', 'and', 'during', 'the', 'weekend']
    
    grammarInfo = [ 
        ['only', ['preposition', 'adjective']], 
        ['Bob', ['noun', 'subject']], 
        ['is', ['verb', 'to be']], 
        ['allowed', ['verb', 'main']], 
        ['to', ['preposition']], 
        ['edit', ['verb']],
        ['my', ['adjective', 'possessive']], 
        ['documents', ['noun', 'plural']], 
        ['after', ['preposition', 'adjective']], 
        ['office', ['adverb']], 
        ['hour', ['noun', 'singular']], 
        ['and', ['conjunction']],
        ['during', ['preposition']], 
        ['the', ['determiner']], 
        ['weekend', ['adverb']]
        ]
    
    syntaxInfoLong = '((<only, (preposition, adjective, -)>, <Bob, (noun, subject, -)>, \
        <is allowed to edit, (verb, main, -)>, (<my, (adjective,possessive, -)>, \
        <documents, (noun, plural, -)>, <after, (preposition, adjective, -)>, \
        <office, (adverb, , -)>, <hour, (noun, singular, -)>, <and, (conjunction, , -)>, \
        <during, (preposition, , -)>, <the, (determiner, , -)>, <weekend, (adverb, , -)>'

    # t1 is a timestamp, this may not always be t1
    syntaxInfoShort = '((t1,’0’), (<only, (subject, ∃, accessing user, -)>, \
        <Bob, (subject, ∃, accessing user, -)>, < edit, (action, edit, -)>, \
        <my, (object, ∃, target user, -)>, <documents, (object, ∀, target recourse, -)>, \
        < (time: office hour+, weekend)>)'

    rule = '{(∃ user (name: Bob)), (action (name: edit)), (∀ target_resource (name: document), \
        ∃ target_user (name: _myself)), (environment_conditions (time: >office hour, weekend))} - t1'

    return [inp, wordList, grammarInfo, syntaxInfoLong, syntaxInfoShort, rule]

#def test_tokens(complexInput):
#    assert cp.getTokens(complexInput[0]) == complexInput[1]

def test_grammar(complexInput):
    assert cp.getGrammar(complexInput[0]) == complexInput[2]

def test_syntaxLong(complexInput):
    assert cp.getSyntaxLong(complexInput[2]) == complexInput[3]

def test_syntaxShort(complexInput):
    assert cp.getSyntaxShort(complexInput[3]) == complexInput[4]

def test_rule(complexInput):
    assert cp.getRule(complexInput[4]) == complexInput[5]

def test_writeToFile(complexInput):
    # Collect the current contents of the policy file
    policyFile = open("policy.txt", "r")
    oldFileContents = policyFile.read()
    policyFile.close()

    # Append the new policy
    cp.writeToFile(complexInput[5])

    # Assert that the policy has been appended correctly
    policyFile = open("policy.txt", "r")
    newFileContents = policyFile.read()
    assert newFileContents == (oldFileContents + "\n" + str(complexInput[5]))