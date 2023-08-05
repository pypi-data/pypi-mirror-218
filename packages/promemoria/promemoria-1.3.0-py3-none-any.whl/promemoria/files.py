# Handles promemoria files.

import pickle
from os import makedirs
from os.path import expanduser

from .reminders import reminder


def getReminders() -> list[reminder]:
    """
    Returns reminders from ~/.promemoria/reminders.pickle
    """

    # Creates or checks reminders' folder.
    global path
    path = expanduser("~") + "/.promemoria/"
    makedirs(path, exist_ok=True)

    # Loads reminders.
    try:
        file = open(path + "reminders.pickle", "rb")

        reminders: list[reminder] = pickle.load(file)
        file.close()

        for rem in reminders:
            if not isinstance(rem, reminder):
                # Raises this error to recreate the file.
                raise FileNotFoundError

    except FileNotFoundError:
        reminders: list[reminder] = []

        saveReminders(reminders)

    except:
        reminders = []

    # Runs a check on reminders.
    for rem in reminders:
        rem.check()

    return reminders


def saveReminders(reminders: list[reminder]) -> None:
    """
    Saves reminders to ~/.promemoria/reminders.pickle
    """

    file = open(path + "reminders.pickle", "wb")
    pickle.dump(reminders, file)
    file.close()
