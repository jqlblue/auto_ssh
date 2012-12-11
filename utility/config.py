#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os, json, sys, getopt
class Config:
    def __init__(self, config):
        self._config = config
        self._items  = {}
        
    def getCategorys(self):
        categorys = self._config.keys()
        print(" ".join(categorys))
        
    def getItems(self, category):
        items_dict = self._config.get(category)
        items = []
        for k, v in items_dict.items():
            self._appendItem(v, k)
        for alias, hosts in self._items.items():
            hosts.sort()
            for host in hosts:
                items.append('[' + alias + ']' + host)
        print(" ".join(items))
        
    def _appendItem(self, alias, item):
        if self._items.has_key(alias):
            items = self._items.get(alias)
            items.append(item)
        else:
            items = []
            items.append(item)
        self._items[alias] = items

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

