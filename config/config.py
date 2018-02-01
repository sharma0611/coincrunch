#!/usr/bin/env python3

#default values
host = ""
port = ""
dbname = ""
user = ""
password = ""

#grab configured values
import yaml

with open("config/config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

host = cfg["host"]
port = cfg["port"]
dbname = cfg["db"] 
user = cfg["user"]
password = cfg["password"]

