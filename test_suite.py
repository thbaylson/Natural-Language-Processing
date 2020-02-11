import pytest
import capstone as cp

@pytest.fixture
def testInput1():
    input =  'only Bob is allowed to edit my documents after office hour and during the weekend'
    wordList = '<only, Bob, is, allowed, to, edit, my, documents, after, office, hour, and, during, the, weekend>'
    
    grammarInfo = '((<only, (preposition, adjective, -)>, <Bob, (noun, subject, -)>, \
        <is, (verb, to be, -)>, <allowed, (verb, main, -)>, <to, (preposition, -, -)>, \
        <edit, (verb, , -)>, (<my, (adjective, possessive, -)>, <documents, (noun, plural, -)>, \
        <after, (preposition, adjective, -)>, <office, (adverb, , -)>, <hour, (noun, singular, -)>, \
        <and, (conjunction, , -)>,<during, (preposition, , -)>, <the, (determiner, , -)>, \
        <weekend, (adverb, , -)>)'
    
    syntaxInfoLong = '((<only, (preposition, adjective, -)>, <Bob, (noun, subject, -)>, \
        <is allowed to edit, (verb, main, -)>, (<my, (adjective,possessive, -)>, \
        <documents, (noun, plural, -)>, <after, (preposition, adjective, -)>, \
        <office, (adverb, , -)>, <hour, (noun, singular, -)>, <and, (conjunction, , -)>, \
        <during, (preposition, , -)>, <the, (determiner, , -)>, <weekend, (adverb, , -)>'

    syntaxInfoShort = '((t1,’0’), (<only, (subject, ∃, accessing user, -)>, \
        <Bob, (subject, ∃, accessing user, -)>, < edit, (action, edit, -)>, \
        <my, (object, ∃, target user, -)>, <documents, (object, ∀, target recourse, -)>, \
        < (time: office hour+, weekend)>)'

    rule = '{(∃ user (name: Bob)), (action (name: edit)), (∀ target_resource (name: document), \
        ∃ target_user (name: _myself)), (environment_conditions (time: >office hour, weekend))} - t1'

    return [input, wordList, grammarInfo, syntaxInfoLong, syntaxInfoShort, rule]

def test_tokens(testInput1):
    assert cp.getTokens(testInput1.input) == testInput1.wordList

def test_grammar(testInput1):
    assert cp.getGrammar(testInput1.wordList) == testInput1.grammarInfo

def test_syntaxLong(testInput1):
    assert cp.getSyntaxLong(testInput1.GrammarInfo) == testInput1.syntaxInfoLong

def test_syntaxShort(testInput1):
    assert cp.getSyntaxShort(testInput1.syntaxInfoLong) == testInput1.syntaxInfoShort

def test_rule(testInput1):
    assert cp.getRule(testInput1.syntaxInfoShort) == testInput1.rule

def test_alwaysTrue():
    assert cp.alwaysTrue() == True

