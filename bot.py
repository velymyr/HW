from address_book import AddressBook, Record, Name, Phone, Birthday
address_book = AddressBook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            print("Please provide the required input")
        except ValueError:
            print("Please enter valid input")
        except KeyError:
            print("Please enter valid name")
    return wrapper


@input_error
def add_contact(name, phone, birthday=None):
    name = Name(name.capitalize())
    phone = Phone(phone)
    if birthday:
        birthday = Birthday(birthday)
    rec = Record(name, phone, birthday)
    address_book.add_record(rec)
    return f"Add success {name} {phone}"


@input_error
def change_phone(name, old_phone, new_phone):
    name = Name(name.capitalize())
    record: Record = address_book.get(name.phone)
    if record is None:
        raise KeyError(f"{name} does not exist in phone book")
    old_phone = Phone(old_phone)
    new_phone = Phone(new_phone)
    record.update_phone(old_phone, new_phone)
    return f"Change success {name} {old_phone.phone} to {new_phone.phone}"


@input_error
def get_phone(*args):
    name = str.capitalize(args[0])
    user_phones_list = []
    for phone in address_book[name].phones:
        user_phones_list.append(phone)
    phone_list = ', '.join(user_phones_list).strip()
    return f"Name: {name} \tPhone numbers: {phone_list}"


@input_error
def remove_phone(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = address_book.get(name.phone)
    if rec:
        return rec.remove_phone(phone)
    else:
        raise ValueError


def show_all(*args):
    if address_book.data:
        return "\n".join(str(r) for r in address_book.data.values())
    else:
        return "Contact list is empty"


def exit(*args):
    return "Good bye!"


def hello(*args):
    return "How can I help you?"


def main():
    while True:
        user_input = input(">>> ")
        if user_input:
            command, data = parser(user_input)
            result = command(*data)
            if result:
                if result == "Good bye!":
                    print(result)
                    break
                print(result)
            continue
        else:
            print(no_command())


def no_command(*args, **kwargs):
    return "Unknown command"


COMMANDS = {
    hello: ("hello",),
    add_contact: ("add",),
    get_phone: ("phone",),
    change_phone: ("change",),
    remove_phone: ("remove",),
    show_all: ("show all",),
    exit: ("close", "exit", "good bye"),
}


@input_error
def parser(text: str) -> tuple[callable, tuple[str] | None]:
    for cmd, keywords in COMMANDS.items():
        for keyword in keywords:
            if text.lower().startswith(keyword):
                data = text[len(keyword):].strip().split()
                return cmd, data
    return no_command, []


def parserX(text: str) -> tuple[callable, tuple[str] | None]:
    lower_text = text.lower()

    if lower_text.startswith("add"):
        return add_contact, lower_text.replace("add", "").strip().split()
    elif lower_text.startswith("hello"):
        return hello, "How can I help you?"
    elif lower_text.startswith("close") or lower_text.startswith("exit") or lower_text.startswith("good bye"):
        return exit, "Good bye!"
    elif lower_text.startswith("show all"):
        return show_all, 'show all'
    elif lower_text.startswith("phone"):
        return get_phone, text.replace("phone", "").strip().split()
    elif lower_text.startswith("change"):
        return change_phone, text.replace("change", "").strip().split()
    else:
        return no_command, ''


if __name__ == "__main__":
    main()
