import os
import sys
from PhoneBook import AddressBook, Record


# Function decorator for validating function arguments
def validate_args(expected_arg_count, command_example):
    def decorator(func):
        def wrapper(*args):
            if len(args[0]) != expected_arg_count:
                return (
                    "{:<7} {:<34} {}".format(
                        '[error]',
                        "Invalid command format. Please use:",
                        command_example))
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
        return ("{:<7} {}".format('[error]', ve))
    else:
        return ("{:<7} {}".format('[ok]', 'Contact added.'))


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
            return ("{:<7} {}".format('[error]', ve))
        else:
            return ("{:<7} {}".format('[ok]', 'Contact updated.'))
    else:
        return ("{:<7} {}".format('[info]', 'Contact not found.'))


# Function for processing the "phone" command
@validate_args(1, 'phone [name]')
def show_phone(args, contacts):
    name = args[0]
    record = contacts.find(name)
    if record is not None:
        phone = record.get_phone()
        if phone is not None:
            return ("{:<7} {:<6} {}".format('[ok]', 'Phone:', phone))
        else:
            return (
                "{:<7} {:<6}".format(
                    '[info]',
                    'This user does not have a phone number'))
    else:
        return ("{:<7} {}".format('[info]', 'Contact not found.'))


# Function for processing the "all" command
def show_all(contacts):
    if contacts:
        return "\n".join(["{:<7} {:<1} {}".format('[ok]', '-', single_record)
                         for _, single_record in contacts.data.items()])
    else:
        return ("{:<7} {}".format('[info]', 'No contacts.'))


# Function for processing the "add-birthday" command
@validate_args(2, 'add-birthday [name] [birthday]')
def add_birthday(args, contacts):
    try:
        name, birthday = args
        record = Record(name)
        record.add_birthday(birthday)
        contacts.add_record(record)
    except ValueError as ve:
        return ("{:<7} {}".format('[error]', ve))
    else:
        return ("{:<7} {}".format('[ok]', 'Birthday added.'))


# Function for processing the "show-birthday" command
@validate_args(1, 'show-birthday [name]')
def show_birthday(args, contacts):
    name = args[0]
    record = contacts.find(name)
    if record is not None:
        birthday = record.show_birthday()
        if birthday is not None:
            return ("{:<7} {:<9} {}".format('[ok]', 'Birthday:', birthday))
        else:
            return (
                "{:<7} {}".format(
                    '[info]',
                    'This user has no record of their birthday'))
    else:
        return ("{:<7} {}".format('[info]', 'Contact not found.'))


# Function for processing the "birthdays" command
def show_next_week_birthdays(contacts):
    if contacts:
        return contacts.get_birthdays_per_week()
    else:
        return ("{:<7} {}".format('[info]', 'No contacts.'))


# Function of displaying information about available commands
def help():
    help = "You can use the following commands: hello, add, change, phone, all, close, exit, help"
    return ("{:<7} {}".format('[info]', help))


# The main function for user interaction
def main():
    contacts = AddressBook()

    print("{:<7} {}".format('[*]', 'Welcome to the assistant bot!'))

    while True:
        # 'end_of_command_marker' -- this is a solution to distinguish between commands that share a common prefix.
        # For example, the commands 'add' and 'add-birthday'.
        end_of_command_marker = '_eocm_'
        try:
            user_input = input("{:<7} {}".format('[*]', 'Enter a command: '))
            command, *args = user_input.split()
            command = command.strip().lower() + end_of_command_marker
        except (ValueError, EOFError):
            continue
        if command == "hello" + end_of_command_marker:
            print("{:<7} {}".format('[*]', 'How can I help you?'))
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
            print("{:<7} {}".format('[*]', 'Good bye!'))
            break
        else:
            print("{:<7} {}".format('[error]', 'Invalid command.'))


# Main function
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("{:<7} {}".format('\n[*]', 'Good bye!'))
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
