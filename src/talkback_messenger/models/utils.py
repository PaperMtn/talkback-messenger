"""Utility functions for models."""

from typing import Dict


def validate_fields(instance: object, expected_types: Dict):
    """Utility function to validate fields of a dataclass.

    Args:
        instance: Dataclass instance
        expected_types: Dict of field name and expected type
    """
    for given_field, expected_type in expected_types.items():
        value = getattr(instance, given_field)
        if value is not None and not isinstance(value, expected_type):
            raise TypeError(
                f'{instance.__class__.__name__}: Expected {given_field} to be of '
                f'type {expected_type}, got {type(value)}')
