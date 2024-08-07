import os
import sys
import configparser
import platform
            
def check_os():
    if platform.system() == 'Darwin':
        return True
    elif platform.system() == 'Windows':
        return False
    else:
        return ("Unknown")
    
def check_for_config():
    config = configparser.ConfigParser()
    if not os.path.exists("./config.ini"):
        config["App Settings"] = {
            "Dark_Mode": "auto"
        }
        with open("./config.ini", "w") as configfile:
            config.write(configfile)
    else:
        config.read("./config.ini")
    return config

def check_in_config(section, key):
    config = configparser.ConfigParser()
    config.read("./config.ini")
    try:
        return config.get(section, key)
    except (configparser.NoSectionError, configparser.NoOptionError):
        return None