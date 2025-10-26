import random
import time
import sys
from env_setup import Credentials
from base.app import App_Object
from pages.dict_compare import compare_and_format as fff
from sendtelegram.telegram import send_telegram
from database.mongodb import MongoConnection

aromas_db = MongoConnection()


def get_aroms_data_from_db():
    aromas_json = aromas_db.get_aroma_data_by_id()
    return aromas_json


class Price_page(App_Object):
    EMAIL_FIELD = "#Email"
    PASSWORD_FIELD = "#Password"
    LOGIN_BUTTON = ".page-action-bar .btn"
    ass = '623914148'
    AROMA_BLOCK = '.product-listing li'
    AROMA_NAME = '.product-listing li h2'
    aromas = {}

    def login(self):
        self.open_tpa()
        self.page.fill(self.EMAIL_FIELD, Credentials.APP_USERNAME)
        self.page.fill(self.PASSWORD_FIELD, Credentials.APP_PASSWORD)
        self.page.click(self.LOGIN_BUTTON)

    def get_aroms_data_from_db(self):
        aromas_json = aromas_db.get_aroma_data_by_id()
        return aromas_json

    def get_aromas(self):
        self.page.goto('https://shop.perfumersapprentice.com/c-84-bulk-sizes.aspx')
        aroma_blocks = self.page.locator(self.AROMA_BLOCK).all()
        for block in aroma_blocks:
            aroma_name = block.locator("h2").text_content()
            price_blocks = block.locator('.addtocart select option').all()
            prices = {}
            for price_block in price_blocks:
                aroma_size_and_price = price_block.text_content()
                aroma_price_index = aroma_size_and_price.find('$')
                aroma_size = aroma_size_and_price[0:15].strip()
                aroma_price = aroma_size_and_price[aroma_price_index:aroma_price_index + 6]
                if "Gallon" in aroma_size or "Case" in aroma_size or "Double" in aroma_size:
                    prices.update({aroma_size: [aroma_price]})
                if prices:
                    self.aromas.update({aroma_name: prices})

    def compare_dicts(self):
        message_string = ''
        messages_timeout = 0
        actual_dict = self.aromas
        expected_dict = self.get_aroms_data_from_db()
        try:
            expected_dict.pop('_id')
            expected_dict.pop('Dr')
        except:
            pass
        messages_list = fff(expected_dict, actual_dict)
        for message in messages_list:
            message_string += message
            message_string += '\n'
            if len(message_string) > 3900:
                print(message_string, file=sys.stdout)
                send_telegram(message)
                message_string = ''
                messages_timeout += 1
                if messages_timeout == 19:
                    time.sleep(50)
            print(message_string, file=sys.stdout)
            send_telegram(message)


        aromas_db.update_aroma_data(actual_dict)
