import json
import os
import requests

class ResultHandler:
    def __init__(self, menu_today_json, menu_api_json) -> None:
        self.menu_today = menu_today_json
        self.menu_week = menu_api_json
        with open(menu_today_json) as menujsondata:
            self.menu_data = json.load(menujsondata)
        with open(menu_api_json) as apijsondata:
            self.api_data = json.load(apijsondata)[0]["data"]
        self.tele_bot_api = os.environ.get('BOTAPI')
        self.chat_ids = ["-1001625632323"]
        # self.chat_ids = ["-799638512"]

    def craft_message(self):
        self.text = "** DINING HALL MENU FOR TODAY: **\n\n"
        for meal in self.menu_data:
            if str(meal["name"]) == "Grab & Go":
                self.text += "**" + str(meal["name"]) + "**" + "\n" + "\n"
                for dish in meal["setmeals"]:
                    del dish["name"]
                    dish.update(
                        (list(filter(lambda x: (x["qrCode"] == dish["mealurls"]), self.api_data)))[0]
                    )
                    self.text += (
                        "**"
                        + str(dish["mealtype"])
                        + ":**"
                        + "\n"
                        + "__"
                        + str(dish["name"])
                        + "__"
                        + "\n"
                        + "\tCalories: "
                        + str(dish["totalCalorie"])
                        + str(dish["calorieUOM"])
                        + "\n"
                        + "\tCarbohydrate: "
                        + str(dish["totalCarbohydrate"])
                        + str(dish["carbohydrateUOM"])
                        + "\n"
                        + "\tTotal Protein: "
                        + str(dish["totalProtein"])
                        + str(dish["proteinUOM"])
                        + "\n"
                        + "\tTotal Fat: "
                        + str(dish["totalFat"])
                        + str(dish["fatUOM"])
                        + "\n"
                        + "\n"
                    )
            else:
                self.text += "**" + str(meal["name"]) + "**" + "\n" + "\n"
                for dish in meal["setmeals"]:
                    del dish["name"]
                    dish.update(
                        (list(filter(lambda x: (x["qrCode"] == dish["mealurls"]), self.api_data)))[0]
                    )
                    self.text += (
                        "__"
                        + str(dish["name"])
                        + "__"
                        + "\n"
                        + "\tCalories: "
                        + str(dish["totalCalorie"])
                        + str(dish["calorieUOM"])
                        + "\n"
                        + "\tCarbohydrate: "
                        + str(dish["totalCarbohydrate"])
                        + str(dish["carbohydrateUOM"])
                        + "\n"
                        + "\tTotal Protein: "
                        + str(dish["totalProtein"])
                        + str(dish["proteinUOM"])
                        + "\n"
                        + "\tTotal Fat: "
                        + str(dish["totalFat"])
                        + str(dish["fatUOM"])
                        + "\n"
                        + "\n"
                    )
        return self.text.replace("&", "%26")

    def write_data(self):
        with open("menu2.json", "w") as file:
            json.dump(self.menu_data, file)

        with open("summary.txt", "w") as file:
            file.write(self.text)
    
    def send_message(self, message: str):
        '''
        Sending the message on Telegram based on the chat id initialised.
        '''
        print("Sending Message")
        print("-----------------")
        for chat_id in self.chat_ids:
            message_url = self.tele_bot_api + chat_id + '&parse_mode=Markdown&text=' + message
            requests.get(message_url)(message_url)
        print("Message Sent")
        print("-----------------")
