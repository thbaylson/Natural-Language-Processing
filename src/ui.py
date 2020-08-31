class ConsoleUI:

    finished = False

    def receive_input(self):
        inp = input("Please enter a rule or request (q to exit): ")
        if inp == "q":
            self.finished = True
        return inp

    def is_finished(self):
        return self.finished
