"""Unit tests for ViewModel.py"""
import pytest

from todo_app.ViewModel import ViewModel
from todo_app.data.Item import Item

# @pytest.fixture
# def viewModel(items):
#     return ViewModel(items)

# class Test_ViewModel:
    # @pytest.mark.parametrize('items',[Item(id=1, title='TDD Test', status='Not started')])
# def test_can_get_todo_items(self, viewModel):
#     assert viewModel.items.id == 1

    # @pytest.mark.parametrize('items',[Item(id=1, title='TDD Test', status='Not started'), Item(id=2, title='TDD Test', status='Not started')])
def test_get_todo_items():
    items = [
                Item(id=1, title='TDD Test', status='Todo'), 
                Item(id=2, title='TDD Test', status='Todo'),
            ]
    todo_items_list = ViewModel(items,'writer').todo_items
    assert len(todo_items_list) > 0
    for item in todo_items_list:
        assert item.status == 'Todo'

def test_get_done_items():
    items = [
                Item(id=1, title='TDD Test', status='Done'), 
                Item(id=2, title='TDD Test', status='Done'),
            ]
    done_items_list = ViewModel(items,'writer').done_items
    assert len(done_items_list) > 0
    for item in done_items_list:
        assert item.status == 'Done'

def test_get_doing_items():
    items = [
                Item(id=1, title='TDD Test', status='Doing'), 
                Item(id=2, title='TDD Test', status='Doing'),
            ]
    doing_items_list = ViewModel(items,'writer').doing_items
    assert len(doing_items_list) > 0
    for item in doing_items_list:
        assert item.status == 'Doing'
def test_writer_role():
    items = [
                Item(id=1, title='TDD Test', status='Doing'), 
                Item(id=2, title='TDD Test', status='Doing'),
            ]
    current_user_role = ViewModel(items,'writer').user_role
    assert current_user_role == 'writer'

def test_reader_role():
    items = [
                Item(id=1, title='TDD Test', status='Doing'), 
                Item(id=2, title='TDD Test', status='Doing'),
            ]
    current_user_role = ViewModel(items,'reader').user_role
    assert current_user_role == 'reader'