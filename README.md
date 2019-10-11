# ruian-service


## Podklady pro SQL dotazování

INSERT into spatial_ref_sys (srid, auth_name, auth_srid, proj4text, srtext) values ( 5514, 'EPSG', 5514, '+proj=krovak +lat_0=49.5 +lon_0=24.83333333333333 +alpha=30.28813972222222 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +towgs84=589,76,480,0,0,0,0 +units=m +no_defs ', 'PROJCS["S-JTSK / Krovak East North",GEOGCS["S-JTSK",DATUM["System_Jednotne_Trigonometricke_Site_Katastralni",SPHEROID["Bessel 1841",6377397.155,299.1528128,AUTHORITY["EPSG","7004"]],TOWGS84[589,76,480,0,0,0,0],AUTHORITY["EPSG","6156"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4156"]],PROJECTION["Krovak"],PARAMETER["latitude_of_center",49.5],PARAMETER["longitude_of_center",24.83333333333333],PARAMETER["azimuth",30.28813972222222],PARAMETER["pseudo_standard_parallel_1",78.5],PARAMETER["scale_factor",0.9999],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["X",EAST],AXIS["Y",NORTH],AUTHORITY["EPSG","5514"]]');


X:	-770180.3
Y:	-1068551.0


wkt_geom			Point (-770181.51000000000931323 -1068550.37999999988824129)
ogc_fid				229326	
gml_id				AD.78395364	
kod				78395364
nespravny	
cislodomovni			105	
cisloorientacni			NULL
cisloorientacnipismeno
psc				26724
stavebniobjektkod		94092133
ulicekod			NULL
platiod				2018-05-31T00:00:00
platido	
idtransakce			2428873
globalniidnavrhuzmeny		1759334
isknbudovaid			NULL
zachranka			SRID=5514;POINT(-770181.51 -1068549.52)
hasici				SRID=5514;POINT(-770181.71 -1068551.64)



select * from katastralniuzemi where st_distance(originalnihranice,'SRID=5514;POINT(-770180.3 -1068551.0)') < 2;

ST_Contains(geometry geomA, geometry geomB);

select * from katastralniuzemi where st_contains(originalnihranice,'SRID=5514;POINT(-770180.3 -1068551.0)');

select * from katastralniuzemi LEFT OUTER JOIN obce on (katastralniuzemi.obeckod=obce.kod) where st_contains(originalnihranice,'SRID=5514;POINT(-770180.3 -1068551.0)');



LEFT OUTER JOIN obce on (katastralniuzemi.obeckod=obce.kod)




geometry ST_Transform(geometry geom, text from_proj, text to_proj);



SELECT ST_AsText(ST_Transform(ST_GeomFromText('POLYGON((743238 2967416,743238 2967450,743265 2967450,743265.625 2967416,743238 2967416))',2249),4326)) As wgs_geom;

SELECT ST_AsText(ST_Transform(ST_GeomFromText('POINT(-770180.3 -1068551.0)',5514),4326)) As wgs_geom;


wgs_geom
POINT(14.0928261730485 49.8260545514689)






ogc_fid 
gml_id 
kod 
nespravny 
cislodomovni 
cisloorientacni 
cisloorientacnipismeno 
psc 
stavebniobjektkod 
ulicekod 
platiod 
platido 
idtransakce 
globalniidnavrhuzmeny 
isknbudovaid 
adresnibod 
zachranka 
hasici 

gml_id, kod, cislodomovni, cisloorientacni, cisloorientacnipismeno, psc, stavebniobjektkod, ulicekod 


select *
from pou
where st_contains(originalnihranice,'SRID=5514;POINT(-770180.3 -1068551.0)');


SELECT gml_id, kod, cislodomovni, cisloorientacni, cisloorientacnipismeno, psc, stavebniobjektkod, ulicekod, ST_Distance(adresnibod , ST_Transform(ST_GeometryFromText('POINT(-770180.3 -1068551.0)', 5514), 900913))
FROM adresnimista
ORDER BY ST_Distance(adresnibod , ST_GeometryFromText('POINT(14.4180933 50.0767469)', 4326))
LIMIT 10;



SELECT gml_id, kod, cislodomovni, cisloorientacni, cisloorientacnipismeno, psc, stavebniobjektkod, ulicekod, ST_Distance(adresnibod , ST_GeometryFromText('POINT(-770180.3 -1068551.0)', 5514))
FROM adresnimista
ORDER BY ST_Distance(adresnibod , ST_GeometryFromText('POINT(-770180.3 -1068551.0)', 5514))
LIMIT 10;

SELECT gml_id, kod, cislodomovni, cisloorientacni, cisloorientacnipismeno, psc, stavebniobjektkod, ulicekod, ST_Distance(adresnibod , ST_GeometryFromText('POINT(-770180.3 -1068551.0)', 5514))
FROM adresnimista
ORDER BY ST_Distance(adresnibod , ST_GeometryFromText('POINT(-770180.3 -1068551.0)', 5514))
LIMIT 10;



SELECT * FROM Customers
WHERE Country='Mexico';



katastralniuzemi.gml_id
katastralniuzemi.kod
katastralniuzemi.nazev
katastralniuzemi.obeckod
obce.gml_id
obce.kod
obce.nazev
obce.statuskod
obce.okreskod
obce.poukod
obce.nutslau
okresy.gml_id
okresy.kod
okresy.nazev
okresy.krajkod
okresy.vusckod
okresy.nutslau
kraje.gml_id
kraje.kod
kraje.nazev
kraje.statkod
pou.gml_id
pou.kod
pou.nazev
pou.spravniobeckod
pou.orpkod








gml_id,kod,nazev,obeckod





select katastralniuzemi.gml_id, katastralniuzemi.kod, katastralniuzemi.nazev  obce.
from katastralniuzemi 
LEFT OUTER JOIN obce on (katastralniuzemi.obeckod=obce.kod) 
where st_contains(katastralniuzemi.originalnihranice,'SRID=5514;POINT(-770180.3 -1068551.0)');







ST_Distance(adresnibod , ST_Transform(ST_GeometryFromText('POINT(-770180.3 -1068551.0)', 5514), 900913))




import psycopg2
from postgis import LineString
from postgis import Point
from postgis.psycopg import register
db = psycopg2.connect("dbname='ruian' user='docker' host='localhost' password='docker'")
register(db)
cursor = db.cursor()


//cursor.execute('CREATE TABLE IF NOT EXISTS mytable ("geom" geometry(LineString) NOT NULL)')
//cursor.execute('INSERT INTO mytable (geom) VALUES (%s)', [LineString([(1, 2), (3, 4)], srid=4326)])
//cursor.execute('SELECT geom FROM mytable LIMIT 1')


cursor.execute("select * from katastralniuzemi where st_contains(originalnihranice,'SRID=5514;POINT(-770180.3 -1068551.0)')")


geom = cursor.fetchone()[0]











import sys
>>> sys.modules[__name__].__dict__.clear()











> import psycopg2
> from postgis import LineString
> from postgis.psycopg import register
> db = psycopg2.connect(dbname="test")
> register(db)
cursor = db.cursor()

> cursor.execute('CREATE TABLE IF NOT EXISTS mytable ("geom" geometry(LineString) NOT NULL)')
> cursor.execute('INSERT INTO mytable (geom) VALUES (%s)', [LineString([(1, 2), (3, 4)], srid=4326)])
> cursor.execute('SELECT geom FROM mytable LIMIT 1')
> geom = cursor.fetchone()[0]
> geom
<LineString LINESTRING(1.0 2.0, 3.0 4.0)>
> geom[0]
<Point POINT(1.0 2.0)>
> geom.coords
((1.0, 2.0), (3.0, 4.0))
> geom.geojson
{'coordinates': ((1.0, 2.0), (3.0, 4.0)), 'type': 'LineString'}
> str(geom.geojson)
'{"type": "LineString", "coordinates": [[1, 2], [3, 4]]}'





db = psycopg2.connect("dbname='test' user='docker' host='localhost' password='docker'")
db1 = psycopg2.connect("dbname='ruian' user='docker' host='localhost' password='docker'")
cursor1 = db1.cursor()
cursor1.execute('SELECT * FROM public.katastralniuzemi LIMIT 1')


cursor1.fetchone()[19]


SELECT * FROM public.katastralniuzemi 


ST_Within(geometry A, geometry B)

[LineString([(1, 2), (3, 4)], srid=4326)]


SELECT * FROM public.katastralniuzemi WHERE ST_Within(p, originalnihranice);



Point(-770180.3, -1068551.0)



Point(x=-770180.3, y=-1068551.0, srid=5514)
X:	-770180.3
Y:	-1068551.0
