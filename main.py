import scraper
from scraper import driver
import time

# Prompt the user to enter the names of the tennis players
player1 = input("Enter the name of player 1: ")
player2 = input("Enter the name of player 2: ")

# Create variations of the initial inputs
conca_player1 = player1.replace(' ', '')
conca_player2 = player2.replace(' ', '')
nbsp_player1 = player1.replace(' ', ' ')
nbsp_player2 = player2.replace(' ', ' ')

# Retrieve the data for Player 1
print('Player 1:')
player_stats = scraper.scrape_player_data(conca_player1)
print(player_stats)
print()
player_elo = scraper.scrape_player_elo(nbsp_player1)
print(player_elo)

time.sleep(2)
print()

# Retrieve the data for Player 2
print('Player 2:')
player_stats = scraper.scrape_player_data(conca_player2)
print(player_stats)
print()
player_elo = scraper.scrape_player_elo(nbsp_player2)
print(player_elo)

driver.quit()
