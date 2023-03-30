from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Selenium and Pandas preparation
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Connection': 'keep-alive',
}

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-notifications')
options.add_argument('--disable-web-security')
options.add_argument('--start-maximized')
options.add_argument('--window-size=1920,1080')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--lang=en-US')
options.add_argument('--user-agent='+headers['User-Agent'])
options.add_argument('--accept-language='+headers['Accept-Language'])
options.add_argument('--accept-encoding='+headers['Accept-Encoding'])
options.add_argument('--connection='+headers['Connection'])

path = r"""C:\Users\Fred\Desktop\chromedriver.exe"""
s = Service(path)
driver = webdriver.Chrome(service=s, chrome_options=options)
elo_url = 'https://tennisabstract.com/reports/atp_elo_ratings.html'
pd.set_option('display.max_columns', None)

# Scrape the player stats and store them in a dataframe
def scrape_player_data(player):
    player_url = f'https://www.tennisabstract.com/cgi-bin/player-classic.cgi?p={player}'
    driver.get(player_url)

    show_splits_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#splitsbody > tr:nth-child(11) > td.splittoggle")))
    split_table = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="wonloss"]')))
    split_html = split_table.get_attribute('innerHTML')

    df = pd.read_html(str(split_html))[0]
    player_stats = df.iloc[0:4, [0, 1, 8, 10]]
    return player_stats

# Scrape the player elo and store it in a dataframe
def scrape_player_elo(player):
    driver.get(elo_url)

    wait = WebDriverWait(driver, 5)
    table = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/table[4]')))

    df = pd.read_html(table.get_attribute('innerHTML'))[0]
    player_index = df[df['Player'] == player].index.values
    player_elo = df.iloc[player_index, [5, 6, 7, 9, 10, 11, 13]]

    return player_elo