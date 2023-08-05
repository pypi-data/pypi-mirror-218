![GitHub](https://img.shields.io/github/license/diantonioandrea/promemoria)

![PyPI](https://img.shields.io/pypi/v/promemoria?label=promemoria%20on%20pypi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/promemoria)
![PyPI - Downloads](https://img.shields.io/pypi/dm/promemoria)

![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/diantonioandrea/promemoria)
![GitHub last commit](https://img.shields.io/github/last-commit/diantonioandrea/promemoria)
![GitHub Release Date](https://img.shields.io/github/release-date/diantonioandrea/promemoria)

![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/diantonioandrea/promemoria/latest)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# [promemoria]

Intuitive Python based tool to create reminders in the shell.

**promemoria** is a Python based tool to help you stay organized and on top of your tasks! Quickly *create reminders in the shell* with the ability to *set a title, description, priority and date* to make sure you never forget anything.

## Main features

- Create and manage reminders directly from the shell.
- Import the latest *Issues* and *Pull Requests* as reminders from a public GitHub repository. ![New feature](https://img.shields.io/badge/new-green)
- Automatically checks for expired reminders when opening a new shell. ![New feature](https://img.shields.io/badge/new-green)

## Installation

**promemoria** can be installed from [PyPI](https://pypi.org) by:

```
python3 -m pip install --upgrade promemoria
```

## Usage

**promemoria** features a small and simple-to-use set of commands.  
These commands can be easily retrieved at any moment by issuing `promemoria help`[^1][^2][^3]

[^1]: Shouldn't `promemoria` work, try `python3 -m promemoria`.

[^2]: A color coded output will serve you better than this example.

[^3]: Referring to version 1.1.0

```
[promemoria]

Available commands.
-------------------

promemoria Shows the list of active reminders.
    --all Shows every reminder.

promemoria new Creates a new reminder
    -t title, string.
    -de description, string. 
    -da date, string, ISO 8601 compliant.
    -ti time, string.
    -p priority, integer, [1-3].

promemoria delete Deletes the specified reminder
    -i index, integer.

promemoria toggle Toggles the specified reminder
    -i index, integer.

promemoria clear Deletes every reminder

GitHub integration.
-------------------

promemoria gh Imports issues and pull requests from GitHub
    -r public repo, string [user/repo].
    -u user, string.
    --pulls Imports pull requests instead of issues.
```

## Expired reminders check

The automatic check can be enabled by issuing the following command[^4]:

[^4]: Linux and macOS only, bash and zsh only.

```
promemoria-check enable
```

## Examples

### Quickly check your reminders

```
promemoria
```

which results in:

```
[promemoria]

You have 1 reminder(s).
-----------------------

◯ [1] Go get some groceries. !
      2023-07-12 08:30
```

### Creating a reminder

```
promemoria new -t "Christmas" -de "It's Christmas\!" -da "2023-12-25" -p 3
```

which results in:

```
[promemoria]

Reminder created succesfully!
-----------------------------

◯ Christmas !!!
  It's Christmas!
  2023-12-25
```

### Import from a GitHub repository

```
promemoria gh -r "python/cpython" -u "sobolevn"
```

which results[^5] in:

[^5]: An example from the official [Python](https://github.com/python/cpython) repository.

```
[promemoria]

Imported 1 issue(s).
____________________

◯ New warning: "'_Py_IsInterpreterFinalizing' undefined; assuming extern returning in" !!
  https://api.github.com/repos/python/cpython/issues/106406
```

### Toggling a reminder

```
promemoria toggle -i 1
````

which results[^2][^6] in:

[^6]: The mark changes and the title gets dimmed.

```
[promemoria]

You toggled a reminder.
-----------------------

● Christmas !!!
  It's Christmas!
  2023-12-25
```