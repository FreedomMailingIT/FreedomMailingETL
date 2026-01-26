"""
A module to set class attributes from dict unknown size and only storing specified
elements and validating the data using annotations of the child class.
"""


from email.utils import parseaddr
from inspect import get_annotations
from typing import get_type_hints
import re


class Base:
    """Class to add dict values to child attribute & validate them."""

    def __init__(self, child, initial_data: dict):
        annotations = get_annotations(type(child))
        child.__dict__ = {key: val for key, val in initial_data.items() if key in annotations}
        out_type = re.findall(r"(json|csv|sql)[.\s\.]*", child.__doc__)[-1]
        validate_input(child, annotations)


def validate_input(child, annotations):
    """
    Validate the input using annotations for standard restrictions.

    Saves on boiler plate and repetative code in child class for common restrictions.
    Use cases can be explanded as desired.  If restrictions not handled here they
    should be handled in child class by a call to specific class methods.
    """
    # setup function calls for validations
    validate_functions = {
        'max': check_max,
        'range': check_range,
        'email': check_email,
        '|': check_options,
        'multi': check_for_multiple_words,
        'req': check_if_required,
        'title': check_for_title,
        'vldtr': call_child_validator
    }

    hints = get_type_hints(child)  # gives field type (int, str, ...)
    for field, annotation in annotations.items():  # both strings (sort of)
        annotation = str(annotation)
        meta = None if not annotation.startswith('typing') else annotation.split("'")[1]

        try:
            # preliminary system checks
            value = getattr(child, field)
            _check_attribute_type(field, value, hints[field])

            # developer specified checks
            restrictions = meta.split(';')  # separate multiple requirements
            for restriction in restrictions:
                restriction = restriction.strip()
                _validate_fields(child, field, value, restriction, validate_functions)
        except ValueError as e:
            restriction = restriction if not e.args else e.args[0]
            print(f'{field}: ({value}) failed requirement: {restriction}')
        except AttributeError as e:
            print(e)


def _check_attribute_type(field, value, hint_type):
    """Ensure data entered is the type specified in hint."""
    if value and not isinstance(value, hint_type):
        raise TypeError(f"{field}: {value} is not of type {hint_type}")


def check_if_required(value, meta):
    """Check if data required for attribute."""
    if meta and not value:
        raise ValueError


def _validate_fields(child, field, value, restriction, validate_functions):
    """Validate each field in input."""
    for key_word in validate_functions:  # pylint: disable=C0206:consider-using-dict-items
        if key_word in restriction:
            if key_word == 'vldtr':
                validate_functions[key_word](child, field, value, restriction)
            else:
                validate_functions[key_word](value, restriction)
            break


def call_child_validator(child, field, value, validator):
    """Calls method from child class."""
    method = getattr(child, validator.split()[1])
    method(field,value)


#******************* Annotation checks ******************

def check_max(value, meta):
    """Check max (one or more consecutive digits in meta string) requirement is met."""
    val = re.search(r"\s+(\d+)\s*", meta).group()
    if len(value) > int(val):
        raise ValueError


def check_range(value, meta):
    """Check range (two values of one or more digits in meta string) requirements met."""
    vals = re.findall(r"\s+(\d+)\s*", meta)
    if not int(vals[0]) <= value <= int(vals[1]):
        raise ValueError


def check_email(value, _):
    """Check valid email given."""
    _, addr = parseaddr(value)
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if value and not re.match(pattern, addr):
        raise ValueError


def check_options(value, meta):
    """Check that valid option given in the form [<option>|<option>...]."""
    cleaned_meta = meta.replace('[', '').replace(']', '').split('|')
    if value not in cleaned_meta:
        raise ValueError


def check_for_multiple_words(value, _):
    """Make sure data contains multiiple words."""
    if ' ' not in value:
        raise ValueError


def check_for_title(value, _):
    """Make sure data is of type title."""
    if not value.istitle():
        raise ValueError
