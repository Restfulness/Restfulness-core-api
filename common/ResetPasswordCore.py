from common.DbHandler import DbHandler

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

import random
import string


class ResetPasswordCore:
    """Core Functions of reseting user's password."""
    @staticmethod
    def get_8_digit_auth_code(username: str) -> str:
        """ Step 1: Start process of resetting password. Return hash format of
        user's ID + random generated 8 digit code."""
        id = DbHandler.get_user_id(username)
        if id is None:
            return "USER_NOT_FOUND"

        random_code = ResetPasswordCore.__generate_8_digit_code()
        ResetPasswordCore.__send_8_digit_code_to_users_email(
            username, random_code)

        return(ResetPasswordCore.__generate_hash_string(id, random_code))

    @staticmethod
    def get_password_reset_token(hashed_data: str, user_input: str) -> str:
        """ Step 2: Return token for reseting password if user inputed correct
        8 digit code."""
        try:
            user_id = ResetPasswordCore.__verify_user_input_with_hashed_data(
                hashed_data, user_input)
        except SignatureExpired:
            return('EXPIRED')
        except BadSignature:
            return('INVALID_TOKEN')

        if user_id == -1:
            return('INVALID_CODE')
        else:
            return(ResetPasswordCore.__generate_reset_password_token(user_id))

    @staticmethod
    def reset_password(reset_token: str, new_password: str) -> str:
        """ Step 3: Change user's password if the token for changing
        password is valid"""
        try:
            user_id = ResetPasswordCore.__validate_reset_password_token(
                reset_token)
        except SignatureExpired:
            return('EXPIRED')
        except BadSignature:
            return('INVALID_TOKEN')

        status = DbHandler.reset_user_forgotten_password(user_id, new_password)
        if status == 'OK':
            return('OK')
        else:
            return('FAILED')

    @staticmethod
    def __validate_reset_password_token(token: str) -> int:
        """ Return user's ID if reset password token is correct. """
        hash = Serializer('test')
        try:
            data = hash.loads(token)
        except SignatureExpired:
            raise
        except BadSignature:
            raise

        return(data['id'])

    @staticmethod
    def __verify_user_input_with_hashed_data(hashed_data: str,
                                             user_input: str) -> int:
        """ Verify if user's inputed 8 digit code is correct, if so,
        return users id."""
        hash = Serializer('test')
        try:
            data = hash.loads(hashed_data)
        except SignatureExpired:
            raise
        except BadSignature:
            raise

        if user_input == data['valid_code']:
            return(data['id'])
        else:
            return(-1)

    @staticmethod
    def __generate_reset_password_token(id: int) -> str:
        """ Generate the main token that reset user's password."""
        hash = Serializer('test', expires_in=300)
        return(
            str(
                hash.dumps({
                    'id': id
                }),
                'utf-8'
            )
        )

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
