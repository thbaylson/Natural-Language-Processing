from ui import ConsoleUI
from controller import Controller
from debuglog import DebugLog as debug

debuglog = debug()
debuglog.set_calling_class = "Capstone"
debuglog.set_debugging(True)

def main():

    # Load base classes
    controller = Controller()

    # Running with ui console as default
    ui = ConsoleUI()

    # Run the ui while the user has not finished rule generation or requests
    while not ui.is_finished():
        inp = ui.receive_input()
        if len(inp) > 0:
            if not ui.is_finished() and inp[0] == "1":
                if len(inp) > 1:
                    controller.process_input(inp[1:])
            if not ui.is_finished() and inp[0] == "3":
                ui.display_processed_info(controller.last_entry)

if __name__ == "__main__":
    main()