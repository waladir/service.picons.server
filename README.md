<h1>Picons Server</h1>

Picons Server slouží jako zdroj log kanálů, dostupných přes http protokol. Lze ho používat buď jako doplněk v Kodi i samostatně. Jako zdroj jsou používané picony od lukas.v z https://github.com/luvadcz/piconsserver.

Další informace a podporu najdete na fóru www.xbmc-kodi.cz v KODI - Doplňky - Programy a hry (https://www.xbmc-kodi.cz/prispevek-picons-server).

<h3>Kodi</h3>

Doplněk najdete v XBMC Kodi CZ/SK repozitáři v Služby. V jeho nastavení můžete změnit port pro webserver, případně jak dlouho se budou ikony držet v lokální keši. Při změně restartněte Kodi.

<h3>Samostatný skript</h3>

Picons Server pro své fungování vyžaduje python modul bottle. Nainstaluje buď jako balíček OS (python3-bottle) nebo pomocí pip3 (pip3 install bottle)

Rozbalte zip, zkopírujte config.txt.sample do config.txt a remap.txt.sample do remap.txt a případně upravte nastavení. Server spusťte z adresáře service.picons.server spuštěním python3 server.py.<br>
Pokud chcete Picons Server spustit na linuxu se systemd jako službu, jako root/přes sudo:
- zkopírujte z adresáře scripts soubor picons_server.service do /etc/systemd/system/
- systemctl daemon-reload
- systemctl enable picons_server
- systemctl start picons_server

<h3>Použití</h3>

Piconu kanálu lze stáhnout z http://&lt;IP adresa&gt;:&lt;port&gt;/picons/&lt;jméno kanálu&gt;, např. http://127.0.0.1:8083/picons/ČT1 HD. Za jméno kanálu lze přidat příponu .png, ale není to nezbytně nutné. 

Pro použití v TVheadendu můžete použít http://&lt;IP adresa&gt;:&lt;port&gt;/picons/%C. Při použití v jiných Kodi doplňcích je potřeba použít funkci quote z urllib.parse.

Doplněk převede vygeneruje normalizované jméno souboru. Odstraní diakritiku, převede velká písmena na malá, odstraní mezery, lomítka, dvojtečku, plus a řetězce hd, ad, md X atd. 

V souboru remap.txt v instalaci doplňku lze provést i ruční mapování ve formátu jméno kanálu&gt;jméno picony.

<b><u>Změny</u></b>

1.0.0 (8.6.2025)
- první verze
