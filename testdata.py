import csv
import random
from faker import Faker
from datetime import datetime


def generate_phone_number():
    # Generate a random Ukrainian phone number
    prefix = "+380"
    operator_codes = ["66", "67", "68", "96",
                      "97", "98", "50", "66", "95", "99"]
    random_operator = random.choice(operator_codes)
    random_number = ''.join(random.choices("0123456789", k=7))
    phone = f"{prefix}{random_operator}{random_number}"

    if random.randint(1, 13) % 3 == 0:
        random_operator = random.choice(operator_codes)
        random_number = ''.join(random.choices("0123456789", k=7))
        phone2 = f"{prefix}{random_operator}{random_number}"
        return f"{phone}|{phone2}"
    else:
        return phone



def generate_csv_file(filename, num_records):
    fake = Faker("uk_UA")

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Phone', 'Birthdate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # writer.writeheader()
        for _ in range(num_records):
            full_name = fake.first_name()
            name_surname = ' '.join(full_name.split()[:2])
            phone_number = generate_phone_number()
            birthdate = fake.date_between_dates(date_start=datetime(
                1970, 1, 1), date_end=datetime(1999, 12, 31))

            writer.writerow({
                'Name': name_surname,
                'Phone': phone_number,
                'Birthdate': birthdate,
            })


if __name__ == "__main__":
    num_records = 20

    generate_csv_file("data.csv", num_records)

    print(
        f"CSV file 'data.csv' with {num_records} records has been generated.")
