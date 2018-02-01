#!/usr/bin/env python3

import configparser
from sys import argv

class Config():

    @staticmethod
    def config_name():
        file = 'config.cfg'
        return file

    @staticmethod
    def get_section(section):
        config = configparser.ConfigParser()
        config.read(Config.config_name())
        sec = config._sections[section]
        return sec

    @staticmethod
    def get_variable(section, key):
        sec = Config.get_section(section)
        return sec[key]
