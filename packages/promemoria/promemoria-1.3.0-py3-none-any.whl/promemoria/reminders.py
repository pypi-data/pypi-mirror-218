from __future__ import annotations

from datetime import datetime

from colorama import Fore, Style

from .utilities import parser, valiDate, msg


class reminder:
    def __init__(self: reminder, prompt: "list, dict", git: bool = False):
        if git:
            # Create a reminder from a git issue or pull request.
            # prompt: dict[str, str]

            self.title = prompt["title"]
            self.description = prompt["description"]

            self.priority = 2  # Default priority.
            self.date = ""
            self.time = ""

            # Flags.
            self.expired: bool = False
            self.dismissed: bool = False

        else:
            try:
                # Create a reminder 'from scratch'.
                # prompt: list[str]

                _, sdOpts, _ = parser(prompt)

                # Checks title.
                assert "t" in sdOpts

                # Title.
                self.title: str = sdOpts["t"]

                # Checks priority.
                if "p" in sdOpts:
                    assert isinstance(sdOpts["p"], int)
                    assert 1 <= sdOpts["p"] <= 3

                    # Priority.
                    self.priority: int = sdOpts["p"]

                else:
                    self.priority = 0

                # Checks description.
                if "de" in sdOpts:
                    assert isinstance(sdOpts["de"], str)

                    # Description.
                    self.description: str = sdOpts["de"]

                else:
                    self.description = ""

                # Checks date.
                if "da" in sdOpts:
                    assert isinstance(sdOpts["da"], str)
                    assert valiDate(sdOpts["da"])

                    # Date.
                    self.date: str = sdOpts["da"]

                else:
                    self.date = ""

                # Checks time.
                if "ti" in sdOpts:
                    assert isinstance(sdOpts["ti"], str)
                    assert valiDate(sdOpts["ti"], "%H:%M")

                    if not self.date:
                        self.date = datetime.now().strftime("%Y-%m-%d")

                    # Time.
                    self.time: str = sdOpts["ti"]

                else:
                    self.time = ""

                # Flags.
                self.expired: bool = False
                self.dismissed: bool = False
                self.confirmation: bool = True

                # Post-creation check.
                self.check()

                msg("Reminder created succesfully.")

            except AssertionError:
                msg("Reminder creation failed.", error=True)
                self.confirmation: bool = False

    def __str__(self: reminder, index: int = -1) -> str:
        # Mark.
        mark = "\u25cf " if self.dismissed else "\u25ef "

        if index != -1:
            mark += "[{}] ".format(index)

        # Lenght of 'mark' in spaces.
        spaces = len(mark) * " "

        # Title.
        # Striked on dismissed reminders.
        if self.dismissed:
            title = Style.DIM + self.title + Style.RESET_ALL

        else:
            title = Style.BRIGHT + self.title + Style.RESET_ALL

        string = mark + title

        # Priority.
        if self.priority:
            priority = " " + Fore.RED + "!" * self.priority + Fore.RESET

            string += priority

        # Description.
        if self.description:
            description = Style.DIM + self.description + Style.RESET_ALL

            string += "\n" + spaces + description

        # Date.
        if self.date or self.time:
            date: str = Fore.GREEN if not self.expired else Fore.RED
            date += self.date + "{}{}" + Fore.RESET
            date = date.format(" " if self.date else "", self.time)

            string += "\n" + spaces + date

        # Finally returns string.
        return string

    def check(self: reminder) -> None:
        if self.date:
            date = datetime.strptime(self.date, "%Y-%m-%d")

            if self.time:
                time = datetime.strptime(self.time, "%H:%M")

            now = datetime.now()

            # Checks expiration.
            if date < now:
                if self.time:
                    if time.hour <= now.hour and time.minute < now.minute:
                        self.expired = True

                    else:
                        self.expired = False

                else:
                    self.expired = True

            else:
                self.expired = False

    def toggle(self: reminder) -> None:
        """
        Toggles itself.
        """

        self.dismissed = not self.dismissed
