from selenium.webdriver import Chrome
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

webdriver = "/Users/Mac/Developer/chromedriver"
driver = Chrome(webdriver)

data = {
    'Home': [],
    'Away': []
}

df = pd.DataFrame(data)

def get_bovada():
    driver.get("https://www.bovada.lv/sports/soccer")

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'next-events-bucket')))

    # change odds format
    dropdown = driver.find_element_by_class_name("sp-odds-format-selector-filter")
    dropdown.click()

    WebDriverWait(dropdown, 5).until(EC.invisibility_of_element((By.LINK_TEXT, ' Decimal Odds ')))
    decimal_odds = dropdown.find_element_by_xpath("//li[text()=' Decimal Odds ']")
    decimal_odds.click()

    show_more_btn = driver.find_element_by_id("showMore")
    show_more_btn.click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'next-events-bucket')))
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'showLess')))

    div = driver.find_element_by_class_name('next-events-bucket')
    icons = div.find_elements_by_class_name('icon-plus')

    for i in icons:
        try:
            i.click()
        except:
            print("Exception")

    games = div.find_elements_by_class_name('coupon-content')

    for game in games:
        try:
            competitors = game.find_element_by_class_name('competitors')
            teams = competitors.find_elements_by_class_name('competitor-name')
            print(teams[0].find_element_by_class_name('name').text + " vs."
            + teams[1].find_element_by_class_name('name').text)

            odds = game.find_elements_by_class_name('market-type')[1]
            prices = odds.find_elements_by_class_name('bet-price')
            new_data = {
                'Home': [teams[0].find_element_by_class_name('name').text],
                'Away': [teams[1].find_element_by_class_name('name').text],
                'BVD_HomeW': [float(prices[0].text)],
                'BVD_AwayW': [float(prices[1].text)],
                'BVD_Draw': [float(prices[2].text)]
            }

            df = df.append(pd.DataFrame(new_data), ignore_index=True, sort=False)
        except:
            print("exception")

def get_888():
    driver.get("https://us.888sport.com/soccer/#/filter/football")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "KambiBC-dropdown__selections")))
    dropdown = driver.find_elements_by_class_name("KambiBC-dropdown__selections")[0]
    dropdown.click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//li[@data-id='sortByTime']")))
    timeEle = driver.find_element_by_xpath("//li[@data-id='sortByTime']")
    timeEle.click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "KambiBC-odds-format-select")))
    dropdown = Select(driver.find_element_by_id("KambiBC-odds-format-select"))
    dropdown.select_by_visible_text("Decimal")

    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='KambiBC-betoffer-labels__event-count']")));
    unopened = driver.find_elements_by_xpath("//li[@class='KambiBC-betoffer-labels__event-count']")
    for u in unopened:
        u.click()

# get_bovada()
get_888()
print(df)
driver.close()
