## Error classes created with Exception inheritance to handle input values (used when validating name and number formats)
class Name_Error1(Exception):
    pass
class Name_Error2(Exception):
    pass
class Number_Error(Exception):
    pass
class Double_Error(Exception):
    pass

def parse_input(user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

## Handler function for possible error scenarios
def input_error(func):
    def inner(args, contacts):
        try:
            return func(args, contacts)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found. Please enter an existing contact."
        except IndexError: 
            return "Invalid input detected, please try again. Expected input: phone [name]"
        except Name_Error1:
            return "Name is not correct, must contain characters only.\Expected input: phone [name]"
        except Name_Error2:
            return "Name is not correct, must contain characters only.\nExpected input: name and phone number."
        except Number_Error:
            return "Number is not correct, must contain digits only.\nExpected input: name and phone number."
        except Double_Error:
            return "Invalid input, provide name with characters only and number with digits only.\nExpected input: name and phone number"
    return inner

## Separate handler function for method change_contact, where ValueError must return a specific message different from the one defined above
def input_change_contact_error(func):
    def inner(args, contacts):
        try:
            return func(args, contacts)
        except ValueError:
            return "Invalid input. Please provide: change [name] [new phone number]"
    return inner

## Function used in add_contact, change_contact and show_phone methods for a validation purpose for name and phone numbers formats
def validate_input_content(args):
    if len(args) == 2:
        if not args[0].isalpha() and not args[1].isdigit():
            raise Double_Error
        elif not args[1].isdigit():
            raise Number_Error  
        elif not args[0].isalpha():
            raise Name_Error2
    elif len(args) ==1:
        if not args[0].isalpha():
            raise Name_Error1
    return args

## add contact function with a decorator to handle errors in the add contact operations
@input_error
def add_contact(args, contacts):
    if len(args) < 2:
        raise ValueError
    validate_input_content(args)
    name, phone = args
    contacts[name] = phone
    return "Contact updated."

## change contact function wrapped with two decorators to handle errors in the change contact operations
@input_error 
@input_change_contact_error
def change_contact(args, contacts):
    validate_input_content(args)
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    else:
        raise KeyError

## show contact function wrapped with a decorator to handle errors in the show/display contact operation
@input_error
def show_phone(args, contacts):
    validate_input_content(args)
    name = args[0]
    return f"The phone number for {name} is: {contacts[name]}"

## show all contacts function
def show_all(contacts):
    if not contacts:
        return "No contacts found."
    result = ""
    for name, phone in contacts.items():
        result += f"{name}: {phone}\n"
    return result.strip()

## main function where the infinite loop is created for continuous interaction between user and CLI
def main():
    contacts = {}
    print("Welcome to the assistant bot! Please type Hello to continue")
    while True:
        user_input = input("Enter a command: ")
        if not user_input:
            print('Please type a valid command or exit to close.')
            continue
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print(
            """
            How can I help you?
            Please choose from the following options:
            ** Add a new contact                       >>> add [name] [phone]
            ** Change an existing contact              >>> change [name] [new phone number]
            ** Display number for an existing contact  >>> phone [name]
            ** Display all contacts from the phonebook >>> all
            ** Exit the application                    >>> close or exit
            """)
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()