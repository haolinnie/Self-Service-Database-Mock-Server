"""
Utility stuff
"""
from flask import jsonify

# TODO: Database mixin class
# TODO: More


def check_sql_safe(*argv):
    for arg in argv:
        if " " in arg or ";" in arg or "," in arg or "--" in arg:
            return False
    return True


def create_response(data=None, status=200, message=""):
    """Wrapper function to make API responses consistent :)

    Data must be a dictionary
        key: type of data
        value: data
    
    :param data <dict> optional data
    :param status <int> optional status code (defaults to 200)
    :param message <str> optional message
    :returns tuple (<Flask Response>, <int>)
    """

    if type(data) is not dict and data is not None:
        raise TypeError("data must be a dictionary!")

    response = {"success": 200 <= status < 300, "message": message, "result": data}
    return jsonify(response), status


def exception_handler(error):
    """Catch all exceptions
    :param Exception
    :returns Tuple(<Flask Response>, <int>)
    """
    return create_response(message=str(error), status=500)

