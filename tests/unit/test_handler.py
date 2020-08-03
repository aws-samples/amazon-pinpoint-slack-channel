import json
import os
import pytest
from pinpoint_slack_channel import app

ROOT_DIR = os.path.abspath(os.curdir)

@pytest.fixture()
def pinpoint_event():

    """ Generates A Pinpoint Event"""
    with open(os.path.join(ROOT_DIR, 'events/event.json')) as json_file:
        return json.load(json_file)

def test_lambda_handler(pinpoint_event):
    
    assert pinpoint_event
    response_obj = app.lambda_handler(pinpoint_event, "")
    assert response_obj['statusCode'] == 200