#!/usr/bin/python3

import os

class Config: # settings for all environ
    """Base config class"""
    # get an environment variable. if missing use default.
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key') #
    DEBUG = False


class DevelopmentConfig(Config): # turns on debug mode
    """Development config settings"""
    DEBUG = True


# Dict to choose config by name
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
