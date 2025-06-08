# -*- coding: utf-8 -*-
import os
import shutil

import time
import requests

from resources.lib.utils import get_script_path, get_data_dir, get_config_value, log_message, load_json_data, save_json_data, remove_diacritics, display_message, is_kodi

def sync_remap_from_sample():
    script_dir = get_script_path()
    sample = os.path.join(script_dir, 'remap.txt.sample')
    if is_kodi() == True:
        data_dir = get_data_dir()
        filename = os.path.join(data_dir, 'remap.txt')
    else:
        filename = os.path.join(script_dir, 'remap.txt')
    if os.path.exists(filename) and os.path.exists(sample):
        try:
            remaps = []
            with open(filename, 'r', encoding = 'utf-8') as f:
                for row in f:
                    if len(row.strip()) > 0 and row[0] != '#':
                        remaps.append(row)
            with open(sample, 'r', encoding = 'utf-8') as s:
                for row in s:
                    if len(row.strip()) > 0 and row[0] != '#':
                        if row not in remaps:
                            with open(filename, 'a', encoding = 'utf-8') as f:
                                f.write(row)
                            f.close()
        except IOError as error:
            if error.errno != 2:
                display_message('Chyba při načtení remap.txt')

def remap(picon):
    script_dir = get_script_path()
    sample = os.path.join(script_dir, 'remap.txt.sample')
    if is_kodi() == True:
        data_dir = get_data_dir()
        filename = os.path.join(data_dir, 'remap.txt')
    else:
        filename = os.path.join(script_dir, 'remap.txt')
    if not os.path.exists(filename) and os.path.exists(sample):
        shutil.copyfile(sample, filename)
    try:
        with open(filename, 'r', encoding = 'utf-8') as f:
            for row in f:
                if len(row.strip()) > 0 and row[0] != '#':
                    mapping = row.strip().split('>')
                    if normalize_picon_name(picon) == normalize_picon_name(mapping[0]):
                        return normalize_picon_name(mapping[1])
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
        for file in os.listdir(data_dir):
            if '.png' in file and file not in cache_data.keys():
                os.remove(os.path.join(data_dir, file))

def normalize_picon_name(picon):
    remove_string = [' hd', ' ad', ' md 1', ' md 2', ' md 3', ' md 4', ' md 5', ' md 6', ' md 7', ' md 8', ' ', '+', ':', '/', '&', '.', '-']
    picon = remove_diacritics(picon).strip().lower().replace('.png', '')
    for string in remove_string:
        picon = picon.replace(string, '')
    return picon

def remap_picon(picon):
    remapped_picon = remap(picon) + '.png'
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
    picon_filename = normalize_picon_name(picon) + '.png'
    picon_file = os.path.join(data_dir, picon_filename)
    if int(get_config_value('dnu_v_kesi')) > 0:
        if os.path.exists(picon_file):
            with open(picon_file, mode='rb') as file:
                return file.read()       
        else:
            try:
                log_message(get_config_value('url_s_piconami') + picon_filename)
                resp = requests.get(get_config_value('url_s_piconami') + picon_filename)
                if resp.status_code not in [200]:
                    if remap == True:
                        return remap_picon(picon_filename)
                    else:
                        return get_err_picon()
                file = open(picon_file, 'wb')
                for chunk in resp:
                    if chunk:
                        file.write(chunk)
                file.close()
                cache_data = load_json_data({'filename' : 'cache.json', 'description' : 'dat keše'})
                if cache_data is None:
                    cache_data = {}
                cache_data.update({picon_filename : int(time.time())})
                save_json_data({'filename' : 'cache.json', 'description' : 'dat keše'}, cache_data)
                with open(picon_file, mode='rb') as file:
                    return file.read()   
            except Exception as e:
                if remap == True:
                    return remap_picon(picon_filename)
                else:
                    return get_err_picon()
    else:
        try:
            resp = requests.get(get_config_value('url_s_piconami') + picon_filename)
            if resp.status_code not in [200]:
                if remap == True:
                    return remap_picon(picon_filename)
                else:
                    return get_err_picon()
            return resp.read()
        except Exception as e:
            if remap == True:
                return remap_picon(picon_filename)
            else:
                log_message('Chyba při stažení ' + picon_filename)
                return get_err_picon()
