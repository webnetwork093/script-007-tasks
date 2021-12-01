import os
import pytest

from server import FileService

main_dir = os.path.join(os.getcwd(), "fortest")
print(os.getcwd())

@pytest.fixture(scope='function')  # Fixture
def file_creation(request):
    print('file_creation START...')
    FileService.create_file(filename=os.path.join(main_dir, "test_ok.txt"))

## change dir

def test_change_dir_autocreate_true():
    path = os.path.join(main_dir, "abcd")
    FileService.change_dir(path=path, autocreate=True)
    assert os.getcwd() == os.path.normpath(path)



def test_change_dir_autocreate_false(path=os.path.join(main_dir, "abcdf")):
    with pytest.raises(RuntimeError):
        FileService.change_dir(path=path, autocreate=False)

## get files

def test_get_files():
    f = FileService.get_files()
    assert isinstance(f, list)

## get file data

def test_get_file_data_runtime_error():
    filename = os.path.join(main_dir, "test_no_file.txt")
    with pytest.raises(RuntimeError):
        FileService.get_file_data(filename=filename, get_content=True)

def test_get_file_data_value_error():
    filename = os.path.join(main_dir, "te?st.txt")
    with pytest.raises(ValueError):
        FileService.get_file_data(filename=filename, get_content=True)

def test_get_file_data_all_ok():
    filename = os.path.join(main_dir, "test.txt")
    stat = FileService.get_file_data(filename=filename, get_content=True)
    assert isinstance(stat, dict)
    assert "name" in stat
    assert "content" in stat
    assert "create_date" in stat
    assert "edit_date" in stat
    assert "size" in stat

## write file data

def test_create_file_value_error():
    filename = os.path.join(main_dir, "te?st.txt")
    with pytest.raises(ValueError):
        FileService.create_file(filename=filename, content="test content 123")

def test_create_file_all_ok():
    filename = os.path.join(main_dir, "test_ok.txt")
    stat = FileService.create_file(filename=filename, content="test content 123")
    assert isinstance(stat, dict)

## delete file

def test_delete_file_runtime_error():
    filename = os.path.join(main_dir, "test_no_file.txt")
    with pytest.raises(RuntimeError):
        FileService.get_file_data(filename=filename, get_content=True)

def test_delete_file_value_error():
    filename = os.path.join(main_dir, "te?st.txt")
    with pytest.raises(ValueError):
        FileService.delete_file(filename=filename)

@pytest.mark.usefixtures('file_creation')
def test_delete_file_all_ok(filename=os.path.join(main_dir, "test_ok.txt")):
    FileService.delete_file(filename=filename)
