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
def complex_input():
    inp =  'only Bob is allowed to edit my documents after office hour and during the weekend'
    word_list = ['only', 'Bob', 'is', 'allowed', 'to', 'edit', 'my', 'documents', 'after', 'office', 
        'hour', 'and', 'during', 'the', 'weekend']
    
    grammar_info = [ 
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
    
    syntax_info_long = '((<only, (preposition, adjective, -)>, <Bob, (noun, subject, -)>, \
        <is allowed to edit, (verb, main, -)>, (<my, (adjective,possessive, -)>, \
        <documents, (noun, plural, -)>, <after, (preposition, adjective, -)>, \
        <office, (adverb, , -)>, <hour, (noun, singular, -)>, <and, (conjunction, , -)>, \
        <during, (preposition, , -)>, <the, (determiner, , -)>, <weekend, (adverb, , -)>'

    # t1 is a timestamp, this may not always be t1
    syntax_info_short = '((t1,’0’), (<only, (subject, ∃, accessing user, -)>, \
        <Bob, (subject, ∃, accessing user, -)>, < edit, (action, edit, -)>, \
        <my, (object, ∃, target user, -)>, <documents, (object, ∀, target recourse, -)>, \
        < (time: office hour+, weekend)>)'

    rule = '{(∃ user (name: Bob)), (action (name: edit)), (∀ target_resource (name: document), \
        ∃ target_user (name: _myself)), (environment_conditions (time: >office hour, weekend))} - t1'

    return [inp, word_list, grammar_info, syntax_info_long, syntax_info_short, rule]

#def test_tokens(complexInput):
#    assert cp.getTokens(complexInput[0]) == complexInput[1]

def test_grammar(complex_input):
    assert cp.get_grammar(complex_input[0]) == complex_input[2]

def test_syntax_long(complex_input):
    assert cp.get_syntax_long(complex_input[2]) == complex_input[3]

def test_syntax_short(complex_input):
    assert cp.get_syntax_short(complex_input[3]) == complex_input[4]

def test_rule(complex_input):
    assert cp.get_rule(complex_input[4]) == complex_input[5]

def test_write_to_file(complex_input):
    # Collect the current contents of the policy file
    policy_file = open("policy.txt", "r")
    old_file_contents = policy_file.read()
    policy_file.close()

    # Append the new policy
    cp.write_to_file(complex_input[5])

    # Assert that the policy has been appended correctly
    policy_file = open("policy.txt", "r")
    new_file_contents = policy_file.read()
    assert new_file_contents == (old_file_contents + "\n" + str(complex_input[5]))
