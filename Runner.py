from ResultHandler import ResultHandler


if __name__ == "__main__":
    result_handler = ResultHandler("menu.json", "satsapi.json")
    message = result_handler.craft_message()
    print(message)
    # sending message 
    result_handler.send_message(message)