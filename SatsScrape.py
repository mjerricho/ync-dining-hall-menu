import os
import time
import requests
import re
from enum import Enum
from pathlib import Path
from pprint import pprint

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class Day(Enum):
    WEEKDAY = 1
    WEEKEND = 2

class SatsScrape:
    def __init__(self, webdriver_name: str, day: Day) -> None:
        '''
        Initialising the SatsScrape. Accessing the website.
        input:
            webdriver <str>: path to webdriver.
            day <Day>: An indication whether that day is weekday or weekend.
        '''
        print("Initialising webdriver")
        print("-----------------")
        project_root = Path(__file__).parent
        webdriver_path = str(project_root) + "/" + str(webdriver_name)
        self.URL = "https://satscampuseats.yale-nus.edu.sg/login"
        self.driver = webdriver.Chrome(webdriver_path)
        self.user = os.environ.get('USER')
        self.password = os.environ.get('PASSWORD')
        self.day = day
        self.nutrition = ("Calorie", "Protein", "Carbs", "Fat")
        # meal links
        if day == Day.WEEKDAY:
            self.breakfast_links = []
            self.breakfast_menu = []
            self.lunch_links = []
            self.lunch_menu = []
        else:
            self.brunch_links = []
            self.brunch_menu = []
        self.dinner_links = []
        self.dinner_menu = []
        self.tele_bot_api = os.environ.get('BOTAPI')
        self.chat_ids = ["-1001625632323"]
        print("Webdriver initialised")
        print("-----------------")
    
    def login(self) -> None:
        '''
        Login to the website.
        '''
        print("Logging in")
        print("-----------------")
        self.driver.get(self.URL)
        self.driver.find_element_by_class_name("jss8").click()
        self.driver.find_element_by_id("userNameInput").send_keys(str(self.user))
        self.driver.find_element_by_id("passwordInput").send_keys(str(self.password))
        # click login button
        self.driver.find_element_by_id("submitButton").click()
        print("Logged in")
        print("-----------------")

    def get_meal_links(self) -> None:
        '''
        Get all the meal links available and append them to the meal links list.
        The meal links depend on the day when class is initialised.
        '''
        print("Getting meal links")
        print("-----------------")
        # click "our food"
        self.driver.find_element_by_class_name("jss97").click()
        time.sleep(2)
        i = 1
        if self.day == Day.WEEKDAY:
            # breakfast
            while True:
                try:
                    print("finding")
                    xpath = '//*[@id="root"]/div/div/div/div/div/div[3]/div/div[2]/div/div[2]/div/div[' + str(i) + ']/a'
                    element = self.driver.find_element_by_xpath(xpath)
                    self.breakfast_links.append(element.get_attribute('href'))
                    i += 1
                except NoSuchElementException:
                    i = 1 
                    break
            # lunch
            while True:
                try:
                    xpath = '//*[@id="root"]/div/div/div/div/div/div[3]/div/div[3]/div/div[2]/div/div[' + str(i) + ']/a'
                    element = self.driver.find_element_by_xpath(xpath)
                    self.lunch_links.append(element.get_attribute('href'))
                    i += 1
                except NoSuchElementException: 
                    i = 1
                    break
            # dinner
            while True:
                try: 
                    xpath = '//*[@id="root"]/div/div/div/div/div/div[3]/div/div[4]/div/div[2]/div/div[' + str(i) + ']/a'
                    element = self.driver.find_element_by_xpath(xpath)
                    self.dinner_links.append(element.get_attribute('href'))
                    i += 1
                except NoSuchElementException: 
                    break
        else:
            while True:
                # brunch
                try:
                    xpath = '//*[@id="root"]/div/div/div/div/div/div[3]/div/div[2]/div/div[2]/div/div[' + str(i) + ']/a'
                    element = self.driver.find_element_by_xpath(xpath)
                    self.brunch_links.append(element.get_attribute('href'))
                    i += 1
                except NoSuchElementException: 
                    i = 1
                    break
                # # dinner
                try:
                    xpath = '//*[@id="root"]/div/div/div/div/div/div[3]/div/div[3]/div/div[2]/div/div[' + str(i) + ']/a'
                    element = self.driver.find_element_by_xpath(xpath)
                    self.dinner_links.append(element.get_attribute('href'))
                    i += 1
                except NoSuchElementException: 
                    break
    
    def get_stats(self, link: str) -> "dict[str: str, str: float, str:float, str:float, str:float]":
        '''
        Get all the stats from a specified meal.
        input:
            link <str>: the link to the meal
        output:
            stats <dict>: dictionary of name, Calories, Protein, Carbs, and Fats.
        '''
        self.driver.get(link)
        time.sleep(1)
        name = self.driver.find_element_by_xpath('//*[@id="signup-modal-slide-description"]/div/div/div[2]/h3').text
        stats = {"name": name}
        for i in range(1, 5):
            try:
                stat_full = self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/div/div/p["+str(i)+"]")
                stat_str = stat_full.text.split(" ")[-1]
                stat_float = float(re.findall(r'\d+', stat_str)[0])
                stats[self.nutrition[i - 1]] = stat_float
            except NoSuchElementException: pass
        return stats
    
    def get_all_meals(self):
        '''
        Getting all the meals (name, calories, protein, carbs, and fats) and append them into a list.
        The information is stored in the state.
        '''
        print("Getting the stats for all meals.")
        print("-----------------")
        if self.day == Day.WEEKDAY:   
            for i in range(4):
                if i < 3:
                    self.breakfast_menu.append(self.get_stats(self.breakfast_links[i]))
                self.lunch_menu.append(self.get_stats(self.lunch_links[i]))
                self.dinner_menu.append(self.get_stats(self.dinner_links[i]))
        else:
            for i in range(4):
                self.brunch_menu.append(self.get_stats(self.brunch_links[i]))
                self.dinner_menu.append(self.get_stats(self.dinner_links[i]))
        print("Finished scraping website")
        print("-----------------")
    
    def craft_message_meal(self, meal: "dict[str: str, str: float, str:float, str:float, str:float]") -> str:
        '''
        Crafting a message for a specific given meal.
        '''
        message = ''''''
        for meal_property in meal.keys():
            if meal_property == 'name':
                message = "".join([message, 
f'''_{meal.get(meal_property, None)}_'''])
            elif meal_property == self.nutrition[0]:
                message = "".join([message, f'''
    {meal_property}: {meal.get(meal_property, None)} Kcal'''])
            else:
                message = "".join([message, f'''
    {meal_property}: {meal.get(meal_property, None)} g'''])
        return message.replace("&", "%26")
    
    def craft_message_menu(self, menu: list, title: str) -> str:
        '''
        crafting a message for a specific given menu
        input:
            menu <list> e.g. self.breakfast_menu
            title <str>
        output:
            message <str>
        '''
        message = f'''*{title}*'''
        for meal in menu:
            message = "".join([message, f'''
{self.craft_message_meal(meal)}'''])
        return message + "\n"
    
    def craft_message_all(self) -> str:
        '''
        Crafting a message for all the meals for that day.
        '''
        if self.day == Day.WEEKDAY:
            return f'''*Dining Hall Meals For Today*
{self.craft_message_menu(self.breakfast_menu, "BREAKFAST")}
{self.craft_message_menu(self.lunch_menu, "LUNCH")}
{self.craft_message_menu(self.dinner_menu, "DINNER")}'''
        else:
            return f'''*Dining Hall Meals For Today*
{self.craft_message_menu(self.brunch_menu, "BRUNCH")}
{self.craft_message_menu(self.dinner_menu, "DINNER")}'''
    
    def send_message(self, message: str):
        '''
        Sending the message on Telegram based on the chat id initialised.
        '''
        print("Sending Message")
        print("-----------------")
        for chat_id in self.chat_ids:
            message_url = self.tele_bot_api + chat_id + '&parse_mode=Markdown&text=' + message
            requests.get(message_url)
        print("Message Sent")
        print("-----------------")

