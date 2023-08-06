import cherrypy
import pytest

from turbogears import controllers, expose
from turbogears.testutil import make_app
from turbogears.rest import RESTContainer, RESTResource


def handle_resource_init_exception(traceback, message, status, version):
    """ While this function operates similarly to a regular error handler,
    it is not one. This catches an error at a different part of the workflow.
    Subsequently, this takes different arguments and may have different end
    results as well.
    """
    cherrypy.response.status = 418
    return 'teapot'


class Root(controllers.RootController):
    """The root controller of the application."""
    _cp_config = {
       'error_page.default': handle_resource_init_exception
    }

    def __init__(self):
        self.controller = AnyController()


@RESTContainer('AnyResource')
class AnyController(RESTResource):
    pass


class AnyResource(RESTResource):
    def __init__(self, id, parent_container=None):
        self.id = id
        if self.id == 'error':
            raise Exception('Error in resource init')

    @expose()
    def GET(self):
        return self.id.encode()


@pytest.fixture
def app():
    return make_app(Root)


def test_resource_init_exception_handling(app):
    response = app.get('/controller/no_error/')
    assert response.text == 'no_error'

    response = app.get('/controller/error/', status=418)
    assert response.text.strip() == 'teapot'

