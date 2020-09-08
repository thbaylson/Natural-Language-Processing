import datetime
import os

class Logger:
    """Do Stuff """

    def log(self, rule: dict, raw: str) -> None:
        """
        Recieves a rule dictionary and a raw input string to create 
        a log string. Writes the log string to the log.csv file
        """
        
        log_string = self.split_rule(rule)
        log_string += self.get_date_time()
        log_string += "," + raw
        self.write_to_log(log_string)

    def split_rule(self, rule: dict)->str:
        """Splits a dict into a comma separeted string"""

        rule_string = '{},{},{},{},{}'\
            .format(rule['acting_user'], rule['action'], rule['res_type'], rule['res'], rule['target_user'])
        return rule_string

    def get_date_time(self) -> str:
        """Finds the date and time and returns it in a comma seperated string"""
        time = datetime.datetime.now()
        return ",{},{}".format(time.strftime("%x"), time.strftime("%X"))

    def write_to_log(self, inp:str) -> None:
        """Writes log information to log.csv"""

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
        logger_file = open("./log.csv", "a+")
        logger_file.write(str(id_number) + "," + inp + "\n")
        logger_file.close()

