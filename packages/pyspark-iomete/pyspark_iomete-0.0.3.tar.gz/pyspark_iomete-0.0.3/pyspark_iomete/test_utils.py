import random
import string


def table_name_with_random_suffix(table_name):
    # add random suffix to table name to avoid conflicts
    random_suffix = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
    return table_name + random_suffix
