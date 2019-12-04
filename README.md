# ruian-service

Rychlá reverzní geolokační služba založená na datech veřejného registru RUIAN.
Služby jsou poskytovány pomocí jednotného REST API. 
V aktuální verzi jsou k dispozici tyto reverzně geolokační služby

- __Parcela__: Vrací identifikaci parcely vstupního bodu a informace o nadřazeném správním členění
* __Základní sídelní jednotka__: Vrací identifikaci ZSJ vstupního bodu a informace o nadřazeném správním členění
* __Katastrální území__: Vrací identifikaci KÚ vstupního bodu a informace o nadřazeném správním členění
* __Povodí__: Vrací identifikaci povodí vstupního bodu a informace o nadřazených povodích
* __Mapový list 1:50000__: Vrací identifikaci mapového listu Základní mapy ČR 1:50 000

## REST API
V případě služeb reverzní geolokace se používají metody GET a POST. 

### GET API
Parametry jsou součástí URL:

#### Parcela

        GET /geoapi/parcela?x=<jtsk.x>&y=<jtsk.y>
        
#### Základní sídelní jednotka

        GET /geoapi/zsj?x=<jtsk.x>&y=<jtsk.y>

#### Katastrální území

        GET /geoapi/ku?x=<jtsk.x>&y=<jtsk.y>

#### Povodí

        GET /geoapi/rozvodnice?x=<jtsk.x>&y=<jtsk.y>

#### Mapový list 1:50000

        GET /geoapi/maplist50?x=<jtsk.x>&y=<jtsk.y>


### POST API
Parametry jsou předávány v těle JSON zprávy:

        {"x":<jtsk.x>,"y":<jtsk.y>}

#### Parcela

        POST /geoapi/parcela

#### Základní sídelní jednotka

        POST /geoapi/zsj

#### Katastrální území

        POST /geoapi/ku

#### Povodí

        POST /geoapi/rozvodnice

#### Mapový list 1:50000

        POST /geoapi/maplist50

## Dockerizace

Pro nastavení parametrů aplikace se používají tyto systémové proměnné, které lze v rámci nasazeni kontejneru změnít:

* __POSTGIS_HOST__ _hostitel služby PostGIS_
* __POSTGIS_PORT__ _TCP port služby PostGIS_
* __RUIAN_DATABASE__ _název databáze, ve které jsou uložena data RUIAN_
* __POVODI_DATABASE__ _název databáze, ve které jsou uložena data povodí_
* __MAPY_DATABASE__ _název databáze, ve které jsou uložena data kladu map 1:50000_
* __POSTGIS_USER__ _jméno oprávněného uživatele služby PostGIS_
* __POSTGIS_PASSWORD__ _heslo k účtu oprávněného uživatele služby PostGIS_
* __RESOURCE_PREFIX__ _url prefix služby_
* __FLASK_ENV__ _prostředí Flask_


### vytvoření obrazu a spuštění kontejneru

        docker build -t ruian-service:latest .

        docker run -d --name ruian-service -e RESOURCE_PREFIX=geoapi -p 5000:5000 ruian-service
        
### Spolupráce

Pro správnou funkci kontejneru je třeba mít nainstalovanou PostGIS službu, 
jejíž identifikaci předáte kontejneru ruian-service pomocí systémových proměnných. 

### Odkazy

http://containertutorials.com/docker-compose/flask-simple-app.html
