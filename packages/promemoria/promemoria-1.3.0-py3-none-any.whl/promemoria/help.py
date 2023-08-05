# promemoria's help

from colorama import Fore, Style


def helpMain() -> str:
    """
    Returns the help string.
    """
    spaces = " " * 4
    introduction: str = "Base commands."
    introduction += "\n" + "-" * len(introduction)

    # Empty command.
    cmd: str = Style.BRIGHT + "promemoria " + Style.RESET_ALL
    cmd += Style.DIM + "Shows the list of active reminders." + Style.RESET_ALL

    cmd += "\n" + spaces + Style.BRIGHT + "--all " + Style.RESET_ALL
    cmd += Style.DIM + "Shows every reminder." + Style.RESET_ALL

    # new.
    cmdNew: str = Style.BRIGHT + "promemoria new " + Style.RESET_ALL
    cmdNew += Style.DIM + "Creates a new reminder" + Style.RESET_ALL

    cmdNew += "\n" + spaces + Fore.RED + Style.BRIGHT + "-t " + Style.RESET_ALL
    cmdNew += Style.DIM + "title, string." + Style.RESET_ALL

    cmdNew += "\n" + spaces + Style.BRIGHT + "-de " + Style.RESET_ALL
    cmdNew += Style.DIM + "description, string. " + Style.RESET_ALL

    cmdNew += "\n" + spaces + Style.BRIGHT + "-da " + Style.RESET_ALL
    cmdNew += Style.DIM + "date, string, ISO 8601 compliant." + Style.RESET_ALL

    cmdNew += "\n" + spaces + Style.BRIGHT + "-ti " + Style.RESET_ALL
    cmdNew += Style.DIM + "time, string." + Style.RESET_ALL

    cmdNew += "\n" + spaces + Style.BRIGHT + "-p " + Style.RESET_ALL
    cmdNew += Style.DIM + "priority, integer, [1-3]." + Style.RESET_ALL

    # delete.
    cmdDelete: str = Style.BRIGHT + "promemoria delete " + Style.RESET_ALL
    cmdDelete += Style.DIM + "Deletes the specified reminder" + Style.RESET_ALL

    cmdDelete += "\n" + spaces + Fore.RED + Style.BRIGHT + "-i " + Style.RESET_ALL
    cmdDelete += Style.DIM + "index, integer." + Style.RESET_ALL

    # toggle.
    cmdToggle: str = Style.BRIGHT + "promemoria toggle " + Style.RESET_ALL
    cmdToggle += Style.DIM + "Toggles the specified reminder" + Style.RESET_ALL

    cmdToggle += "\n" + spaces + Fore.RED + Style.BRIGHT + "-i " + Style.RESET_ALL
    cmdToggle += Style.DIM + "index, integer." + Style.RESET_ALL

    # clear.
    cmdClear: str = Style.BRIGHT + "promemoria clear " + Style.RESET_ALL
    cmdClear += Style.DIM + "Deletes every reminder" + Style.RESET_ALL

    # GitHub integration.
    introductionGit: str = "GitHub integration."
    introductionGit += "\n" + "-" * len(introductionGit)

    # git.
    cmdGit: str = Style.BRIGHT + "promemoria gh " + Style.RESET_ALL
    cmdGit += (
        Style.DIM + "Imports issues and pull requests from GitHub" + Style.RESET_ALL
    )

    cmdGit += "\n" + spaces + Fore.RED + Style.BRIGHT + "-r " + Style.RESET_ALL
    cmdGit += Style.DIM + "public repo, string [user/repo]." + Style.RESET_ALL

    cmdGit += "\n" + spaces + Style.BRIGHT + "-u " + Style.RESET_ALL
    cmdGit += Style.DIM + "user, string." + Style.RESET_ALL

    cmdGit += "\n" + spaces + Style.BRIGHT + "--pulls " + Style.RESET_ALL
    cmdGit += Style.DIM + "Imports pull requests instead of issues." + Style.RESET_ALL

    # Full help.
    entries: list[str] = [introduction, cmd, cmdNew, cmdDelete, cmdToggle, cmdClear]

    # GitHub integration.
    entries += [introductionGit, cmdGit]

    return "\n\n".join(entries)


def helpChecker() -> str:
    """
    Returns the help string.
    """
    spaces = " " * 4
    introduction: str = "Base commands."
    introduction += "\n" + "-" * len(introduction)

    # Empty command (auto).
    cmd: str = Style.BRIGHT + "promemoria-check " + Style.RESET_ALL
    cmd += Style.DIM + "Checks for expired reminders." + Style.RESET_ALL

    # Enable command.
    cmdEnable: str = Style.BRIGHT + "promemoria-check enable " + Style.RESET_ALL
    cmdEnable += Style.DIM + "Enables the auto-checker." + Style.RESET_ALL

    # Disable command.
    cmdDisable: str = Style.BRIGHT + "promemoria-check disable " + Style.RESET_ALL
    cmdDisable += Style.DIM + "Disables the auto-checker." + Style.RESET_ALL

    # Full help.
    entries: list[str] = [introduction, cmd, cmdEnable, cmdDisable]

    return "\n\n".join(entries)
