from gc import get_stats
from SatsScrape import SatsScrape, Day  
from datetime import datetime

if __name__ == "__main__":
    day = Day.WEEKDAY if datetime.today().weekday() <= 4 else Day.WEEKEND
    print(f"day is {day}")
    sats_scrape = SatsScrape("chromedriver", day)
    sats_scrape.login()
    #ONLY UNCOMMENT FOR TESTING PURPOSES
    sats_scrape.go_tomorrow()
    
    sats_scrape.get_meal_links()
    sats_scrape.get_all_meals()
    message = sats_scrape.craft_message_all()
    print(message)
    # only uncomment this if message is right
    # sats_scrape.send_message(message)
