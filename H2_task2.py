from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):

    @staticmethod
    def phone_validation(phone):
        if not phone.isdigit():                 # Validate the string contains only digits
            return False, 'Phone number is not valid. It must contain numbers only.'
        elif len(phone) != 10:                  # Validate the phone number has the correct length
            return False, 'Phone number is not valid. Please provide a number with 10 digits.'
        return True, phone
            
class Record:
    def __init__(self, name, *phones):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):                 # adding a phone number in the object record
        valid, msg = Phone.phone_validation(phone)
        if valid:
            self.phones.append(Phone(phone))
        else:
            print(msg)
    def edit_phone(self, old_phone, new_phone): # search and edit a phone number in the object record
        for i in self.phones:
            if i.value == old_phone:
                index = self.phones.index(i)
                self.phones[index] = Phone(new_phone)
                break
    def find_phone(self, phone_number):  
        for i in self.phones:                   # search for a phone number of the object record
            if i.value == phone_number:
                return i.value
        return None
    def remove_phone(self, phone_number):       # search and delete a specific number of the object record
        for i in self.phones:
            if i.value == phone_number:
                self.phones.remove(i)
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):               # adding the record to the address book
        self.data[record.name.value] = record
    def find(self, name):                       # finding and returning a record from the address book
        if name in self.data:
            return self.data[name]
        else:
            return None, 'Person is not in the Address book'
    def delete(self, name):                     # deleting a record from address book
        if name in self.data:
            del self.data[name]
        else:
            return 'Person is not in the address book'
        
##################### Code verification block #####################
        
    # Creation of a new address book 
book = AddressBook()

    # Creation of a entry for John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

    # Add a John entry to the address book
book.add_record(john_record)

    # Creating and adding a new entry for Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

    # Displaying all entries in the contact list
for name, record in book.data.items():
    print(record)

    # Find and edit a phone number for John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

    # Displaying: Contact name: John, phones: 1112223333; 5555555555
print(john) 

    # Searching for a specific phone number in John's entry
found_phone = john.find_phone('5555555555')
print(f"{john.name}: {found_phone}")  

    # Deletion: 5555555555
john.remove_phone(found_phone)
print(john)

    # Deletion Jane's entry
book.delete("Jane")