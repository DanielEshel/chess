
def get_key(value, dictionary):
    """
    get key of a value in a dictionary
    :param value: value in dict
    :param dictionary: the dictionary
    :return: key if found, None if not found
    """
    for key in dictionary.keys():
        if dictionary[key] == value:
            return key


