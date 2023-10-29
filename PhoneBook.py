from collections import defaultdict
from datetime import datetime, timedelta

# The base class for record fields.
class Field:
    # class initialization
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Class for storing a contact name
class Name(Field):
    pass

# Class for storing a phone number
class Phone(Field):
    # class initialization
    def __init__(self, value):
        if not self.is_valid_phone(value):
            raise ValueError("Invalid phone number format. Must be 10 digits.")
        super().__init__(value)

    # returns a static method for the `is_valid_phone(phone)` method function
    # function for phone number validation
    @staticmethod
    def is_valid_phone(phone):
        return len(phone) == 10 and phone.isdigit()

class Birthday(Field):
    # class initialization
    def __init__(self, value):
        if not self.is_valid_birthday(value):
            raise ValueError("Incorrect date of birth format. It should be in the format DD.MM.YYYY")
        super().__init__(value)

    # returns a static method for the `is_valid_birthday(birthday)` method function
    # function of validating the date of birth
    @staticmethod
    def is_valid_birthday(birthday):
        try:
            datetime.strptime(birthday, '%d.%m.%Y')
            return True
        except ValueError:
            return False

# Class for storing contact information, including name and phone list
class Record:
    # class initialization
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = str()

    # function of adding a phone number
    def add_phone(self, phone):
        if not any(p.value == phone for p in self.phones):
            self.phones.append(Phone(phone))

    # phone number deletion function
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    # function of editing a phone number
    def edit_phone(self, old_phone, new_phone):
        if Phone.is_valid_phone(new_phone):
            for phone in self.phones:
                if phone.value == old_phone:
                    phone.value = new_phone
                    break
        else:
            raise ValueError("Invalid phone number format. Must be 10 digits.")

    # phone number search function
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    # function to return the phone number(s)
    def get_phones(self):
        return f"{'; '.join(str(p) for p in self.phones)}"

     # function of adding a birthday
    def add_birthday(self, birthday):
        if not self.birthday: self.birthday = Birthday(birthday)

    # function to return the phone number
    def show_birthday(self):
        return self.birthday

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {self.birthday.value}"

# Class for storing and managing records
class AddressBook:
    # class initialization
    def __init__(self):
        self.data = {}

    # function of adding a record
    def add_record(self, record):
        self.data[record.name.value] = record

    # record search function
    def find(self, name):
        return self.data.get(name)

    # record deletion function
    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self, users):
        birthday_dict = defaultdict(list)
        today = datetime.today().date()

        for user in users:
            name = user["name"]
            birthday = user["birthday"].date()
            birthday_this_year = birthday.replace(year=today.year)

            delta_days = (birthday_this_year - today).days

            if delta_days < 7:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                delta_days = (birthday_this_year - today).days

            day_of_week = (today + timedelta(days=delta_days)).strftime("%A")
            birthday_dict[day_of_week].append(name)

        for day, names in birthday_dict.items():
            print(f"{day}: {', '.join(names)}")

