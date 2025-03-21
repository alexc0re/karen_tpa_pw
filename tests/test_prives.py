

def test_prices(price_page):
    # db_create()
    price_page.login()
    price_page.get_aromas()
    price_page.compare_dicts()



# def test_get_aroms():
#     get_aroms_data_from_db()