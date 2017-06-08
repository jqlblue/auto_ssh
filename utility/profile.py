#!/usr/bin/env python
#-*- coding: utf-8 -*-
from ConfigParser import SafeConfigParser
#import os, sys, getopt
import os

class Profile:
    def __init__(self, config):
        self._config = config
        self._items  = []

    def getProfile(self, category):
        items = ['user', 'pass', 'port']
        for item in items:
            self._items.append(self._config.get(category, item))
        print(" ".join(self._items))

if __name__ == '__main__':
    #config = ConfigParser.ConfigParser()
    config_path = os.path.dirname(__file__)
    if not config_path:
        config_path = './'
    config = SafeConfigParser()
    
    config.read(config_path + '/../data/.profile.ini')
    #-c [category]
    #opts, args = getopt.getopt(sys.argv[1:], "hc:")
    o = Profile(config)

    category = 'default'

    #for op, value in opts:
        #if op == '-c':
         #   category = value

    o.getProfile(category)
