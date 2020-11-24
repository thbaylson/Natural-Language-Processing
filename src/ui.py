from wordcloud import WordCloud, STOPWORDS
from reporter import Reporter
from debuglog import DebugLog as debug

class ConsoleUI:

    finished = False
    finished_prompt = False

    debuglog = debug()
    debuglog.set_calling_class = "ConsoleUI"
    debuglog.set_debugging(True)

    def receive_input(self) -> str:
        inp = input("\n0: Quit\n1: Create New Rule\n2: Run an Analysis\n3: Processed Info\n>> ")
        if inp == "0":
            self.finished = True
        if inp == "1":
            inp += input("\nCreate New Rule\n>> ")
        if inp == "2":
            while(not self.finished_prompt):
                self.prompt_for_report()

            self.finished_prompt = False
        if inp == "3":
            print("\nProcessed Info\n")
        return inp

    def prompt_for_report(self):
        """ Promt the user for what kind of analysis they want to perform"""
        report = Reporter()

        print("\nChoose an Analysis Option:")
        inp = input("0: Back\n1: Display Last # Rows \
                            \n2: Show Functioning Policies \
                            \n3: Employee Policy Count \
                            \n4: Column Error Count \
                            \n5: Find Errors \
                            \n6: Find Suspicious Activity \
                            \n7: Make WordCloud \
                            \n>> ")
        if inp == "0":
            self.finished_prompt = True
        
        elif inp == "1":
            self.report_wrapper_count("\nLast Rows", report.log_tail)

        elif inp == "2":
            self.report_wrapper_count("\nShow Functioning Policies", report.not_null)
        
        elif inp == "3":
            self.report_wrapper("\nEmployee Policy Count", report.employee_policy_count())
        
        elif inp == "4":
            self.report_wrapper("\nColumn Error Count", report.col_errors())
        
        elif inp == "5":
            self.report_wrapper("\nFind Errors", report.find_errors())
        elif inp == "6":
            self.report_wrapper("\nFind Suspicious Activity", report.find_suspicious_activity())
        elif inp == "7":
            self.make_word_cloud(report.log_df)

    def report_wrapper(self, title: str, output) -> None:
        """ Used to print reports that don't need a row count"""
        print(title + "\n" + str(output))
        input("(Enter to Continue)")
    
    def report_wrapper_count(self, title: str, func: object) -> None:
        """ Used to print reports that may need a row count"""
        rows = input(title + "\nHow Many Rows?\n>> ")
        print(func(int(rows) if rows != '' else 5 ))
        input("(Enter to Continue)")

    def make_word_cloud(self, df) -> None:
        """ Creates a WordCloud from a Pandas DataFrame and the saves it to the resources folder"""
        cloud_words = '' 
        
        #cloud_df = log_df[['acting_user', 'action', 'target_type', 'target_resource', 'target_user', 'raw']]
        cloud_df = df[['raw']]
        
        # iterate through the csv file 
        for val in cloud_df.to_numpy():
            
            # typecaste each val to string 
            val = str(val)
        
            # split the value 
            tokens = val.split() 
                
            # Converts each token into lowercase 
            for i in range(len(tokens)): 
                tokens[i] = tokens[i].lower()
            
            cloud_words += " ".join(tokens) + " "
        
        wordcloud = WordCloud(width = 800, height = 800, 
                            stopwords = set(STOPWORDS), 
                            min_font_size = 15
                            ).generate(cloud_words) 
        
        wordcloud.to_file("../resources/word_cloud.png")

    def display_processed_info(self, string: str) -> None:
        print(string)

    def is_finished(self) -> bool:
        return self.finished
