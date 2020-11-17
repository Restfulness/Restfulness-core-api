from common.DbHandler import DbHandler

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

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

        return(ResetPasswordCore.__generate_hash_string(id, random_code))

    @staticmethod
    def get_password_reset_token(hashed_data: str, user_input: str) -> str:
        """ Return token for reseting password if user inputed correct
        8 it code."""
        user_id = ResetPasswordCore.__verify_user_input_with_hashed_data(
            hashed_data, user_input)
        print(user_id)
        # TODO: This function should be completed

    @staticmethod
    def __verify_user_input_with_hashed_data(hashed_data: str,
                                             user_input: str) -> int:
        """ Verify if user's inputed 8 digit code is correct, if so,
        return users id."""
        s = Serializer('test')
        try:
            data = s.loads(hashed_data)
        except SignatureExpired:
            return 'EXPIRED'
        except BadSignature:
            return 'INVALID'

        return(data['id'])

    @staticmethod
    def __generate_hash_string(id: int, random_code: str) -> str:
        """ Create a hash that contains (user's ID and valid
        random created 8 digit code) which expires in 300 seconds."""
        hash = Serializer('test', expires_in=300)
        return(
            str(
                hash.dumps({
                    'id': id,
                    'valid_code': random_code
                }),
                'utf-8'
            )
        )

    @staticmethod
    def __send_8_digit_code_to_users_email(username: str, random_code: str):
        """ Send random generated password to user's email."""
        # TODO: Implement sending email part
        pass

    @staticmethod
    def __generate_8_digit_code() -> str:
        """ For generating random 8 digit of integers."""
        result_str = ''.join(
            random.choice(string.digits) for i in range(8)
        )
        return result_str
