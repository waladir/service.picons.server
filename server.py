# -*- coding: utf-8 -*-
import sys
import time
import threading

from resources.lib.web import start_server
from resources.lib.picons import clear_cache, sync_remap_from_sample
from resources.lib.utils import is_kodi, get_config_value, log_message

class BottleThreadClass(threading.Thread):
    def run(self):
        start_server()

bt = BottleThreadClass()
bt.start()

if is_kodi() == True:
    time.sleep(3)

interval = 60*60
next = time.time() + 10

if is_kodi() == True:
    import xbmc
    while not xbmc.Monitor().abortRequested():
        if(next < time.time()):
            time.sleep(3)
            sync_remap_from_sample()
            if int(get_config_value('dnu_v_kesi')) > 0:
                clear_cache()
                interval = 60*60
                next = time.time() + float(interval)
        time.sleep(1)
else:
    try:
        log_message('Start plánovače pro čištění keše\n')
        while True:
            if(next < time.time()):
                time.sleep(3)
                sync_remap_from_sample()
                if int(get_config_value('dnu_v_kesi')) > 0:
                    log_message('Čištění keše\n')
                    clear_cache()
                    next = time.time() + float(interval)
            time.sleep(1)
    except KeyboardInterrupt:
        log_message('Ukončení plánovače pro čištění keše\n')
        sys.exit()
