import connexion
import six

from swagger_server.models.body import Body  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.inline_response201 import InlineResponse201  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.inline_response4001 import InlineResponse4001  # noqa: E501
from swagger_server.models.inline_response404 import InlineResponse404  # noqa: E501
from swagger_server import util


def books_get():  # noqa: E501
    """Get a list of all books

    Returns a complete list of all books in the library.&lt;br/&gt; # noqa: E501


    :rtype: List[InlineResponse200]
    """
    return 'do some magic!'


def books_id_borrow_post(id):  # noqa: E501
    """Borrow an available book

    Marks a book as &#39;unavailable&#39; (borrowed). Requires &#39;user&#39; or &#39;admin&#39; role.&lt;br/&gt; # noqa: E501

    :param id: The ID of the book to borrow.
    :type id: int

    :rtype: InlineResponse2001
    """
    return 'do some magic!'


def books_id_get(id):  # noqa: E501
    """Get a single book by ID

    Returns details for a specific book.&lt;br/&gt; # noqa: E501

    :param id: The ID of the book to retrieve.
    :type id: int

    :rtype: InlineResponse200
    """
    return 'do some magic!'


def books_id_return_post(id):  # noqa: E501
    """Return a borrowed book

    Marks a book as &#39;available&#39; (returned). Requires &#39;user&#39; or &#39;admin&#39; role.&lt;br/&gt; # noqa: E501

    :param id: The ID of the book to return.
    :type id: int

    :rtype: InlineResponse2002
    """
    return 'do some magic!'


def books_post(body):  # noqa: E501
    """Add a new book (Admin only)

    Creates a new book and adds it to the library. Requires admin privileges.&lt;br/&gt; # noqa: E501

    :param body: The book to create.
    :type body: dict | bytes

    :rtype: InlineResponse201
    """
    if connexion.request.is_json:
        body = Body.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
