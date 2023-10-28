import os
import sys
from PhoneBook import Record, AddressBook

# Function decorator for validating function arguments
def validate_args(expected_arg_count, command_example):
    def decorator(func):
        def wrapper(*args):
            if len(args[0]) != expected_arg_count:
                return f"[error] Invalid command format. Please use '{command_example}'."
            return func(*args)
        return wrapper
    return decorator


# Function for processing the "add" command
@validate_args(2, 'add [name] [phone]')
def add_contact(args, contacts):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return "[ok] Contact added."


# Function for processing the "change" command
@validate_args(2, 'change [name] [phone]')
def change_contact(args, contacts):
    name, phone = args
    record = contacts.find(name)
    print(record)
    if record is not None:
        old_phone = record.phones[0].value
        record.edit_phone(old_phone, phone)
        return "[ok] Contact updated."
    else:
        return "[info] Contact not found."


# Function for processing the "phone" command
@validate_args(1, 'phone [name]')
def show_phone(args, contacts):
    name = args[0]
    record = contacts.find(name)
    if record is not None:
        phone = record.phones[0]
        return f"Phone: {phone}"
    else:
        return "[info] Contact not found."


# Function for processing the "all" command
def show_all(contacts):
    if contacts:
        return "\n".join([f"{name}: {phone}" for name,
                         phone in contacts.items()])
    else:
        return "[info] No contacts."

def help():
    help = "[info] You can use the following commands: hello, add, change, phone, all, close, exit, help"
    return help

# The main function for user interaction
def main():
    contacts = AddressBook()
    # Starter dictionary for storing contacts
    print("[*] Welcome to the assistant bot!")

    while True:
        user_input = input("[*] Enter a command: ")
        command, *args = user_input.split()
        command = command.strip().lower()

        if command == "hello":
            print("[*] How can I help you?")
        elif command.startswith("add"):
            print(add_contact(args, contacts))
        elif command.startswith("change"):
            print(change_contact(args, contacts))
        elif command.startswith("phone"):
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        elif command == "help":
            print(help())
        elif command in ["close", "exit"]:
            print("[*] Good bye!")
            break
        else:
            print("[error] Invalid command.")


# Main function
if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print('\n[*] Good bye!')
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)