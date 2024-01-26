import geopandas as gpd
from shapely.geometry import Point, LineString
import re
import os
import requests


def valider_nom_regex(data_set, data_set_name, regex):
    for nom in data_set:
        if len(nom) > 6 or not regex.match(nom):
            print(f"la valeur {nom} n'est pas un nom valide pour un {data_set_name}")


def verif_doublon_geom(data_set, data_set_name, data_set_name_field):
    for i in data_set.index:
        for j in data_set.index:
            # On teste à partir de i > j pour ne pas tester plusieurs fois les mêmes couples
            if i > j and data_set['geometry'][i] == data_set['geometry'][j]:
                print(f'les {data_set_name} {data_set[data_set_name_field][i]} et {data_set[data_set_name_field][j]} ont la même géométrie')


def verif_doublon_nom(data_set, data_set_name, data_set_name_field):
    for i in data_set.index:
        for j in data_set.index:
            # On teste à partir de i > j pour ne pas tester plusieurs fois les mêmes couples
            if i > j and data_set[data_set_name_field][i] == data_set[data_set_name_field][j]:
                print(f'les {data_set_name} {data_set[data_set_name_field][i]} et {data_set[data_set_name_field][j]} ont le même nom')


def sont_inclus_dans_emprise(geom_emprise, data_set, data_set_name, data_set_name_field):
    for i in data_set.index:
        if not data_set['geometry'][i].within(geom_emprise):
            print(f"Le {data_set_name} {data_set[data_set_name_field][i]} n'est pas situé à l'intérieur de l'emprise")


# Fonction permettant de vérifier qu'une géométrie est inclue dans une commune
def est_inclu_dans_la_commune(geom_emprise, insee):
    # On récupère la géométrie de la commune depuis l'IGN
    url = f'https://apicarto.ign.fr/api/cadastre/commune?code_insee={insee}'
    response = requests.get(url)

    if response.status_code == 200:
        # Chargement des données GeoJSON dans un GeoDataFrame avec Geopandas
        data_geojson = response.json()
        gdf_commune = gpd.GeoDataFrame.from_features(data_geojson['features'])
        # On convertie la géométrie de la commune en Lambert 93
        gdf_commune.crs = "EPSG:4326"
        gdf_commune = gdf_commune.to_crs(epsg=2154)

        # Test si les géométries s'intersectent
        if not gdf_commune['geometry'][0].intersects(geom_emprise):
            print(f"L'emprise n'est pas contenue au sein de la commune d'INSEE {insee}")



path = os.path.realpath(__file__) 
dir = os.path.dirname(path) 
dir_data = dir.replace('sources', 'test_data')

supports = gpd.read_file(dir_data + "/supports.shp")
foyers = gpd.read_file(dir_data + "/foyers.shp")
cables = gpd.read_file(dir_data + "/cables.shp")
emprise = gpd.read_file(dir_data + "/emprise.shp")

# pour test si nom de type nn-nnn (ex: 01-234)
regex = re.compile(r'\d{2}-\d{3}')

valider_nom_regex(supports['NOMSUP'], 'support', regex)
valider_nom_regex(foyers['NOMFOY'], 'support', regex)
valider_nom_regex(cables['NOMCAB'], 'support', regex)

# On vérifie que les supports sont sous le foyer du même nom
for i in supports.index:
    for j in foyers.index:
        if supports['NOMSUP'][i] == foyers['NOMFOY'][j]:
            if supports['geometry'][i] != foyers['geometry'][j]:
                print(f"Le support et le foyer de même nom {supports['NOMSUP'][i]} ne se superposent pas")
            break
    # Si les conditions pour amener au break n'ont pas été remplies
    else:
        print(f"le support {supports['NOMSUP'][i]} ne possède pas de foyer correspondant à sa numérotation")


# On vérifie que les foyers sont superposés à un support
for i in foyers.index:
    for j in supports.index:
        if foyers['geometry'][i] == supports['geometry'][j]:
            break
    # Si les conditions pour amener au break n'ont pas été remplies
    else:
        print(f"le foyer {foyers['NOMFOY'][i]} n'est pas superposé à un support")


# On vérifie que deux supports n'ont pas la même géométrie
verif_doublon_geom(supports, "supports", "NOMSUP")

# On vérifie que deux câbles n'ont pas la même géométrie
verif_doublon_geom(cables, "câbles", "NOMCAB")

# On vérifie que deux supports n'ont pas la même nom
verif_doublon_nom(supports, "supports", "NOMSUP")

# On vérifie que deux foyers n'ont pas la même nom
verif_doublon_nom(foyers, "foyers", "NOMFOY")

# On vérifie que deux câbles n'ont pas la même nom
verif_doublon_nom(cables, "câbles", "NOMCAB")

# On vérifie que la couche câble ne présente pas de géométrie invalide
for i in cables.index:
    if not cables['geometry'][i].is_valid:
        print(f"le câble {cables['NOMCAB'][i]} présente une géométrie invalide")


# On vérifie que les supports sont attachés aux câbles de même nom (si il existe)
for i in supports.index:
    for j in cables.index:
        if supports['NOMSUP'][i] == cables['NOMCAB'][j]:
            cable_start_coords = cables['geometry'][j].coords[0]
            cable_end_coords = cables['geometry'][j].coords[-1]

            # On teste si le support est à l'une des deux extrémités
            if not supports['geometry'][i].equals(Point(cable_start_coords)) and not supports['geometry'][i].equals(Point(cable_end_coords)):
                print(f"Le câble {cables['NOMCAB'][j]} n'est pas connecté au support de même nom")


# Vérifications sur l'emprise 
if len(emprise.index) != 1:
    print("La couche emprise doit contenir un seul enregistrement")
else:
    # Vérifications attributaires
    if emprise['NOM'][0] is None:
        print("Le nom de l'emprise n'est pas renseigné")
    if emprise['INSEE'][0] > 99999 or emprise['INSEE'][0] < 1000:
        print(f"La valeur INSEE {emprise['INSEE'][0]} de l'emprise est incohérente")
    if emprise['TECHNICIEN'][0] is None:
        print("Le nom du technicien n'est pas renseigné dans l'emprise")

    # Vérifications si les éléments supports, foyers, cables sont inclus dans la géométrie surfacique de l'emprise
    sont_inclus_dans_emprise(emprise['geometry'][0], supports, "support", "NOMSUP")
    sont_inclus_dans_emprise(emprise['geometry'][0], foyers, "foyer", "NOMFOY")
    sont_inclus_dans_emprise(emprise['geometry'][0], cables, "câble", "NOMCAB")

    est_inclu_dans_la_commune(emprise['geometry'][0], emprise['INSEE'][0])