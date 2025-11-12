import connexion
import six

from swagger_server.models.body1 import Body1  # noqa: E501
from swagger_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from swagger_server.models.inline_response4002 import InlineResponse4002  # noqa: E501
from swagger_server.models.inline_response401 import InlineResponse401  # noqa: E501
from swagger_server import util


def login_post(body):  # noqa: E501
    """Log in a user

    This endpoint authenticates a user based on username and password.&lt;br/&gt; # noqa: E501

    :param body: User credentials needed for login.
    :type body: dict | bytes

    :rtype: InlineResponse2003
    """
    if connexion.request.is_json:
        body = Body1.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
