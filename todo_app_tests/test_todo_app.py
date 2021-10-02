"""Integration tests for todo.py"""

import pytest
from todo_app import app
from dotenv import find_dotenv, load_dotenv
from unittest.mock import patch, Mock
from todo_app_tests.app_fixtures import trello_board_response, trello_lists_response, trello_get_card_list

@pytest.fixture 
def client():
    # Use our test integration config instead of the 'real' version 
    try:
        file_path = find_dotenv('.env.test')
        load_dotenv(file_path, override=True)
    except OSError:
        print(".env file not found")

    with patch('requests.get') as mock_get_requests:
        mock_get_requests.side_effect = mock_get_lists
        
        # Create the new app. 
        test_app = app.create_app()

        # Use the app to create a test_client that can be used in our tests.
        with test_app.test_client() as client: 
            yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Study' in response.data.decode()


def mock_get_lists(url, params):
    if url == 'https://api.trello.com/1/members/me/boards':
        response = Mock()
        response.json.return_value = trello_board_response
        response.return_value.status_code = 200
        return response
    elif url == 'https://api.trello.com/1/boards/60a2de5a87ca081037632fc2/lists':
        response = Mock()
        # sample_trello_lists_response should point to some test response data
        response.json.return_value = trello_lists_response
        return response
    elif url == 'https://api.trello.com/1/boards/60a2de5a87ca081037632fc2/cards':
        response = Mock()
        # sample_trello_lists_response should point to some test response data
        response.json.return_value = trello_get_card_list
        return response

    return None