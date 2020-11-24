import datetime
import json
import pandas as pd
import os
from pathlib import Path
from debuglog import DebugLog as debug

class Logger:
    """
    Creates and maintains a log of information. Such information includes: well formed rules, 
    the data and time the rule was created, and the raw user input sentence.
    """

    debuglog = debug()
    debuglog.set_calling_class = "Logger"
    debuglog.set_debugging(True)

    def log(self, rule: dict, raw: str) -> None:
        """
        Recieves a rule dictionary and a raw input string to create 
        a log string. Writes the log string to the log.csv file
        """
        filename = "log.json"
        Path(filename).touch()
        
        json_data = self.make_json(rule, raw)
        json_df = pd.DataFrame([json_data])
        
        # If the log file is not empty, read the file and append the new record to it
        if os.stat(filename).st_size > 0:
            log = pd.read_json(filename, orient= "table", convert_dates= False)
            log = log.append(json_df, ignore_index= True)
            log.to_json(filename, orient= "table")
        # If the log file is empty, write the json_df DataFrame to it
        else:
            json_df.to_json(filename, orient= "table")
        

    def make_json(self, rule: dict, raw: str) -> dict:
        """ Create a dictionary to be saved to a text file"""

        time = datetime.datetime.now()

        json_data = {}
        json_data["rule_id"] = self.get_id()
        json_data["acting_user"] = rule['acting_user']
        json_data["action"] = rule['action']
        json_data["target_type"] = rule['res_type']
        json_data["target_resource"] = rule['res']
        json_data["target_user"] = rule['target_user']
        json_data["has_conditional"] = 1 if(len(rule['conditions']) > 0) else 0
        json_data["date"] = time.strftime("%x")
        json_data["time"] = time.strftime("%X")
        json_data["raw"] = raw

        return json_data


    def get_id(self) -> int:
        """ Get the id number for the data"""

        id_number = 1

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
                id_number = int(rule_number[1]) + 1

        # Finally we append the new log to log.csv
        return id_number

