"""
time.py
=======
This module provides functions for working with dates and time.

Variables:
    - months: A list of month names.

Functions:
    - get_date: Returns the current date in the format "MM/DD/YYYY".
    - get_month: Returns the current month index and name.
    - get_year: Returns the current year as an integer.
"""

from datetime import datetime, date

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ]

def get_date():
    """
    Returns the current date in the format "MM/DD/YYYY".

    Returns:
        str: The current date in the format "MM/DD/YYYY".

    Example:
        >>> get_date()
        '07/02/2023'
    """
    today = date.today()
    d = today.strftime("%m/%d/%Y")
    return d


def get_month():
    """
    Returns the current month index and name.

    Returns:
        list: A list containing the current month index (0-11) and name.

    Example:
        >>> get_month()
        [6, 'July']
    """
    month_index = datetime.now().month - 1
    return [month_index, months[month_index]]


def get_year():
    """
    Returns the current year as an integer.

    Returns:
        int: The current year.

    Example:
        >>> get_year()
        2023
    """
    return int(datetime.now().year)
