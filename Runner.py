from gc import get_stats
from SatsScrape import SatsScrape, Day  
from datetime import datetime

if __name__ == "__main__":
    sats_scrape = SatsScrape("chromedriver", Day.WEEKDAY)
    sats_scrape.login()
    # sats_scrape.get_day()
    # sats_scrape.go_tomorrow()
    sats_scrape.get_meal_links()
    sats_scrape.get_all_meals()
    message = sats_scrape.craft_message_all()
    print(message)
    # only uncomment this if message is right
    sats_scrape.send_message(message)
