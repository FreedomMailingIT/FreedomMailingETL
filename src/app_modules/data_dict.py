"""A dataclass created from a dictionary to create dotted dictionary."""


from dataclasses import dataclass


@dataclass
class Record:
    """Class to hold address record data."""
    def __init__(self, **kwargs):
        self.elements = []
        for key, val in kwargs.items():
            setattr(self, key, val)
            self.elements.append(key)

    def __repr__(self):
        return '\n'.join([
            f'{attr}: {self.__getattribute__(attr)}' for attr in self.elements
            ]) + '\n'

    def get_elements(self):
        """Return a list of elements created in __init__."""
        return '\n'.join(self.elements)
