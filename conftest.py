from playwright.sync_api import sync_playwright
from pytest import fixture
from base.app import App_Object
from pages.price_page import Price_page



@fixture(scope='session')
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope='session')
def get_browser(get_playwright):
    browser = get_playwright.chromium.launch(headless=True)
    yield browser
    browser.close()


@fixture(scope='function')
def app_obj(get_playwright, get_browser):
    app = App_Object(browser=get_browser, url='https://shop.perfumersapprentice.com/signin.aspx?returnurl=%2F')
    yield app

@fixture(scope='function')
def price_page(get_browser):
    price_page = Price_page(get_browser, url='https://shop.perfumersapprentice.com/signin.aspx?returnurl=%2F')
    yield price_page