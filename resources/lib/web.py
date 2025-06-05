# -*- coding: utf-8 -*-
from bottle import run, route, response

from resources.lib.picons import get_picon
from resources.lib.utils import get_config_value


@route('/picons/<picon1>/<picon2>')
def picons_slash(picon1, picon2):
    return picons(picon1 + '/' + picon2)

@route('/picons/<picon>')
def picons(picon):
    if picon[-4:] != '.png':
        picon = picon + '.png'
    picon = get_picon(picon)
    response.content_type = 'image/png'
    return picon

def start_server():
    port = int(get_config_value('webserver_port'))
    run(host = '0.0.0.0', port = port)

