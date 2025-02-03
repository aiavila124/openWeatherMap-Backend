from Classes.Login import Login
from Utils.Authorizer import response_format

@response_format
def get_token(event, context):
    class_ = Login()
    methods = {
        "POST": class_.get_token,
    }
    method_to_run = methods[event['httpMethod']]
    return method_to_run(event)
