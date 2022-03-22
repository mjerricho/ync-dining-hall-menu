# YNCDiningHallMenu_bot

## Project Description
This project aims to scrape the Yale-NUS dining hall website and send daily meals to a telegram group. We have noticed that going on the dining hall website takes a while as users will have to go through a login process. As the community uses Telegram as the main messaging platform, we have decided to try and make this process of checking today's dining hall menu a much more efficient process by bringing the message to the community. 

We utilized the Selenium library to interact with the web for the project. Selenium then scrapes all the available foods in today's dining menu and cleans the data. After cleaning said data, it will craft a message of the menu and use Telegram's API to send a message to a set group. The project aims to make it easier for the Yale-NUS community to know what they are eating today in a fast and quick way, avoiding the hassle of needing to go on the SATS website or go down to check. This effort would help up to 1000 people currently living on campus by saving up to 15 clicks (5 mins a day).

Additionally, we can provide more functions to generate more customised messages, such as the meal with the most protein or the least calories, to help students and faculty adhere to their diet. 

The project repository can be found at https://github.com/mjerricho/ync-dining-hall-menu.git

To join the Telegram Channel where we generate the messages, join this group https://t.me/YNCDiningMenu

## Version 2 - Scrapy + Selenium (Thanks to Bryan)
### Set-up
1. Run the following in your terminal (remove square brackets, keep double quotes (where applicable), replace placeholder values):

```
export USER=[your_username]
export PASS=[your_password]
export DT="[datetime_from_chrome _request_header]"
export SGT="[sgt_from_chrome _request_header]"
export AUTHORIZATION="[authorization_from_chrome _request_header]"
export XID="[xid_from_chrome _request_header]"
```
2. Install the chromedriver using `brew install -cask chromedriver` for Mac. 
3. Then, install [webdriver](https://chromedriver.chromium.org/downloads) into the project root folder e.g. chromedriver.

### How to run
1. Run `scrapy crawl menuscraper -o menu.json` (run daily at midnight to update menu for the day)
2. Run `scrapy crawl scrapesatsapi -o satsapi.json` (only need to run weekly, which is when SATS uploads the following week's menu; or run whenever errors noticed, or menu seems out of sync)
3. Run `python3 textfilegen.py`
4. Stonks (menu written in summary.text)

### Copy-pastable Scripts
```
scrapy crawl menuscraper -o menu.json
scrapy crawl scrapesatsapi -o satsapi.json
python3 textfilegen.py
```

## Version 1 - Only Selenium
### Installation
1. [Add Username and Password as environment variables.](https://phoenixnap.com/kb/set-environment-variable-mac).
2. Install [webdriver](https://chromedriver.chromium.org/downloads) into the project root folder e.g. chromedriver. If you are using another driver type, change the webdriver name in the `SatsScrape.py`.

### Setting up virtual environment
1. Run `python3 -m venv .venv`.
2. Run `source .venv/bin/activate`.
3. Run `pip install -r requirements.txt`.
To deactivate virtual environment, run `deactivate`.

### To run
Run `python3 Runner.py`.

### To check which chat groups the bot is in:
Get `https://api.telegram.org/bot<TOKEN>/GetUpdates`. Replace the `<TOKEN>` with the `/token` in botfather.

### To send messages
Get `https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHATID>&parse_mode=Markdown&text=<MESSAGE>`.

# Disclaimer
_SATS_Scraping contain links to external websites that are not provided or maintained by us. Please note we do not guarantee the accuracy, relevance, timeliness, or completeness of any information on these external websites._