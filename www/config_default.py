# -*- coding: utf-8 -*-
"""
Created on Thu Oct 4 2018
@author: Vegelofe
Learned from Michael Liao
"""

# config_default.py

configs = {
    'debug': True,
    'db': {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '******',           #Your mysql password
        'db': 'chorus'
    },
    'session': {
        'secret': 'chorus'
    }
}
