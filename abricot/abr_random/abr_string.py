""" random a string """
from random import Random

def generate_random_string(string_len=16, s_symbol=False)-> str:
    """ To generate a random string of certain length.

    Args:
        string_len (int, optional): The length of string. Defaults to 16.

    Returns:
        str: A random string.
    """
    return_str = ''
    special_symbol = '@#$%^&*!~?>:;'
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    if s_symbol:
        chars += special_symbol

    length = len(chars) - 1
    random = Random()
    for _ in range(string_len):
        return_str+=chars[random.randint(0,length)]
    return return_str
