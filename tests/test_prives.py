

def test_prices(price_page):
    price_page.login()
    price_page.get_aromas()
    price_page.compare_dicts()

