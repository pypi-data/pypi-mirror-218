#!/usr/bin/env python3


class KeyAlreadyExistsError(Exception):
    pass


class EntryNotFoundError(Exception):
    pass


class EntryExpiredError(Exception):
    pass
