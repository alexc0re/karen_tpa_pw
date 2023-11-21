import ast
import json
import os
import random
import time
from sendtelegram.telegram import send_telegram
from env_setup import Credentials
from base.app import App_Object
from data import data
from database.db_update import AromasDB
aromas_db = AromasDB()

def db_create():
    aromas_db.create_aroma_data()


def gachi():
    gachi_videos = ['https://www.youtube.com/watch?v=AIQZ_3xWosc', 'https://www.youtube.com/watch?v=johcE5s525M',
                    'https://www.youtube.com/watch?v=XWDdMVlhpwM&pp=ygULZ2FjaGkgdmlkZW8%3D',
                    'https://www.youtube.com/watch?v=frfZyKIHPuQ&t=40s&pp=ygULZ2FjaGkgdmlkZW8%3D',
                    'www.youtube.com/watch?v=fUdsmUbs3s0']
    return random.choice(gachi_videos)


def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o: (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
    same = set(o for o in shared_keys if d1[o] == d2[o])
    return added, removed, modified, same



def get_aroms_data_from_db():
    aromas_json = aromas_db.get_aroma_data_by_id()
    aroms = str(aromas_json)
    aroms = aroms[1:]
    aroms = aroms[:-1]
    aroms = aroms[:-1]
    aroms = ast.literal_eval(aroms)
    print(type(aroms))
    print(aroms)
    return aroms



class Price_page(App_Object):
    EMAIL_FIELD = "#Email"
    PASSWORD_FIELD = "#Password"
    LOGIN_BUTTON = ".page-action-bar .btn"
    ass = '623914148'
    AROMA_BLOCK = ('.product-listing li')
    AROMA_NAME = ('.product-listing li h2')
    PRICE = (f' li:nth-child({1}) .addtocart option')
    spisok = []
    aromas = {}
    data = data

    def login(self):
        self.open_tpa()
        self.page.fill(self.EMAIL_FIELD, Credentials.APP_USERNAME)
        self.page.fill(self.PASSWORD_FIELD, Credentials.APP_PASSWORD)
        self.page.click(self.LOGIN_BUTTON)

    def get_aromas(self):
        self.page.goto('https://shop.perfumersapprentice.com/c-84-bulk-sizes.aspx')
        aroma_blocks = self.page.locator(self.AROMA_BLOCK).all()
        for block in aroma_blocks:
            aroma_name = block.locator("h2").text_content()
            price_blocks = block.locator('.addtocart select option').all()
            prices = []
            for price_block in price_blocks:
                aroma_price = price_block.text_content()
                prefix = aroma_price[0:4]
                if 'gall' in prefix:
                    prices.append(aroma_price.replace(str('\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t'), 'Price: '))
                elif prefix == 'case':
                    prices.append(aroma_price.replace(str('\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t'), 'Price: ')
                                  .replace(' (4) 2week lead time', ''))
                elif prefix == 'doub':
                    prices.append(aroma_price.replace(str('\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t'), 'Price: ').
                                  replace(' (8) 2 week lead time', ''))
            if prices:
                self.aromas.update({aroma_name: prices})

    def compare_dicts(self):
        # send_telegram(gachi())
        actual_list = self.aromas
        expected_list = get_aroms_data_from_db()
        added, removed, modified, same = dict_compare(actual_list, expected_list)
        for products, prises_list in modified.items():
            arr = prises_list[0]
            arr2 = prises_list[1]
            i = 0
            if len(arr) == len(arr2):
                while i < len(arr):
                    if arr[i] != arr2[i]:
                        time.sleep(10)
                        print(f"\n{products}\nold:{arr2[i]} \nnew:{arr[i]}")
                        # send_telegram(f"\n{products}\nold:{arr2[i]} \nnew:{arr[i]}")

                        i += 1
                    else:
                        i += 1
            else:
                time.sleep(10)
                print(f'\nNew position was added/removed:\nOld file:{products}{arr2} '
                      f'\nNew file:{products}{arr}')
                # send_telegram(f'\nNew position was added/removed:\nOld file:{products}{arr2} '
                         #     f'\nNew file:{products}{arr}')
        aromas_db.update_aroma_data(self.aromas)


