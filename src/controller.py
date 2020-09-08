import re
import sys
import os

import spacy

# Uncomment to allow for word association graphing
# from spacy import displacy
# from pathlib import Path
from accesswords import AccessWords
from logger import Logger

# TODO: Need file headers


class Controller:

    def process_input(self, inp: str) -> None:
        # Load core reference
        nlp = spacy.load("en_core_web_sm")
        logger = Logger()

        # Get local file and folder information
        local_dir = '../'
        local_files = [file.path.split('/')[-1] for file in os.scandir(local_dir) if file.is_file()]
        local_folders = [folder.path.split('/')[-1] for folder in os.scandir(local_dir) if
                         folder.is_dir()]
        local_exts = [file.split('.')[-1] for file in local_files]

        # Process input
        processed_input = self.split_input(inp)

        # The call nlp() uses the default model. To speed things up, we may want to define our own model
        tokens = nlp(processed_input)

        # Uncomment to allow for output of graph
        """
        tokens = nlp("Bob can edit Alice's documents")
        svg = displacy.render(tokens, style="dep", jupyter=False)
        file_name = '-'.join([w.text for w in tokens if not w.is_punct]) + ".svg"
        output_path = Path(file_name)
        output_path.open("w", encoding="utf-8").write(svg)
        """

        # Build the grammar
        grammar = self.get_grammar(tokens)

        # Scan for target_resource
        target = self.get_target_resource(grammar, local_files, local_folders, local_exts)

        # Print out column display to demonstrate processing
        self.print_column_display(grammar)

        # Generate rule and write to files
        rule = self.get_rule(grammar, target)
        logger.log(rule, inp)

        rule = self.format_rule(rule)
        self.write_to_file(rule)

    def split_input(self, inp: list) -> str:
        """
        Recieve command line input, search for errors, and split the input on
        word boundaries.
        """
        # Match the first command line argument independent of OS
        match_object = re.search('capstone.py', 'controller.py')
        if match_object is not None:
            # Trims off the command line file call
            inp = inp[1:]
        return str(inp)


    def get_target_resource(self, inp: dict, files: list, folders: list, exts: list) -> dict:
        """
        If a specific file referenced, search locally for the file, confirm it exists, and append:
        (X target_resource (name: document))

        If a specific folder referenced, search locally for the folder, confirm it exists, and append:
        (X target_resource (case: folder))

        If no specific file or folder, but items of that type exist in directory, append:
        (X target_resource (case: filetype))
        """
        target = ""
        target_type = ""
        resource_found = False
        resource_data = {}

        # Search specific reference and specific folders
        for word in inp:
            if word in files:
                target = word
                target_type = "file"
                resource_found = True
        if not resource_found:
            # Search specific folders
            for word in inp:
                if word in folders:
                    target = word
                    target_type = "case"
                    resource_found = True
        if not resource_found:
            # Search filetype reference
            for word in inp:
                if word in exts:
                    target = word
                    target_type = "case"

        # Make correct info appendable
        resource_data[target] = target_type
        return resource_data


    def print_column_display(self, grammar: dict) -> None:
        """
        Prints a human readable column display of the input policy or query
        """
        col_width = 0
        col_name_word = "Word"
        col_name_pos = "Part of Speech"
        col_name_neg = "Negation"
        col_name_acc = "Access"

        # If the longest word is greater than our longest col header name
        for word in grammar:
            if len(word) > len(col_name_pos):
                col_width = len(word) + 2
            else:
                col_width = len(col_name_pos) + 2

        # Building the columns
        print("\nProcessed Info:")
        print('{0:<{width}} {1:<{width}} {2:^10} {3:^8}'.format(col_name_word, col_name_pos,
                                                                col_name_neg, col_name_acc,
                                                                width=col_width))
        # Fill out the columns
        pos_index = 1
        for word in grammar:
            pos_str = grammar[word][pos_index]
            neg = ""
            acc = ""
            if self.is_negation_word(grammar[word]):
                neg = "-"
            if self.is_access_word(word):
                acc = "*"
            print('{0:<{width}} {1:<{width}} {2:^10} {3:^8}'.format(word, pos_str, neg, acc,
                                                                    width=col_width))


    def get_grammar(self, tokens: list) -> dict:
        """ Placeholder function to help set up PyTest"""
        # SpaCy can find tokens and parts of speech at the same time
        grammar = {}

        # Creates a dictionary with keys being the input words and their values being that input
        # word's P.O.S.
        for token in tokens:
            grammar[token.text.lower()] = [token.pos_.lower(),
                                           token.dep_.lower(),
                                           token.lemma_.lower()]

        # Find punctuation in the grammar
        words_to_remove = []
        for word in grammar:
            if 'punct' in grammar[word]:
                words_to_remove.append(word)

        # Remove punctuation in the grammar
        for word in words_to_remove:
            del grammar[word]

        return grammar


    def get_syntax_long(self, grammar: dict) -> dict:
        """ Placeholder function to help set up PyTest"""
        return grammar


    def get_syntax_short(self, syn_long: dict) -> dict:
        """ Placeholder function to help set up PyTest"""
        return syn_long


    def get_rule(self, syn_short: dict, target_res: dict) -> dict:
        """
        Placeholder function to help set up PyTest
        resource_data[target] = target_type, where target_type is either case or name
        """
        rule = {}
        rule['acting_user'] = self.get_affected_user(syn_short) #The 'Bob' in 'Bob can access my documents'
        rule['action'] = self.get_access_action(syn_short)
        rule['res'] = list(target_res.keys())[0]
        rule['res_type'] = target_res[rule['res']]
        rule['target_user'] = self.get_target_user(syn_short) #The 'my' in 'Bob can access my documents'

        return rule

    def format_rule(self, rule: dict) -> str:
        """Formats the rule dictionary into a single String"""
        rule = '(X user (name: {})), (action (name: {})), (X target_resource ({}: {})), (X target_user (name: {}))'\
            .format(rule['acting_user'], rule['action'], rule['res_type'], rule['res'], rule['target_user'])
        return rule


    def write_to_file(self, rule: str) -> None:
        """Prints the policy rule to the policy file
        policy_file = open("./policy.txt", "a+")
        policy_file.write("\nRule1 {" + rule + "}")
        policy_file.close()
        """
        new_rule_number = 1

        # Use the with keyword here to let Python close the file even if there's an error.
        # Open the file for binary reading so that we can seek right to the end of the file.
        # This solution is very fast, but can have unintended outcomes due to working with raw bytes in UTF-8.
        with open('policy.txt', 'rb') as policy_file:
            # First we have to see if there are any bytes in the file.
            # If there aren't any, the file is empty and we don't need to do the following work.
            if(policy_file.read(1) != b''):

                # Seek to the end of the file offset by -2 bytes. So os.SEEK_CUR is now 2 bytes from the end of the file.
                policy_file.seek(-2, os.SEEK_END)

                # Loop until we find the byte sequence of a newline character.
                while policy_file.read(1) != b'\n':
                    policy_file.seek(-2, os.SEEK_CUR)

                # We need to decode() the readline() bc we opened the file in binary mode.
                last_line = policy_file.readline().decode()

                # Here we separate the last line into the 'Rule#' part and the policy-rule part.
                last_line_array = last_line.split(' ')

                # Now we split 'Rule#' by 'e' to grab just the number that comes after the 'e'.
                rule_number = last_line_array[0].rsplit('e')

                # Next we change the string number into an int and add 1
                new_rule_number = int(rule_number[1]) + 1

        # Finally we append the full rule with it's determined rule number to the policy file
        policy_file = open("./policy.txt", "a+")
        policy_file.write("\nRule" + str(new_rule_number) + " {" + rule + "}")
        policy_file.close()


    def get_access_action(self, grammar: dict) -> str:
        """
        Searches a dictionary of words to identify if it contains an access word.
        If the dictionary has an access word, this function returns that access word
        if it doesn't, it returns an empty string.
        """
        access = ""
        for word in grammar:
            if 'verb' in grammar[word]:
                # We have to check the word's root, which is last in the last
                if self.is_access_word(grammar[word][-1]):
                    access = (getattr(AccessWords, grammar[word][-1]).value)[1]
                    break
        return access


    def get_target_user(self, grammar: dict) -> str:
        """
        Searches a dictionary of words to identify if it contains a target user.
        If the dictionary has a target user, this function returns that user
        if it doesn't, it returns an empty string.
        """
        target = ""
        for word in grammar:
            if 'poss' in grammar[word]:
                if word == 'my':
                    home_dir = os.path.expanduser('~')
                    target = home_dir.split("\\")[-1]
                else:
                    target = word
                break
        return target.lower()


    def get_affected_user(self, grammar: dict) -> str:
        """
        Searches a dictionary of words to identify if it contains an affected user.
        If the dictionary has an affected user, this function returns that user
        if it doesn't, it returns an empty string.
        """
        affected = ""
        for word in grammar:
            if('propn' in grammar[word]):
                if ('nsubj' in grammar[word]) or ('nsubjpass' in grammar[word]) or ('pobj' in grammar[word]):
                    affected = word
                    break
        return affected


    def is_access_word(self, word: str) -> bool:
        """
        Identifies whether a word is an access word
        """
        has_access = False
        access_words = [item.value[0] for item in AccessWords]
        if word in access_words:
            has_access = True
        return has_access


    def has_negation(self, grammar: dict) -> bool:
        """
        Searches a dictionary of words to identify if it contains a negating word.
        """
        negation_exists = False
        for word in grammar:
            if self.is_negation_word(grammar[word]):
                negation_exists = True
                break
        return negation_exists


    def is_negation_word(self, word: list) -> bool:
        """
        Identifies whether a word is a negation
        """
        return 'neg' in word
