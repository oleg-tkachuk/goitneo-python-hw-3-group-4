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
def show_all(_, contacts):
    if len(contacts.data.items()) !=0:
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
def help(*_):
    help = "You can use the following commands: hello, add, change, phone, all, close, exit, help"
    return ("{:<7} {}".format('[info]', help))


# Greeting display function
def hello(*_):
    return "{:<7} {}".format('[*]', 'How can I help you?')

# Function of generating the KeyboardInterrupt interrupt for exit
def exit(*_):
    raise KeyboardInterrupt


# Command mapping
commands = {
    'add': add_contact,
    'change': change_contact,
    'phone': show_phone,
    'all': show_all,
    'add-birthday': add_birthday,
    'show-birthday': show_birthday,
    'birthdays': show_next_week_birthdays,
    'help': help,
    'hello': hello,
    'exit': exit,
    'close': exit
}

# The main function for user interaction
def main():
    contacts = AddressBook()

    print("{:<7} {}".format('[*]', 'Welcome to the assistant bot!'))

    while True:
        try:
            user_input = input("{:<7} {}".format('[*]', 'Enter a command: '))
            parts = user_input.strip().split()
            try:
                command = parts[0].lower()
                args = parts[1:]
            except IndexError:
                continue
            if command in commands:
                result = commands[command](args, contacts)
                print(result)
            else:
                print("{:<7} {}".format('[error]', 'Invalid command.'))
        except (ValueError, EOFError):
            continue


# Main function
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("{:<8} {}".format('\n[*]', 'Good bye!'))
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
