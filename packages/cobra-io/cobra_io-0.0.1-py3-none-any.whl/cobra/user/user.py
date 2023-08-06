import requests

from cobra.utils.urls import BASE_URL


_refresh_token = None


def login(e_mail: str) -> str:
    """
    Login to COBRA and return the access token.

    :param e_mail: The e-mail address of the user.
    :return: The access token.
    :note: May ask for the password if the refresh token is not available.
    """
    global _refresh_token
    if _refresh_token is not None:
        r_refresh = requests.post(BASE_URL + 'token/refresh/', data={'refresh': _refresh_token})
        if r_refresh.status_code == 200:
            return r_refresh.json()['access']
        # Fall through if refresh token is invalid.
    password = input("Please enter your password: ")
    r_login = requests.post(BASE_URL + 'token/', data={'email': e_mail, 'password': password})
    if r_login.status_code != 200:
        raise ValueError("Invalid credentials.")
    _refresh_token = r_login.json()['refresh']
    return r_login.json()['access']
