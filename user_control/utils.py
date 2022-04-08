from datetime import date


def calculate_age(born):
    """
    Calculate age from date of birth
    :param born: date of birth
    :return: age
    """
    today = date.today() 
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day)) 
