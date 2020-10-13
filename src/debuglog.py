class DebugLog:

    def __init__(self):
        self.calling_class = ""
        self.debug_output = False

    def set_debugging(self, output_on):
        self.debug_output = output_on

    def set_calling_class(self, class_name):
        self.calling_class = class_name

    def error(self, input):
        if self.debug_output:
            print("\n ---- \n DEBUG ERROR: ", input, "\n ---- \n")

    def warn(self, input):
        if self.debug_output:
            print("\n !!! DEBUG WARNING: ", input, "\n")

    def info(self, input):
        if self.debug_output:
            print("\nDEBUG INFO: ", input, "\n")

    def debug(self, input):
        if self.debug_output:
            print("\nDEBUG DEBUG: ", input, "\n")