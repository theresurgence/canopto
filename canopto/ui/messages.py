from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style

from canopto.core.config import get_download_dir, is_download_dir_valid

STYLE = Style.from_dict({
    'error': 'fg:#ff0066',
    'warning': 'fg:ansiyellow',
    'info': 'fg:ansibrightblue',
    'time': 'fg:orange',
    'underline': 'underline',
    'ub': 'underline bold',
    'cyan': 'fg: ansicyan',
    'strike': 'strike',
})


def print_request_error():
    msg = FormattedText([
        ('class:error', 'Connection Error. Please check your internet connection!')
    ])
    print_formatted_text(msg, style=STYLE)


def print_authentication_error(status_code):
    msg = FormattedText([
        ('class:error', f'Error {status_code}. Please check your username and password!')
    ])
    print_formatted_text(msg, style=STYLE)


def print_folder_warning():
    msg = FormattedText([
        ('class:warning', 'You have not chosen a folder to store your course files and videos.')
    ])
    print_formatted_text(msg, style=STYLE)
    print()


async def print_folder_notification():
    if await is_download_dir_valid():
        msg = FormattedText([
            ('', 'Folder to store files and videos: '),
            ('class:ansicyan', f'{get_download_dir()}'),
        ])
    else:
        msg = FormattedText([
            ('class:warning', 'You cannot download any files or videos until you choose a folder to store them.')
        ])
    print_formatted_text(msg, style=STYLE)
    print_formatted_text("")


def print_download_time(file_or_video, time_taken):
    msg = FormattedText([
        ('class:time', f'Finished downloading {file_or_video} in {time_taken}s.')
    ])
    print_formatted_text(msg, style=STYLE)


def print_download_time(file_or_video, time_taken):
    msg = FormattedText([
        ('class:time', f'Finished downloading {file_or_video} in {time_taken}s.\n')
    ])
    print_formatted_text(msg, style=STYLE)


def print_list_courses():
    msg = FormattedText([
        ('class:ub', 'You are taking the following courses:')
    ])
    print_formatted_text(msg, style=STYLE)


def print_faq():
    faq_text = HTML("""
<aaa bg='seagreen'><bold>FAQ</bold></aaa>
<underline>1. How are my login credentials stored?</underline>
Your username and password is stored locally and securely on your computer using the python keyring library.
For more information please check out: https://pypi.org/project/keyring/
Credentials are only used for authenticating with NUS Canvas servers.

<underline>2. Video downloads seem to take very long!</underline>
Videos can be large, and can easily be a few hundred MBs each. Please wait patiently.

<underline>3. If my download is interrupted, can I resume it?</underline>
Yes, you can end downloads abruptly and resume them at any time.
Partially downloaded files have a ".part" file extension, which will be removed
once the download is fully complete.

<underline>4. Will my annotated files be overwritten?</underline>
No, if the file has been full downloaded to your computer (no more ".part" extension), it will be ignored.

""")
    print_formatted_text(faq_text)
