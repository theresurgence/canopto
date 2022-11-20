import logging

import httpx
import keyring
from bs4 import BeautifulSoup

from core.web import get_request, post_request
from ui.messages import print_authentication_error, print_request_error
from ui.tui import ask_save_credentials_prompt, get_credentials_prompt

CANVAS_URL = "https://canvas.nus.edu.sg/login/saml/103"
USER_IDENTIFIER_URL = "https://nus.vmwareidentity.asia/federation//auth/login/input/useridentifier"
AUTH_REQUEST_URL = "https://nus.vmwareidentity.asia/authcontrol/auth/request"
AUTHENTICATE_URL = "https://nus.vmwareidentity.asia/authcontrol/authenticate"
AUTH_RESP_INTERNAL_URL = "https://nus.vmwareidentity.asia/federation/auth/response/internal"
SAML_URL = 'https://canvas.nus.edu.sg/login/saml'


def get_credentials_from_keyring():
    try:
        username = keyring.get_password("canopto", "username")
        password = keyring.get_password("canopto", username)
        return username, password
    except keyring.errors.KeyringLocked:
        print("Cannot get saved credentials!")
        return None, None


def save_credentials_to_keyring(username: str, password: str):
    keyring.set_password("canopto", "username", username)
    keyring.set_password("canopto", username, password)


def logout_credentials_from_keyring():
    username = keyring.get_password("canopto", "username")
    if username:
        keyring.delete_password("canopto", username)
    keyring.delete_password("canopto", "username")

    return username


async def authenticate(username, password) -> None:
    """
    Retrieve authentication cookies from Canvas server.
    Cookies can be saved to a file and loaded to minimize the authentication
    process
    """

    # 1 Canvas Login portal
    res = await get_request(CANVAS_URL, follow_redirects=True)

    # 2 User Identifier
    context_id = BeautifulSoup(res.text, 'html.parser').find(
        'input', {'id': 'contextId'})['value']
    data = {'username': username, 'contextId': context_id}
    res = await post_request(USER_IDENTIFIER_URL, data)

    # 3 Auth Request
    data = {i['name']: i['value']
            for i in BeautifulSoup(res.text, 'html.parser').find_all('input')}
    res = await post_request(AUTH_REQUEST_URL, data)

    # 4 Authenticate with credentials
    context_id = BeautifulSoup(res.text, 'html.parser').find(
        'input', {'id': 'contextId'})['value']
    data = {'userInput': username,
            'password': password, 'contextId': context_id}
    res = await post_request(AUTHENTICATE_URL, data)

    # 5 Internal Authentication
    data = {i['name']: i['value']
            for i in BeautifulSoup(res.text, 'html.parser').find_all('input')}
    res = await post_request(AUTH_RESP_INTERNAL_URL,
                             data, follow_redirects=True)

    # 6 SAML (No need to follow_redirect)
    saml_data = BeautifulSoup(res.text, 'html.parser').form.get_text()
    data = {'SAMLResponse': saml_data}
    res = await post_request(SAML_URL, data)


async def authentication_loop():
    username, password = get_credentials_from_keyring()

    is_keyring_used = False
    if username is not None and password is not None:
        is_keyring_used = True

    while True:
        if username is None or password is None:
            username, password = await get_credentials_prompt()

        try:
            # Cookies for debugging
            # load_cookies('cookies.txt')
            await authenticate(username, password)
            # save_cookies('cookies.txt')

        except httpx.RequestError as exc:
            print_request_error()
            logging.error(f"An error occurred while requesting {exc.request.url!r}.")
            return False

        except httpx.HTTPStatusError as exc:
            print_authentication_error(exc.response.status_code)
            logging.error(f"Error {exc.response.status_code} while requesting {exc.request.url!r}.")
            username, password = None, None
            is_keyring_used = False  # time for user to enter credentials again

        except httpx.ConnectTimeout as exc:
            logging.error(f"{exc} Timeout error")
            return False

        else:
            if not is_keyring_used:
                if await ask_save_credentials_prompt():
                    save_credentials_to_keyring(username, password)
                    logging.info(f"Saved credentials to keyring")
            return True
