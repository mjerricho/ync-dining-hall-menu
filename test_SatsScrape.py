from SatsScrape import SatsScrape, Day  

sats_scrape = SatsScrape("chromedriver", Day.WEEKDAY)

def test__init__():
    assert(sats_scrape.URL == "https://satscampuseats.yale-nus.edu.sg/login")
    assert(sats_scrape.day == Day.WEEKDAY)

sats_scrape.login()
sats_scrape.get_meal_links()

def test_get_meal_links():
    assert(len(sats_scrape.dinner_links) == 4)