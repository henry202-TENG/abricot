from random import Random

def generate_random_string(string_len=16)-> str:
    """ To generate a random string of certain length.

    Args:
        string_len (int, optional): The length of string. Defaults to 16.

    Returns:
        str: A random string.
    """
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for _ in range(string_len):
        str+=chars[random.randint(0,length)]
    return str