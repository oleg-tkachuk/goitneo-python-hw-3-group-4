# The base class for record fields.
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Class for storing a contact name
class Name(Field):
    pass

# Class for storing a phone number
class Phone(Field):
    def __init__(self, value):
        if not self.is_valid_phone(value):
            raise ValueError("Invalid phone number format. Must be 10 digits.")
        super().__init__(value)

    # returns a static method for the `is_valid_phone(phone)` method function
    # function for phone number validation
    @staticmethod
    def is_valid_phone(phone):
        return len(phone) == 10 and phone.isdigit()

# Class for storing contact information, including name and phone list
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

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

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"

# Class for storing and managing records
class AddressBook:
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


# Create a new address book
#book = AddressBook()

# Create a record for John
#john_record = Record("John")
#john_record.add_phone("1234567890")
#john_record.add_phone("5555555555")

# Add a John entry to the address book
#book.add_record(john_record)

# Create a record for Jane
#jane_record = Record("Jane")
#jane_record.add_phone("9876543210")

# Add a Jane entry to the address book
#book.add_record(jane_record)

# Create a record for Alice
#alice_record = Record("Alice")
#alice_record.add_phone("2222222222")
#alice_record.add_phone("7777777777")
#alice_record.add_phone("8888888888")

# Add Alice entry to the address book
#book.add_record(alice_record)

# Display all records in the workbook
#for name, record in book.data.items():
#    print(record)

#  Find and edit a phone number for John
#john = book.find("John")
#john.edit_phone("1234567890", "1112223333")

#print(john)

# Search for a specific phone number in John's record
#found_phone = john.find_phone("5555555555")
#print(f"{john.name.value}: {found_phone}")

# Deleting a Jane record
#book.delete("Jane")

# Edit Alice phone number
#alice = book.find("Alice")
#alice.edit_phone("2222222222", "7878000000")

#print(alice)

# Display all records in the workbook
#for name, record in book.data.items():
#    print(record)
