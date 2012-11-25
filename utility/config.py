#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os, json, sys, getopt
class Config:
    def __init__(self, config):
        self._config = config
        
    def getCategorys(self):
        categorys = self._config.keys()
        print(" ".join(categorys))
        
    def getItems(self, category):
        items_dict = self._config.get(category)
        items = []
        for k, v in items_dict.items():
            if v == '':
                items.append(k)
            else:
                items.append(k + '[' + v + ']')
        print(" ".join(items))

    def getHostByAlias(self, alias):
        categorys = self._config.keys()
        hosts = []
        for category in categorys:
            items_dict = self._config.get(category)
            for k, v in items_dict.items():
                if v == alias:
                    hosts.append(k + '[' + category + ']')
        print (" ".join(hosts))

if __name__ == '__main__':
    #config = ConfigParser.ConfigParser()
    config_path = os.path.dirname(__file__)
    if not config_path:
        config_path = './'
    f = file(config_path + '/../data/host_config.json')
    config = json.load(f)
    f.close
    #-c [category] -a [alias]
    opts, args = getopt.getopt(sys.argv[1:], "hc:a:")
    o = Config(config)
    if (opts == []):
        o.getCategorys()
        exit()

    for op, value in opts:
        if op == '-c':
            o.getItems(value)
        elif op == '-a':
            o.getHostByAlias(value)
        else:
            o.getCategorys()

