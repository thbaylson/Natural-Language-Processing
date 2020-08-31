from ui import ConsoleUI
from controller import Controller


def main():
    # Load base classes
    controller = Controller()

    # Running with ui console as default
    ui = ConsoleUI()

    # Run the ui while the user has not finished rule generation or requests
    while not ui.is_finished():
        inp = ui.receive_input()
        if not ui.is_finished():
            controller.process_input(inp)


if __name__ == "__main__":
    main()