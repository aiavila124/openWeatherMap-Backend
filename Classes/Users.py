from Utils.Response import ApiResponse
from Models.UsersModel import UsersModel
from Utils.Tools.TypingTools import EventType
from Helpers.GeneralTools import get_input_data, hash_password
from Utils.Tools.ValidationTools import validate_field
import Schemas.UserSchemas as UserSchemas
from Helpers.ProcessSql import ProcessSql
from Helpers.BasicHelper import BasicHelper
from http import HTTPStatus

ACTIVE = 1

class Users:
    
    def __init__(self):
        self.schemas = UserSchemas
        self.process_sql = ProcessSql()
        self.bh = BasicHelper()

    def create_user(self, event: EventType) -> ApiResponse:
        """
        Handles the creation of a new user.

        Args:
            event (EventType): The event object containing request data which contains 
                the fields to create the new user data.

        Returns:
            ApiResponse: The response object containing the status code and user data.
        """
        request = get_input_data(event)

        validate_field(self.schemas.CreateUserSchema(), request)
        
        self.bh.validate_if_field_exists(
            UsersModel, 
            {'email': request['email']},
            value= "email"
        )

        request['password'] = hash_password(request['password'])

        new_user = self.process_sql.insert(
            model=UsersModel(**request),
        )

        return ApiResponse(
            status_code=HTTPStatus.CREATED,
            data={
                "user_id": new_user,
                **request
            }
        )

    def update_user(self, event: EventType)->ApiResponse:
        """
        Handles the update of a user.

        Args:
            event (EventType): The event object containing request data which contains 
                the fields to be updated.

        Returns:
            ApiResponse: The response object containing the status code and user data.
        """

        request = get_input_data(event)
        validate_field(self.schemas.UpdateUserSchema(), request)

        validate_id_data = [
            {
                "model": UsersModel,
                "id": request['user_id'],
                "name": 'user_id'
            }
        ]

        self.process_sql.validate_id(validate_id_data)

        self.bh.validate_if_field_exists(
            UsersModel, 
            {'email': request['email']},
            type_='update',
            user_id=request['user_id']
        )

        request['password'] = hash_password(request['password'])
   
        res = self.process_sql.update(
            model=UsersModel,
            conditions={
                'user_id': request['user_id']
            },
            values=request
        )

        return ApiResponse(
            status_code=HTTPStatus.CREATED,
            data=res
        )


    def delete_user(self, event: EventType)->ApiResponse:
        """
        Deletes a user from the database.

        Args:
            event (EventType): The event object containing request data which 
                contains the user ID.

        Returns:
            ApiResponse: The response object containing the status code and user data.
        """
        
        request = get_input_data(event)
        status_code = HTTPStatus.OK
        data=[]

        validate_field(self.schemas.DeleteUserSchema(), request)

        validate_id_data = [
            {
                "model": UsersModel,
                "id": request['user_id'],
                "name": 'user_id'
            }
        ]

        self.process_sql.validate_id(validate_id_data)

        res = self.process_sql.delete(
            model=UsersModel,
            conditions={
                'user_id': request['user_id']
            }
        )

        if not res:
            status_code = HTTPStatus.NOT_FOUND
            data='It was not possible to delete the user.'

        return ApiResponse(
            status_code=status_code,
            data=data
        )

    def get_user_data(self, event: EventType) -> ApiResponse:
        """
        Handles the retrieval of user data.

        Args:
            event (EventType): The event object containing request data which contains
                the parameters to filter the user data.

        Returns:
            ApiResponse: The response object containing the status code and user data.
        """
        user_id = event.get('user_id')

        users = self.process_sql.get_data(
            model=UsersModel,
            request={'user_id': user_id},
            all_columns_except=['password', 'active', 'created_at', 'updated_at']
        )

        status_code = HTTPStatus.OK
        if not users:
            status_code = HTTPStatus.NOT_FOUND

        return ApiResponse(
            data=users,
            status_code=status_code
        )
