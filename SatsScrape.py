import os
import time
from selenium import webdriver
import requests
from enum import Enum
import re
from pathlib import Path


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
        self.nutrition = ["Calories", "Protein", "Carbs", "Fats"]
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
        print(self.tele_bot_api)
        self.chat_ids = ["-799638512", "-1001625632323"]
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
        if self.day == Day.WEEKDAY:
            for i in range(1, 5):
                # breakfast
                if i < 4:
                    xpath = '//*[@id="root"]/div/div/div/div/div/div[3]/div/div[2]/div/div[2]/div/div[' + str(i) + ']/a'
                    element = self.driver.find_element_by_xpath(xpath)
                    self.breakfast_links.append(element.get_attribute('href'))
                # lunch
                xpath = '//*[@id="root"]/div/div/div/div/div/div[3]/div/div[3]/div/div[2]/div/div[' + str(i) + ']/a'
                element = self.driver.find_element_by_xpath(xpath)
                self.lunch_links.append(element.get_attribute('href'))
                # dinner
                xpath = '//*[@id="root"]/div/div/div/div/div/div[3]/div/div[4]/div/div[2]/div/div[' + str(i) + ']/a'
                element = self.driver.find_element_by_xpath(xpath)
                self.dinner_links.append(element.get_attribute('href'))
        else:
            for i in range(1, 5):
                # brunch
                xpath = '//*[@id="root"]/div/div/div/div/div/div[3]/div/div[2]/div/div[2]/div/div[' + str(i) + ']/a'
                element = self.driver.find_element_by_xpath(xpath)
                self.brunch_links.append(element.get_attribute('href'))
                # dinner
                xpath = '//*[@id="root"]/div/div/div/div/div/div[3]/div/div[3]/div/div[2]/div/div['+ str(i) +']/a'
                element = self.driver.find_element_by_xpath(xpath)
                self.dinner_links.append(element.get_attribute('href'))
    
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
            stat_full = self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/div/div/p["+str(i)+"]")
            stat_str = stat_full.text.split(" ")[-1]
            stat_float = float(re.findall(r'\d+', stat_str)[0])
            stats[self.nutrition[i - 1]] = stat_float
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
        message = f'''
_{meal['name']}_
    {self.nutrition[0]}: {meal[self.nutrition[0]]}
    {self.nutrition[1]}: {meal[self.nutrition[1]]}
    {self.nutrition[2]}: {meal[self.nutrition[2]]}
    {self.nutrition[3]}: {meal[self.nutrition[3]]}
        '''
        return message.replace("&", "%26")
    
    def craft_message_all(self) -> str:
        '''
        Crafting a message for all the meals for that day.
        '''
        if self.day == Day.WEEKDAY:
            return f'''
*Dining Hall Meals For Today*
*BREAKFAST*\
{self.craft_message_meal(self.breakfast_menu[0])}\
{self.craft_message_meal(self.breakfast_menu[1])}\
{self.craft_message_meal(self.breakfast_menu[2])}\

*LUNCH*\
{self.craft_message_meal(self.lunch_menu[0])}\
{self.craft_message_meal(self.lunch_menu[1])}\
{self.craft_message_meal(self.lunch_menu[2])}\
{self.craft_message_meal(self.lunch_menu[3])}\

*DINNER*\
{self.craft_message_meal(self.dinner_menu[0])}\
{self.craft_message_meal(self.dinner_menu[1])}\
{self.craft_message_meal(self.dinner_menu[2])}\
{self.craft_message_meal(self.dinner_menu[3])}\
            '''
        else:
            return f'''
*Dining Hall Meals For Today*
*BRUNCH*\
{self.craft_message_meal(self.brunch_menu[0])}\
{self.craft_message_meal(self.brunch_menu[1])}\
{self.craft_message_meal(self.brunch_menu[2])}\
{self.craft_message_meal(self.brunch_menu[3])}\

*DINNER*\
{self.craft_message_meal(self.dinner_menu[0])}\
{self.craft_message_meal(self.dinner_menu[1])}\
{self.craft_message_meal(self.dinner_menu[2])}\
{self.craft_message_meal(self.dinner_menu[3])}\
            '''
    
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
    
#TODO custom message e.g. most protein etc for more functions - 
# used the craft_message_meal for the custom one


