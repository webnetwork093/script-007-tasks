import os
import pytest
from aiohttp import web
import requests
import server.FileService as FileService
from server.WebHandler import WebHandler
from server.Config import Config

config = Config().config

URL = 'http://' + config['host'] + ":" + config['port']
main_dir = os.getcwd()

## write file data

async def test_server_create_file_all_ok():

    response = requests.post(
                             url=f'{URL}/files',
                             json={'filename': "testFILE.txt", 'content': 'file content'},
    )

    #r_json = response.json()

    assert response.status_code == 200
    assert response.json().get('status') == 'success'

async def test_server_create_file_value_error():

    response = requests.post(
                             url=f'{URL}/files',
                             json={'filename': "test?FILE.txt", 'content': 'file content'},
    )

    assert response.status_code == 400
    assert response.json().get('status') == 'error'

async def test_server_delete_file_value_error():

    response = requests.delete(
                             url=f'{URL}/files/test!FILE.txt',
    )

    assert response.status_code == 400
    assert response.json().get('status') == 'error'

async def test_server_delete_file_ok():

    response = requests.delete(
                             url=f'{URL}/files/testFILE.txt',
    )

    assert response.status_code == 200
    assert response.json().get('status') == 'success'

async def test_server_get_files():

    response = requests.get(
                             url=f'{URL}/files',
    )

    assert response.status_code == 200
    assert response.json().get('status') == 'success'


@pytest.fixture(scope='function')  # Fixture
def file_creation(request):
    print('file_creation START...')
    FileService.create_file(filename=os.path.join(main_dir, "test_ok.txt"))

@pytest.mark.usefixtures('file_creation')
async def test_server_get_file_data():

    response = requests.get(
                             url=f'{URL}/files/test_ok.txt',
    )

    assert response.status_code == 200
    assert response.json().get('status') == 'success'
