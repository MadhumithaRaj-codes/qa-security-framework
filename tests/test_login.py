from selenium import webdriver
from pages.login_page import LoginPage
import time


def test_login():

    driver = webdriver.Chrome()

    driver.get("http://127.0.0.1:5000")

    login = LoginPage(driver)

    login.enter_username("admin")
    login.enter_password("password123")
    login.click_login()

    time.sleep(2)

    assert "Login Successful" in driver.page_source

    driver.quit()