from Utils.Tools.TypingTools import EventType
from Utils.Response import ApiResponse
from Helpers.GeneralTools import get_input_data, get_token_data, verify_password
from Utils.Tools.ValidationTools import validate_field
from Helpers.ProcessSql import ProcessSql
from Helpers.BasicHelper import BasicHelper
from Models.UsersModel import UsersModel
import Schemas.LoginSchemas as LoginSchemas
from http import HTTPStatus

class Login:
    def __init__(self):
        self.schemas = LoginSchemas
        self.process_sql = ProcessSql()
        self.helper = BasicHelper()

    def get_token(self, event: EventType)->ApiResponse:
        """
        Handles the retrieval of a user's token.

        Args:
            event (EventType): The event object containing request data which contains
                the user's email and password.

        Returns:
            ApiResponse: The response object containing the status code and user's token.
        """
        request = get_input_data(event)
        validate_field(self.schemas.Login(), request)

        user_data = self.helper.validate_if_does_not_exist(
            model=UsersModel,
            request={'email': request['email']},
            message="Incorrect credentials."
        )[0]

        verify_password(request['password'], user_data['password'])


        token = get_token_data(request['email'], user_data['user_id'])

        return ApiResponse(
            status_code=HTTPStatus.OK,
            data={'token': token}
        )
