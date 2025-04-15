import configparser


class Settings:
    CONFIG = configparser.ConfigParser()
    CONFIG.read("config.ini")
