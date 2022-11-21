from __future__ import unicode_literals

from prompt_toolkit import PromptSession
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import create_confirm_session
from prompt_toolkit.validation import Validator, ValidationError

from canopto.classes.menuoption import MenuOption
from canopto.core.config import is_download_dir_valid
from canopto.ui.messages import print_folder_notification


class BlankValidatorNoMessage(Validator):
    def validate(self, document):
        text = document.text

        if len(text) == 0:
            raise ValidationError()


class BlankValidatorWithMessage(Validator):
    def validate(self, document):
        text = document.text

        if len(text) == 0:
            raise ValidationError(message='Field cannot be blank!', cursor_position=0)


class OptionValidator(BlankValidatorNoMessage):
    def validate(self, document):
        super().validate(document)
        text = document.text

        if len(text) > 1 or not text.isdigit() or int(text) < 1 or int(text) > 5:
            raise ValidationError(message='Only numbers from 1-5 are allowed', cursor_position=0)


async def get_credentials_prompt():
    session = PromptSession()
    with patch_stdout():
        username = await session.prompt_async('Enter NUSNET ID (exxxxxxx): ', validator=BlankValidatorWithMessage())
        password = await session.prompt_async('Password: ', is_password=True, validator=BlankValidatorWithMessage())
    return username, password


async def ask_save_credentials_prompt():
    session = create_confirm_session("Do you want to save username and password on your computer?",
                                     suffix=" Press (y)es/(n)o: ")
    return await session.prompt_async(validator=BlankValidatorNoMessage())


bindings = KeyBindings()


@bindings.add(str(1))
def exit_with_value(event):
    event.app.exit(result=MenuOption.DL_ALL)


@bindings.add(str(2))
def exit_with_value(event):
    event.app.exit(result=MenuOption.DL_FILES)


@bindings.add(str(3))
def exit_with_value(event):
    event.app.exit(result=MenuOption.DL_VIDEOS)


@bindings.add(str(4))
def exit_with_value(event):
    event.app.exit(result=MenuOption.SEL_FOLDER)


@bindings.add(str(5))
def exit_with_value(event):
    event.app.exit(result=MenuOption.FAQ)


@bindings.add(str(6))
def exit_with_value(event):
    event.app.exit(result=MenuOption.LOGOUT)


@bindings.add(str(7))
def exit_with_value(event):
    event.app.exit(result=MenuOption.QUIT)


half_bindings = KeyBindings()


@half_bindings.add(str(4))
def exit_with_value(event):
    event.app.exit(result=MenuOption.SEL_FOLDER)


@half_bindings.add(str(5))
def exit_with_value(event):
    event.app.exit(result=MenuOption.FAQ)


@bindings.add(str(6))
def exit_with_value(event):
    event.app.exit(result=MenuOption.LOGOUT)


@half_bindings.add(str(7))
def exit_with_value(event):
    event.app.exit(result=MenuOption.QUIT)


async def select_option_prompt(courses):
    with patch_stdout():
        courses.list_courses()
        await print_folder_notification()
        print_formatted_text(HTML("<aaa bg='ansiblue' ><b>Select option number:</b></aaa>"))

        if await is_download_dir_valid():
            session = PromptSession(key_bindings=bindings, validator=OptionValidator())
            print_formatted_text(HTML("<aaa >1. Download all files + videos</aaa>"))
            print_formatted_text(HTML("<aaa >2. Download all files </aaa>"))
            print_formatted_text(HTML("<aaa >3. Download all videos</aaa>"))
        else:
            session = PromptSession(key_bindings=half_bindings, validator=OptionValidator())
            print_formatted_text(
                HTML("<aaa ><strike fg='ansibrightblack'>1. Download all files + videos</strike></aaa>"))
            print_formatted_text(HTML("<aaa ><strike fg='ansibrightblack'>2. Download all files</strike></aaa>"))
            print_formatted_text(HTML("<aaa ><strike fg='ansibrightblack'>3. Download all videos</strike></aaa>"))

        print_formatted_text(HTML("<aaa >4. Choose download folder</aaa>"))
        print_formatted_text(HTML("<aaa >5. FAQ</aaa>"))
        print_formatted_text(HTML("<aaa >6. Logout</aaa>"))
        print_formatted_text(HTML("<aaa >7. Quit</aaa>\n"))
        print_formatted_text(HTML("<aaa fg='yellow' >Ctrl-C to exit anytime</aaa>"))
        result = await session.prompt_async(editing_mode=False)
        return result
