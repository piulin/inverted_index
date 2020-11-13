
import re


def tokenize(text: str):
    """
    Tokenize a text.
    :param text:
    :return: tokens of the text
    """


    space_splits = re.findall(r"[\w']+", text)

    return space_splits


def normalize(tokens):
    """
    normalize tokens. TODO.
    :param tokens:
    :return:
    """

    return list(set(tokens))
