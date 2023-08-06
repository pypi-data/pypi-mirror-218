import cherrypy
import pytest

from turbogears import controllers, expose
from turbogears.errorhandling import error_handler, exception_handler
from turbogears.testutil import make_app
from turbogears.rest import RESTContainer, RESTResource


# BaseException does not get caught by error/exception_handler.
# However, that is not a new behavior from COREBT-16020.
class TeapotError(Exception):
    pass


class HideError(Exception):
    pass


def exception_to_http_error(*args, **kw):
    tg_exception = args[-1]
    errors = {
        TeapotError: 418,
        HideError: 200
    }

    code = errors.get(type(tg_exception), 400)

    # Set the actual HTTP response
    cherrypy.response.status = code

    return f'status={code}'.encode()


class Root(controllers.RootController):
    """The root controller of the application."""

    def __init__(self):
        self.controller = AnyController()


@RESTContainer('AnyResource')
class AnyController(RESTResource):
    @expose()
    # We're using both `error_handler` and `exception_handler` because
    # exception_handler is currently not working, but it may be fixed
    # in the future.
    @error_handler(exception_to_http_error)
    @exception_handler(exception_to_http_error)
    def GET(self):
        raise HideError('pass')


class AnyResource(RESTResource):
    def __init__(self, id, parent_container=None):
        self.id = id

    @expose()
    def index(self, calling_function=None, **kw):
        if calling_function:
            return exception_to_http_error(HideError())
        else:
            return 'regular resource index'.encode()

    @expose()
    @error_handler(exception_to_http_error)
    @exception_handler(exception_to_http_error)
    def handle_exception(self):
        if self.id == 'teapot':
            raise TeapotError('teapot err')
        elif self.id == 'value':
            raise ValueError('value err')
        elif self.id == 'hide':
            raise HideError('value err')
        return self.id.encode()

    @expose()
    @error_handler(index)
    @exception_handler(index)
    def handle_exception_handle_in_class(self):
        if self.id == 'hide':
            raise HideError('pass')
        return self.id.encode()


@pytest.fixture
def app():
    return make_app(Root)


def test_resource_exception_hider(app):
    response = app.post('/controller/hide/handle_exception_handle_in_class')
    assert response.text == 'status=200'

    response = app.get('/controller/hide/handle_exception')
    assert response.text == 'status=200'


def test_resource_exception_raiser(app):
    app.get('/controller/value/handle_exception', status=400)
    app.put('/controller/teapot/handle_exception', status=418)
    response = app.get('/controller/no_error/handle_exception')
    assert response.text == 'no_error'


def test_controller_exception_hider(app):
    response = app.get('/controller')
    assert response.text == 'status=200'


def test_resource_no_exception(app):
    response = app.get('/controller/do_not/handle_exception')
    assert response.text == 'do_not'


def test_resource_index_still_works(app):
    response = app.put('/controller/any_id/')
    assert response.text == 'regular resource index'
