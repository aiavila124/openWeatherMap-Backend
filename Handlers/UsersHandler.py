from Classes.Users import Users
from Utils.Authorizer import response_format, authorizer

@response_format
def users(event, context):
    class_ = Users()
    methods = {
        "POST": class_.create_user
    }
    method_to_run = methods[event['httpMethod']]
    return method_to_run(event)

@authorizer
def get_user_data(event, context):
    class_ = Users()
    methods = {
        "GET": class_.get_user_data
    }
    method_to_run = methods[event['httpMethod']]
    return method_to_run(event)
