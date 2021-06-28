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
    todo_items_list = ViewModel(items).todo_items
    assert len(todo_items_list) > 0

def test_get_done_items():
    items = [
                Item(id=1, title='TDD Test', status='Done'), 
                Item(id=2, title='TDD Test', status='Done'),
            ]
    done_items_list = ViewModel(items).done_items
    assert len(done_items_list) > 0

def test_get_doing_items():
    items = [
                Item(id=1, title='TDD Test', status='Doing'), 
                Item(id=2, title='TDD Test', status='Doing'),
            ]
    doing_items_list = ViewModel(items).doing_items
    assert len(doing_items_list) > 0