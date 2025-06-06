# -*- coding: utf-8 -*-
import os

from urllib.request import URLError, urlretrieve, urlopen
import time

from resources.lib.utils import get_script_path, get_data_dir, get_config_value, log_message, load_json_data, save_json_data, remove_diacritics, display_message

PICONS_URL = 'https://marhycz.github.io/picons/640/'

def remap(picon):
    script_dir = get_script_path()
    filename = os.path.join(script_dir, 'remap.txt')
    try:
        with open(filename, "r") as f:
            for row in f:
                if len(row.strip()) > 0 and row[0] != '#':
                    mapping = row.strip().split('>')
                    if normalize_picon_name(picon) == normalize_picon_name(mapping[0]) + '.png':
                        return normalize_picon_name(mapping[1]) + '.png'
    except IOError as error:
        if error.errno != 2:
            display_message('Chyba při načtení remap.txt')
    return picon

def clear_cache():
    cache_data = load_json_data({'filename' : 'cache.json', 'description' : 'dat keše'})
    if cache_data is not None:
        ts = int(time.time())
        data_dir = get_data_dir()
        for picon in list(cache_data):
            if int(cache_data[picon]) + 60*60*24*int(get_config_value('dnu_v_kesi')) < ts:
                picon_file = os.path.join(data_dir, picon)
                if os.path.exists(picon_file):
                    os.remove(picon_file)
                del cache_data[picon]
        save_json_data({'filename' : 'cache.json', 'description' : 'dat keše'}, cache_data)

def normalize_picon_name(picon):
    remove_string = [' hd', ' ad', ' md 1', ' md 2', ' md 3', ' md 4', ' md 5', ' md 6', ' md 7', ' md 8', ' ', '+', ':', '/']
    picon = remove_diacritics(picon).lower()
    for string in remove_string:
        picon = picon.replace(string, '')
    return picon

def remap_picon(picon):
    remapped_picon = remap(picon)
    if picon != remapped_picon:
        return get_picon(remapped_picon, False)
    else:
        return get_err_picon()

def get_err_picon():
    script_dir = get_script_path()
    picon_file = os.path.join(script_dir, 'resources','images','picon_err.png')
    with open(picon_file, mode='rb') as file:
        return file.read()       

def get_picon(picon, remap = True):
    data_dir = get_data_dir()
    picon_filename = normalize_picon_name(picon)
    print(picon_filename)
    picon_file = os.path.join(data_dir, picon_filename)
    if int(get_config_value('dnu_v_kesi')) > 0:
        if os.path.exists(picon_file):
            with open(picon_file, mode='rb') as file:
                return file.read()       
        else:
            try:
                urlretrieve(PICONS_URL + picon_filename, picon_file)
                cache_data = load_json_data({'filename' : 'cache.json', 'description' : 'dat keše'})
                if cache_data is None:
                    cache_data = {}
                cache_data.update({picon_filename : int(time.time())})
                save_json_data({'filename' : 'cache.json', 'description' : 'dat keše'}, cache_data)
                with open(picon_file, mode='rb') as file:
                    return file.read()       
            except URLError as e:
                if remap == True:
                    return remap_picon(picon_filename)
                else:
                    return get_err_picon()
    else:
        try:
            response = urlopen(PICONS_URL + picon_filename)
            return response.read()
        except URLError as e:
            if remap == True:
                return remap_picon(picon_filename)
            else:
                log_message('Chyba při stažení ' + picon_filename)
                return get_err_picon()
