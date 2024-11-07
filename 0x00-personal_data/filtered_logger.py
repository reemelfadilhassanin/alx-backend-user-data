#!/usr/bin/env python3
"""
Function to obfuscate specified fields in a log
message using a regular expression.
"""

from typing import List
import re
import logging
from os import environ
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Returns a log message obfuscated """
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """ Returns a Logger Object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Returns a connector to a MySQL database """
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    # Debugging print statements to ensure
    # the environment variables are correct
    print(f"DB Username: {username}")
    print(f"DB Password: {password}")
    print(f"DB Host: {host}")
    print(f"DB Name: {db_name}")

    if not db_name:
        raise ValueError("Database name (PERSONAL_DATA_DB_NAME) is not set!")

    try:
        # Create a connection to the database
        cnx = mysql.connector.connect(user=username,
                                      password=password,
                                      host=host,
                                      database=db_name)
        return cnx
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit(1)  # Exit the program if there's a connection error


def main():
    """
    Obtain a database connection using get_db and retrieves all rows
    in the users table and display each row under a filtered format
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [i[0] for i in cursor.description]

    logger = get_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.info(str_row.strip())

    cursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filters values in incoming log records using filter_datum """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        # Debugging: Print the formatted message
        print(f"Formatted message: {record.msg}")
        return super(RedactingFormatter, self).format(record)


if __name__ == '__main__':
    main()
