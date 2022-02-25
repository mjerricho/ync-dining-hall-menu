from SatsScrape import SatsScrape, Day  
from datetime import datetime

if __name__ == "__main__":
    day = Day.WEEKDAY if datetime.today().weekday() <= 4 else Day.WEEKEND
    sats_scrape = SatsScrape("chromedriver", day)
    sats_scrape.login()
    sats_scrape.get_meal_links()
    sats_scrape.get_all_meals()
    message = sats_scrape.craft_message_all()
    sats_scrape.send_message(message)