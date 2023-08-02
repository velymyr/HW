from collections import UserDict
from collections.abc import Iterator
from datetime import datetime, date
import re
import pickle
import csv


class Field:
    def __init__(self, value) -> None:
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value):
        pass

    def __str__(self) -> str:
        return self.value


class Name(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.value = value

    def __str__(self) -> str:
        return self.value


class Phone(Field):
    def __init__(self, phone: str) -> None:
        super().__init__(phone)
        self._value = phone

    def __str__(self) -> str:
        return self._value

    @property
    def phone(self):
        return self._value

    @phone.setter
    def phone(self, phone_number):
        self.validate(phone_number)
        self._value = phone_number

    def validate(self, value):
        # +380441234567; +38(044)1234567; +38(044)123-45-67; 0441234567;
        # 044-123-4567; (073)123-4567; (099)123-4567
        regex = r"^(?:\+38)?(?:\(\d{3}\)[0-9]{3}-?[0-9]{2}-?[0-9]{2}|0\d{2}-?[0-9]{3}-?[0-9]{2}-?[0-9]{2})$"
        if not re.findall(regex, value, re.M):
            print("Invalid phone number format")
            raise ValueError


class Birthday(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        date_format = "%Y-%m-%d"
        try:
            birthdate = datetime.strptime(str(value), date_format).date()
            self.__value = birthdate
        except:
            self.__value = None
            print('Wrong format. Enter date in format "%Y-%m-%d"')
            raise ValueError

    def __str__(self):
        return self.__value.strftime("%Y-%m-%d")


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthdate: Birthday = None) -> None:
        self.name = name
        self.phones = [] if phone else None
        if phone:
            self.phones.append(phone)
        self.birthdate = birthdate

    def add_phone(self, phone: Phone):
        if self.phones is None:
            self.phones = []
        self.phones.append(phone)

    def add_phones(self, phones):
        if self.phones is None:
            self.phones = phones
            return
        for phone in phones:
            self.phones.append(phone)

    def remove_phone(self, phone: Phone):
        if phone not in self.phones:
            raise ValueError(
                f"The phone number '{phone.phone}' is not listed in the records.")
        self.phones.remove(phone)

    def update_phone(self, old_phone: Phone, new_phone: Phone):
        try:
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone
        except ValueError:
            raise ValueError(
                f"The phone number '{old_phone.phone}' is not listed in the records.")

    def add_birthday(self, birthdate: Birthday):
        self.birthdate = birthdate

    def days_to_birthday(self):
        current_date = date.today()
        birthday_this_year = date(
            current_date.year, self.birthdate.phone.month, self.birthdate.phone.day)
        birthday_next_year = date(
            current_date.year + 1, self.birthdate.phone.month, self.birthdate.phone.day)
        delta = (birthday_this_year - current_date).days

        if delta >= 0:
            return delta
        else:
            return (birthday_next_year - current_date).days

    def __str__(self) -> str:
        phones = "; ".join(str(p)
                           for p in self.phones) if self.phones else "not added"
        bd = self.birthdate if self.birthdate else "----------"
        return f"Name: {self.name},\tPhone numbers: {phones},\tBirthday: {bd}"

    def __repr__(self) -> str:
        return str(self)


class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, record: Record):
        key = record.name.value
        self.data[key] = record

    def __iter__(self, n=1):
        self._index = 0
        self._items = list(self.data.values())
        self._step = n
        return self

    def __next__(self):
        if self._index < len(self._items):
            item = self._items[self._index]
            self._index += self._step
            return item
        else:
            raise StopIteration

    def save_to_file_pickle(self, file_path):
        with open(file_path, "wb") as fh:
            pickle.dump(self.data, fh)

    def load_from_file_pickle(self, file_path):
        with open(file_path, "rb") as fh:
            data = pickle.load(fh)
            self.data.update(data)

    def save_to_file(self, file_path):
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            print(self.data)
            for rec in self.data.values():
                print(rec)
                name = rec.name.value
                phones = [phone.value for phone in rec.phones]
                birthday = rec.birthdate.value.strftime(
                    "%Y-%m-%d") if rec.birthdate else ""
                writer.writerow([name, "|".join(phones), birthday])

    def load_from_file(self, file_path):
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)


if __name__ == "__main__":
    ad = AddressBook()
    ad.load_from_file("data.csv")
