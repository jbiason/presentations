# -*- encoding: utf-8 -*-

"""Behave steps."""

import behave
import mainsource


@behave.given("that I have a username {name}")
def set_username(context, name):
    context.username = name
    return


@behave.given("that I have a password {password}")
def set_password(context, password):
    context.password = password
    return


@behave.when("I try to create an user")
def create_user(context):
    try:
        mainsource.create_user(context.username, context.password)
    except mainsource.UserCreationError as exc:
        context.last_exception = exc
    return


@behave.then("I should get an error of invalid password")
def is_invalid_password(context):
    assert hasattr(context, 'last_exception')
    assert isinstance(context.last_exception,
                      mainsource.PasswordIsNotStrongEnough)
