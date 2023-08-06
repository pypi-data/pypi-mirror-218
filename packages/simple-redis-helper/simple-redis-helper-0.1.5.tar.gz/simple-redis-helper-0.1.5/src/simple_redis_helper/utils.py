import os


def has_password(ns):
    """
    Checks the namespace whether a password has been supplied either directly or via environment variable.
    Direct password takes precedence over environment variable.

    :param ns: the namespace to check
    :return: True if a password has been supplied
    :rtype: bool
    """
    if hasattr(ns, "password"):
        if ns.password is not None:
            return True

    if hasattr(ns, "password_env"):
        if ns.password_env is not None:
            if os.getenv(ns.password_env) is not None:
                return True

    return False


def get_password(ns):
    """
    Returns the password from the namespace (supplied either directly or via environment variable).
    Direct password takes precedence over environment variable.

    :param ns: the namespace to use
    :return: the password if one has been supplied, otherwise None
    :rtype: str
    """
    if hasattr(ns, "password"):
        if ns.password is not None:
            return ns.password

    if hasattr(ns, "password_env"):
        if ns.password_env is not None:
            if os.getenv(ns.password_env) is not None:
                return os.getenv(ns.password_env)

    return None
