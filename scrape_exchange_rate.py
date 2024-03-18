import json
import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from datetime import datetime as dt

URL = "https://www.boc.cn/sourcedb/whpj/"


def get_currency_name(currency_code: str) -> str | None:
    """get the currency name from the currency code

    Args:
        currency_code (str): the code of the currency

    Returns:
        str: the name of the currency if the currency code is found, otherwise None
    """
    with open("currency_codes.json", "r", encoding="utf-8") as f:
        currency_codes = json.load(f)

    for code in currency_codes:
        if code["currency_code"] == currency_code:
            return code["currency_name"]
    return None


def get_currency_exchange_rate(date: str, currency_code: str) -> tuple | None:
    """get the exchange rate of a currency on a specific date

    Args:
        date (str): the date to get the exchange rate, format: %Y%m%d
        currency_code (str): the currency code to get the exchange rate

    Returns:
        tuple: (currency_code, date, exchange_rate) if the exchange rate is found, otherwise None
    """
    currency_name = get_currency_name(currency_code)
    if not currency_name:
        print(f"{currency_code} is not supported")
        return None

    date = dt.strptime(date, "%Y%m%d").strftime("%Y-%m-%d")

    try:
        options = webdriver.ChromeOptions()
        browser = webdriver.Chrome(options=options)
        browser.get(URL)

        # select the end time
        endtime_element = browser.find_element(By.ID, "nothing")
        endtime_element.clear()
        endtime_element.send_keys(date)

        # select the currency
        select_element = browser.find_element(By.ID, "pjname")
        select = Select(select_element)
        select.select_by_value(currency_name)

        # click the search button to get the exchange rate
        search_btn = browser.find_element(By.CSS_SELECTOR, "td > input.search_btn")
        search_btn.click()

        # get the exchange rate
        tabel = browser.find_element(By.CSS_SELECTOR, "div.BOC_main.publish > table")
        tr = tabel.find_elements(By.TAG_NAME, "tr")[1]
        tds = tr.find_elements(By.TAG_NAME, "td")
        if len(tds) == 7:
            return (currency_code, date, tds[3].text)
        else:
            return (currency_code, date, "")
    except Exception as e:
        print(f"For {currency_code}, an error occurred: {str(e)}")
    finally:
        browser.quit()

    return None


if __name__ == "__main__":
    arg = argparse.ArgumentParser()
    arg.add_argument("date", type=str, help="The date to get the exchange rate")
    arg.add_argument(
        "currency_code", type=str, help="The currency code to get the exchange rate"
    )
    args = arg.parse_args()
    data = get_currency_exchange_rate(args.date, args.currency_code)

    if data:
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(f"{data[0]} {args.date} {data[2]}")
        print(
            f"Successfully saved the selling price of {args.currency_code} in result.txt"
        )
    else:
        print(
            f"An error occurred while getting the exchange rate of {args.currency_code} on {args.date}"
        )
