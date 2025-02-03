from Classes.Resources import Resources
from Utils.Authorizer import authorizer


@authorizer
def cities(event, context):
    class_ = Resources()
    methods = {
        "GET": class_.get_cities
    }
    method_to_run = methods[event['httpMethod']]
    return method_to_run(event)


@authorizer
def countries(event, context):
    class_ = Resources()
    methods = {
        "GET": class_.get_countries
    }
    method_to_run = methods[event['httpMethod']]
    return method_to_run(event)


@authorizer
def states(event, context):
    class_ = Resources()
    methods = {
        "GET": class_.get_states
    }
    method_to_run = methods[event['httpMethod']]
    return method_to_run(event)


@authorizer
def icons(event, context):
    class_ = Resources()
    methods = {
        "GET": class_.get_icons
    }
    method_to_run = methods[event['httpMethod']]
    return method_to_run(event)
