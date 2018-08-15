#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""This is a sample code that simulates a user being created."""

from __future__ import print_function

import argparse
import json

from collections import Counter
from unicodedata import category

LOWERCASE_CHARS = "Ll"
UPCASE_CHARS = "Lu"
NUMBERS = "Nd"


class UserCreationError(Exception):
    """Base class for all exceptions in this module."""
    pass


class PasswordIsNotStrongEnough(UserCreationError):
    """The password used is not strong enough."""
    pass


class UserAlreadyExists(UserCreationError):
    """The user already exists in the database."""
    pass


def password_is_strong(password):
    """Check if the password have enough strength."""
    number_of = Counter(category(ch) for ch in password)
    return (number_of[LOWERCASE_CHARS] >= 1 and
            number_of[UPCASE_CHARS] >= 2 and
            number_of[NUMBERS] >= 1 and
            len(password) >= 12)


def get_users():
    """Retrieve the list of users in the system."""
    data = {}
    try:
        with open('users.json') as origin:
            data = json.load(origin)
    except IOError:
        # File does not exist, so we just assume it's empty
        pass
    return data


def save_users(user_list):
    """Save the user list back to the 'database'."""
    with open('users.json', 'w') as target:
        json.dump(user_list, target)
    return


def create_user(user, password):
    """'Create' and user."""
    if not password_is_strong(password.decode('utf-8')):
        raise PasswordIsNotStrongEnough

    users = get_users()
    if user in users:
        raise UserAlreadyExists

    users[user] = password
    save_users(users)
    return


def main():
    """Expose the functions back in command line options."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user',
                        dest='user',
                        help='Username to be created',
                        required=True)
    parser.add_argument('-p', '--password',
                        dest='password',
                        help='Password for the user',
                        required=True)
    args = parser.parse_args()
    try:
        create_user(args.user, args.password)
    except PasswordIsNotStrongEnough:
        print("That password is not strong enough")
    except UserAlreadyExists:
        print("Username already used")
    else:
        print("User created")
    return


if __name__ == "__main__":
    main()
