<h1>Picons Server</h1>

Picons Server slouží jako zdroj log kanálů, dostupných přes http protokol. Lze ho používat buď jako doplněk v Kodi i samostatně.

<h3>Kodi</h3>

Nainstalujte doplněk a v jeho nastavení můžete změnit port pro webserver. Při změně restartněte Kodi.

<h3>Samostatný skript</h3>

Picons Server pro své fungování vyžaduje python modul bottle. Nainstaluje buď jako balíček OS (python3-bottle) nebo pomocí pip3 (pip3 install bottle)

Rozbalte zip, ykopírujte config.txt.sample do config.txt a případně upravte nastavení. Server spusťte z adresáře service.picons.server spuštěním python3 server.py.<br>
Pokud chcete Picons Server spustit na linuxu se systemd jako službu, jako root/přes sudo:
- zkopírujte z adresáře scripts soubor picons_server.service do /etc/systemd/system/
- systemctl daemon-reload
- systemctl enable picons_server
- systemctl start picons_server

<h3>Použití</h3>

Picony kanálu vrací http://&lt;IP adresa&gt;:&lt;port&gt;/picons/&lt;jméno kanálu&gt;, např. http://127.0.0.1:8083/picons/ČT1 HD. Za jméno kanálu lze přidat příponu .png, ale není to nezbytně nutné. 

Pro použití v TVheadendu můžete použít http://&lt;IP adresa&gt;:&lt;port&gt;/picons/%C. Při použití v jiných Kodi doplňcích je potřeba použít funkci quote z urllib.parse.

Doplněk převede vygeneruje normalizované jméno souboru. Odstraní diakritiku, převede velká písmena na malá, odstraní mezery, lomítka, dvojtečku, plus a řetězece hd, ad, md X atd. 

V souboru remap.txt v instalaci doplňku lze provést i ruční mapování ve formátu jméno kanálu&gt;jm0no picony.

<b><u>Změny</u></b>

1.0.0 (x.x.2025)<br>
- první verze<br><br>
