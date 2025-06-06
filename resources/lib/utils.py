# -*- coding: utf-8 -*-
import os

import codecs
import json
import unicodedata

def is_kodi():
    try:
        import xbmc
        test = int(xbmc.getInfoLabel('System.BuildVersion').split('.')[0])
        return True
    except Exception:
        return False

def get_script_path():
    path = os.path.realpath(__file__)
    if path is not None:
        return path.replace('/resources/lib/utils.py', '').replace('\\resources\\lib\\utils.py', '')

def get_data_dir():
    if is_kodi() == True:
        import xbmcaddon
        from xbmcvfs import translatePath
        addon = xbmcaddon.Addon()
        data_dir = translatePath(addon.getAddonInfo('profile'))
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
    else:
        data_dir = os.path.join(get_script_path(), 'data')
    return data_dir


def get_config_value(setting):
    if is_kodi() == True:
        import xbmcaddon
        addon = xbmcaddon.Addon()
        return addon.getSetting(setting)
    else:
        config_file = os.path.join(get_script_path(), 'config.txt')
        with codecs.open(config_file, 'r', 'utf-8') as f:
            config = json.load(f)
            f.close()
        if setting in config:
            return config[setting]
        
def log_message(message):
    if is_kodi() == True:
        import xbmc
        xbmc.log('Picons Server > ' + message) 
    else:
        print(message)

def display_message(message):
    if is_kodi() == True:
        import xbmcgui
        xbmcgui.Dialog().notification('Picons Server', message, xbmcgui.NOTIFICATION_ERROR, 4000)
    else:
        print(message)

def save_json_data(file, data):
    data_dir = get_data_dir()
    filename = os.path.join(data_dir, file['filename'])
    try:
        with open(filename, "w") as f:
            f.write('%s\n' % json.dumps(data))
    except IOError:
        display_message('Chyba uložení ' + file['description'])

def load_json_data(file):
    data = {}
    data_dir = get_data_dir()
    filename = os.path.join(data_dir, file['filename'])
    try:
        with open(filename, "r") as f:
            for row in f:
                data = row[:-1]
        data = json.loads(data)
    except IOError as error:
        if error.errno != 2:
            display_message('Chyba při načtení ' + file['description'])
    return data

def remove_diacritics(text):
    return str(unicodedata.normalize('NFKD',text).encode('ASCII','ignore').decode('utf-8'))

