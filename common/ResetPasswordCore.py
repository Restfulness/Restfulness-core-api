from common.DbHandler import DbHandler

import random
import string


class ResetPasswordCore:
    """Core Functions of reseting user's password."""
    @staticmethod
    def get_8_digit_auth_code(username: str) -> str:
        id = DbHandler.get_user_id(username)
        if id is None:
            return "USER_NOT_FOUND"

        random_code = ResetPasswordCore.__generate_8_digit_code()
        ResetPasswordCore.__send_8_digit_code_to_users_email(
            username, random_code)
        # TODO: Store 8-digit password

    @staticmethod
    def __send_8_digit_code_to_users_email(username: str, random_code: str):
        """ Send random generated password to user's email."""
        pass

    @staticmethod
    def __generate_8_digit_code() -> str:
        """ For generating random 8 digit of integers."""
        result_str = ''.join(
            random.choice(string.digits) for i in range(8)
        )
        return result_str
