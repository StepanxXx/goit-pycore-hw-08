"""Simple contact management assistant bot with basic CRUD operations."""

from address_book import AddressBook, Record
from input_error import input_error
import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

def parse_input(user_input):
    """Parse user input into command and arguments, converting command to lowercase."""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    """Add a new contact to the address book, checking for duplicates."""
    name, phone, *_ = args
    contact = book.find(name)
    message = "Contact updated."
    if contact is None:
        contact = Record(name)
        book.add_record(contact)
        message = "Contact added."
    if phone:
        contact.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    """Update the phone number for an existing contact."""
    name, old_phone, new_phone, *_ = args
    contact = book.find(name)
    if contact is None:
        return f'Contact "{name}" is not exists.'
    if contact.find_phone(old_phone) is None:
        return f'Phone "{old_phone}" is not exists.'
    contact.edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error
def show_phone(args, book: AddressBook):
    """Display the phone numbers for a specified contact."""
    name = args[0]
    contact = book.find(name)
    if contact is None:
        return f'Contact "{name}" is not exists.'
    if len(contact.phones) <= 0:
        return f'The contact "{name}" has no phones.'
    return "\n".join([str(phone) for phone in contact.phones])

@input_error
def show_all(book: AddressBook):
    """Format and return a list of all contacts and their phone numbers."""
    result = ""
    for contact in book.data.values():
        result += f"{contact.name}: {", ".join([str(phone) for phone in contact.phones])}\n"
    return result.strip()

@input_error
def add_birthday(args, book: AddressBook):
    """Add the birthday for an existing contact."""
    name, birthday, *_ = args
    contact = book.find(name)
    if contact is None:
        return f'Contact "{name}" is not exists.'
    contact.add_birthday(birthday)
    return "Contact birthday added."

@input_error
def show_birthday(args, book: AddressBook):
    """Display the birthday for a specified contact."""
    name = args[0]
    contact = book.find(name)
    if contact is None:
        return f'Contact "{name}" is not exists.'
    if contact.birthday is None:
        return 'Contact date of birth is not specified.'
    return str(contact.birthday)

@input_error
def show_birthdays(book: AddressBook):
    """Show birthdays that will occur within the next week."""
    result = ""
    for congratulation in book.get_upcoming_birthdays():
        result += f"{str(congratulation)}\n"
    return result.strip()

def main():
    """Address book assistant bot"""
    book = load_data()
    try:
        print("Welcome to the assistant bot!")
        while True:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break

            elif command == "hello":
                print("How can I help you?")

            elif command == "add":
                print(add_contact(args, book))

            elif command == "change":
                print(change_contact(args, book))

            elif command == "phone":
                print(show_phone(args, book))

            elif command == "all":
                print(show_all(book))

            elif command == "add-birthday":
                print(add_birthday(args, book))

            elif command == "show-birthday":
                print(show_birthday(args, book))

            elif command == "birthdays":
                print(show_birthdays(book))

            else:
                print("Invalid command.")
    finally:
        save_data(book)


if __name__ == "__main__":
    main()
    
