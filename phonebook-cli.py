import os
import sys
from PhoneBook import AddressBook, Record


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
    try:
        name, phone = args
        record = Record(name)
        record.add_phone(phone)
        contacts.add_record(record)
    except ValueError as ve:
        return f"[error] {ve}"
    else:
        return "[ok] Contact added."


# Function for processing the "change" command
@validate_args(2, 'change [name] [phone]')
def change_contact(args, contacts):
    name, phone = args
    record = contacts.find(name)
    if record is not None:
        old_phone = record.get_phone()
        try:
            record.edit_phone(old_phone, phone)
        except ValueError as ve:
            return f"[error] {ve}"
        else:
            return "[ok] Contact updated."
    else:
        return "[info] Contact not found."


# Function for processing the "phone" command
@validate_args(1, 'phone [name]')
def show_phone(args, contacts):
    name = args[0]
    record = contacts.find(name)
    if record is not None:
        phone = record.get_phones()
        return f"[ok] Phone(s): {phone}"
    else:
        return "[info] Contact not found."


# Function for processing the "all" command
def show_all(contacts):
    if contacts:
        return "\n".join(
            [f"\040" * 5 + f"{single_record}" for _, single_record in contacts.data.items()])
    else:
        return "[info] No contacts."


# Function for processing the "add-birthday" command
@validate_args(2, 'add-birthday [name] [birthday]')
def add_birthday(args, contacts):
    try:
        name, birthday = args
        record = Record(name)
        record.add_birthday(birthday)
        contacts.add_record(record)
    except ValueError as ve:
        return f"[error] {ve}"
    else:
        return "[ok] Birthday added."


# Function for processing the "show-birthday" command
@validate_args(1, 'show-birthday [name]')
def show_birthday(args, contacts):
    name = args[0]
    record = contacts.find(name)
    if record is not None:
        birthday = record.show_birthday()
        return f"[ok] Birthday: {birthday}"
    else:
        return "[info] Contact not found."


# Function for processing the "birthdays" command
def show_next_week_birthdays(contacts):
    if contacts:
        return contacts.get_birthdays_per_week()
    return "[info] No contacts."


# Function of displaying information about available commands
def help():
    help = "[info] You can use the following commands: hello, add, change, phone, all, close, exit, help"
    return help


# The main function for user interaction
def main():
    contacts = AddressBook()

    print("[*] Welcome to the assistant bot!")

    while True:
        # 'end_of_command_marker' -- this is a solution to distinguish between commands that share a common prefix.
        # For example, the commands 'add' and 'add-birthday'.
        end_of_command_marker = '_eocm_'
        try:
            user_input = input("[*] Enter a command: ")
            command, *args = user_input.split()
            command = command.strip().lower() + end_of_command_marker
        except (ValueError, EOFError):
            continue
        if command == "hello" + end_of_command_marker:
            print("[*] How can I help you?")
        elif command.startswith("add" + end_of_command_marker):
            print(add_contact(args, contacts))
        elif command.startswith("change" + end_of_command_marker):
            print(change_contact(args, contacts))
        elif command.startswith("phone" + end_of_command_marker):
            print(show_phone(args, contacts))
        elif command == "all" + end_of_command_marker:
            print(show_all(contacts))
        elif command.startswith("add-birthday" + end_of_command_marker):
            print(add_birthday(args, contacts))
        elif command.startswith("show-birthday" + end_of_command_marker):
            print(show_birthday(args, contacts))
        elif command == "birthdays" + end_of_command_marker:
            print(show_next_week_birthdays(contacts))
        elif command == "help" + end_of_command_marker:
            print(help())
        elif command in ["close" + end_of_command_marker, "exit" + end_of_command_marker]:
            print("[*] Good bye!")
            break
        else:
            print("[error] Invalid command.")


# Main function
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n[*] Good bye!')
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
