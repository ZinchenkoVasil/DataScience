#from .controllers import get_response
import uuid

def test_get_response():
    guid = str(uuid.uuid4())
    password = 'Admin'
    assert get_response(guid, password, "test")[0] == 200