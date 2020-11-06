
"""
The util module contains miscellaneous
tools used internally.
"""


def ask_yn_q(question):
    """
    Prints the question and loops until the user has
    typed "yes" or "no" to answer the question.
    Returns True if the user typed "yes".
    """
    question = question+' '
    resp = input(question).strip().lower()
    while resp[0] != 'y' and resp[0] != 'n':
        print("Please answer 'yes' or 'no' ('y' and 'n' are also accepted)")
        resp = input(question).strip().lower()
    # True if 'y' False if 'n'
    return resp[0] == 'y'

