# Imports Contents from a specific repo as reminders.

import requests

from .reminders import reminder
from .utilities import parser


def gitContents(prompt: list[str]) -> tuple[bool, list[reminder]]:
    """
    Returns a list of contents from a GitHub repo as reminders.
    """

    _, sdOpts, ddOpts = parser(prompt)

    try:
        assert "r" in sdOpts
        assert isinstance(sdOpts["r"], str)
        assert "/" in sdOpts["r"] and len(sdOpts["r"]) >= 3

        if "u" in sdOpts:
            assert isinstance(sdOpts["u"], str)
            assert len(sdOpts["u"])

        repo = sdOpts["r"]
        content = "pulls" if "pulls" in ddOpts else "issues"

        url: str = "https://api.github.com/repos/{}/{}"
        url = url.format(repo, content)

        contents: list = requests.get(url).json()

        # contents might be of type 'dict' on errors.
        assert isinstance(contents, list)

    except:  # This should be avoided.
        return False, []

    reminders: list[reminder] = []

    for content in contents:
        gitContent: dict[str, str] = {}
        gitContent["title"] = content["title"]
        gitContent["description"] = repo

        if "u" not in sdOpts:
            reminders.append(reminder(gitContent, True))

        # Checks assignee or requested reviewer on pulls.
        else:
            gitContent["description"] += ":" + sdOpts["u"]
            search = content["assignees"]

            if "pulls" in ddOpts:
                search += content["requested_reviewers"]

            if sdOpts["u"] in [user["login"] for user in search]:
                reminders.append(reminder(gitContent, True))

    return True, reminders
