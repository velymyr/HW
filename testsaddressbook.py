import unittest
from address_book import Name, Phone, Record, AddressBook


class TestRecord(unittest.TestCase):
    def setUp(self):
        self.name = Name("JohnDoe")
        self.phone1 = Phone("1234567890")
        self.phone2 = Phone("9876543210")
        self.record = Record(self.name, self.phone1)

    def test_add_phone(self):
        self.record.add_phone(self.phone2)
        self.assertEqual(self.record.phones, [self.phone1, self.phone2])

    def test_remove_phone_valid(self):
        self.record.remove_phone(self.phone1)
        self.assertEqual(self.record.phones, [])

    def test_remove_phone_invalid(self):
        with self.assertRaises(ValueError):
            self.record.remove_phone(self.phone2)

    def test_update_phone_valid(self):
        new_phone = Phone("9999999999")
        self.record.update_phone(self.phone1, new_phone)
        self.assertEqual(self.record.phones, [new_phone])

    def test_update_phone_invalid(self):
        new_phone = Phone("5555555555")
        with self.assertRaises(ValueError):
            self.record.update_phone(new_phone, new_phone)


class TestAddressBook(unittest.TestCase):
    def setUp(self):
        self.addressbook = AddressBook()
        self.name = Name("JohnDoe")
        self.phone = Phone("1234567890")
        self.record = Record(self.name, self.phone)

    def test_add_record(self):
        self.addressbook.add_record(self.record)
        self.assertEqual(self.addressbook.data, {self.name.phone: self.record})


if __name__ == "__main__":
    unittest.main()
