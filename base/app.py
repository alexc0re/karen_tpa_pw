from playwright.sync_api import Browser, expect
import logging as log
import json



class App_Object:

    def __init__(self, browser: Browser, url=''):
        self.base_url = url
        self.browser = browser
        self.context = self.browser.new_context()
        self.page = self.context.new_page()


    def open_tpa(self):
        self.page.goto(self.base_url, wait_until='load')


    def navigate_to(self, endpoint):
        self.page.goto(self.base_url + endpoint, wait_until='load')
        expect(self.page.locator(".toast-container .toast-error")).to_be_hidden()





