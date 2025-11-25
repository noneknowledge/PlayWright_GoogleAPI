from dotenv import dotenv_values

config = dotenv_values("./.env")
print(config["EMAIL_PASSWORD"])


def login():
    
    return print("login function.")