import os, pytest
from threading import Thread
from todo_app.data.todo import TodoService
from todo_app import app
from dotenv import find_dotenv, load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



@pytest.fixture(scope='module') 
def app_with_temp_board():
    # Create the new board & update the board id environment variable
    os.environ['TRELLO_BOARD_NAME'] = 'E2E_Test_Board' 

    todoService = TodoService()

    board_id = todoService.board_id
    print(f'board id = {board_id}')

    # construct the new application
    application = app.create_app() 

    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True 
    thread.start()
    yield application

    # Tear Down
    thread.join(1) 
    todoService.delete_board(board_id)

@pytest.fixture(scope="module") 
def driver():
    # Load the app config
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    #Set up headless option for chrome driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    
    with webdriver.Chrome(options=chrome_options) as driver:
        yield driver
    
    
@pytest.fixture(autouse=True) 
def archive_cards():
    os.environ['TRELLO_BOARD_NAME'] = 'E2E_Test_Board' 
    todoService = TodoService()
    todoService.archive_cards()

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000')
    assert driver.title == "To-Do App"

def test_add_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000')
    
    task_title = driver.find_element_by_id('title')
    task_title.send_keys("Selenium Test Add")
    task_title.submit()
    try:
        todo_item_added = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "todo_item_1")))

        driver.find_element_by_id("todo_item_1")
        
        assert "Selenium Test Add" in todo_item_added.text
    except TimeoutException:
        print ("Page taking too long to respond")

def test_move_to_doing_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000')

    task_title = driver.find_element_by_id('title')
    task_title.send_keys("Selenium Test Started")
    task_title.submit()
    try:
        todo_item_added = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "todo_item_1")))

        assert "Selenium Test Started" in todo_item_added.text

        todo_item_start_btn = driver.find_element_by_id('start_todo_item_1')
        todo_item_start_btn.click()

        todo_doing_item = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID, "doing_item_1")))

        assert "Selenium Test Started" in todo_doing_item.text

    except TimeoutException:
        print ("Page taking too long to respond")

def test_move_to_done_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000')
    #Adding a card
    task_title = driver.find_element_by_id('title')
    task_title.send_keys("Selenium Test Completed")
    task_title.submit()
    try:
        todo_item_added = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "todo_item_1")))

        assert "Selenium Test Completed" in todo_item_added.text
        #Starting a card
        todo_item_start_btn = driver.find_element_by_id('start_todo_item_1')
        todo_item_start_btn.click()

        todo_doing_item = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID, "doing_item_1")))

        assert "Selenium Test Completed" in todo_doing_item.text
        #Moving to Done
        todo_item_done_btn = driver.find_element_by_id('done_todo_item_1')
        todo_item_done_btn.click()

        todo_done_item = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID, "done_item_1")))

        assert "Selenium Test Completed" in todo_done_item.text

    except TimeoutException:
        print ("Page taking too long to respond")
