import os
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector
from satsmenuscraper.items import MealItem, SetMealItem


class menuspider(scrapy.Spider):
    name = "menuscraper"
    start_urls = ["https://satscampuseats.yale-nus.edu.sg/"]

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.implicitly_wait(10)
        self.driver.get("https://satscampuseats.yale-nus.edu.sg/login")
        self.driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div/button/span/div"
        ).click()
        self.user = os.environ.get("USER")
        self.password = os.environ.get("PASS")
        self.driver.find_element_by_xpath("//input[@id='userNameInput']").send_keys(
            str(self.user)
        )  # username goes here
        self.driver.find_element_by_xpath("//input[@id='passwordInput']").send_keys(
            str(self.password)
        )  # password goes here rip security but i was too lazy
        self.driver.find_element_by_xpath('//*[@id="submitButton"]').click()

        self.driver.find_element_by_xpath(
            "//div[@id='root']/header/div/div/div/ul/li/button/span"
        ).click()

        element = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//html/body/div[1]/div/div/div/div/div/div[3]/div/div")
            )
        )

        # sleep(0.5)

        sel = self.driver.execute_script("return document.body.innerHTML")

        self.driver.quit()

        html_to_parse = Selector(text=sel)

        meal_groups = html_to_parse.xpath(
            "//html/body/div[1]/div/div/div/div/div/div[3]/div/div"
        )

        meals = []

        for mealdiv in meal_groups:
            item = MealItem()
            item["name"] = mealdiv.xpath("./h2/text()").get()
            if item["name"]:
                mealsubset = mealdiv.xpath("./div")
                tempdict = []
                for mealsubsetitem in mealsubset:
                    tempsetmeal = mealsubsetitem.xpath("./div/h3/text()").get()
                    meallink = mealsubsetitem.xpath("./div/div/div/a")
                    for link in meallink:
                        setmeal = SetMealItem()
                        setmeal["mealtype"] = tempsetmeal
                        setmeal["name"] = link.xpath("./text()").get()
                        tempurl = link.xpath("./@href").get()
                        setmeal["mealurls"] = tempurl[12:]
                        tempdict.append(setmeal)
                item["setmeals"] = tempdict
                meals.append(item)

        return meals
