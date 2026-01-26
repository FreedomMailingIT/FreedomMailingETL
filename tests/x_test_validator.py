"""Class use experiment."""

from dataclasses import dataclass
from typing import Annotated

from app_modules.validator import Base


@dataclass
class Person(Base):
    """Filtered person data from source and output to <filename>.json."""
    name: Annotated[str, 'req; maximum length 30; multi word; title']
    age: Annotated[int, 'req; range 18 thru 65']
    gender: Annotated[str, 'req; [Male|Female]']
    hobby: Annotated[str, 'req; multiple word']
    other: Annotated[str, 'required; vldtr validate_other']
    another: Annotated[str, 'opt; vldtr validate_another']
    email: Annotated[str, 'optional; valid email'] = None

    def __init__(self, initial_data: dict):
        super().__init__(self, initial_data)
        self.custom_validators = {'validate_others': self.validate_other}

    def validate_other(self, field, value):
        """Validate data given in other."""
        _ = field
        if not value:
            raise ValueError

    def validate_another(self, field, value):
        """Validate data given in other."""
        _ = field
        if 'test' not in value:
            raise ValueError('validate_another() reports "test" not in value given.')


inputd = {
    'name': 'Gregory J Baker',
    'age': 75,
    'gender': 'male',
    'hobby': 'computer programming, flying',
    'email': 'gjbaker@usa.com',
    'other': 'anything right now',
    'another': 'some more stuff'
    }
person = Person(inputd)
print('*****************************')
print(person.name)
