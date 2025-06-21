#!/usr/bin/python3


import os

class Config:
    """Base config class"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    """Development config settings"""
    DEBUG = True


# Dict to choose config by name
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
