from IPython.display import display, HTML
import plotly.express as px

from reporter import Reporter

class ConsoleUI:

    finished = False
    finished_prompt = False

    def receive_input(self) -> str:
        inp = input("\n0: Quit\n1: Create New Rule\n2: Run an Analysis\n>> ")
        if inp == "0":
            self.finished = True
        if inp == "1":
            inp += input("\nCreate New Rule\n>> ")
        if inp == "2":
            while(not self.finished_prompt):
                self.prompt_for_report()

            self.finished_prompt = False
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

    def report_wrapper(self, title: str, output) -> None:
        """ Used to print reports that don't need a row count"""
        print(title + "\n" + str(output))
        input("(Enter to Continue)")
    
    def report_wrapper_count(self, title: str, func: object) -> None:
        """ Used to print reports that may need a row count"""
        rows = input(title + "\nHow Many Rows?\n>> ")
        print(func(int(rows) if rows != '' else 5 ))
        input("(Enter to Continue)")

    def is_finished(self) -> bool:
        return self.finished
