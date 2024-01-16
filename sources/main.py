import geopandas as gpd
from shapely.geometry import Point, LineString
import re
import os


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


path = os.path.realpath(__file__) 
dir = os.path.dirname(path) 
dir_data = dir.replace('sources', 'test_data')

supports = gpd.read_file(dir_data + "/supports.shp")
foyers = gpd.read_file(dir_data + "/foyers.shp")
cables = gpd.read_file(dir_data + "/cables.shp")

# pour test si nom de type nn-nnn (ex: 01-234)
regex = re.compile(r'\d{2}-\d{3}')

valider_nom_regex(supports['NOMSUP'], 'support', regex)
valider_nom_regex(foyers['NOMFOY'], 'support', regex)
valider_nom_regex(cables['NOMCAB'], 'support', regex)

# On vérifie que les supports sont sous le foyer du même nom
for i in supports.index:
    correspondance = False
    for j in foyers.index:
        if supports['NOMSUP'][i] == foyers['NOMFOY'][j]:
            correspondance = True

            if supports['geometry'][i] != foyers['geometry'][j]:
                print(f"Le support et le foyer de même nom {supports['NOMSUP'][i]} ne se superposent pas")

    if correspondance == False:
        print(f"le support {supports['NOMSUP'][i]} ne possède pas de foyer correspondant à sa numérotation")


# On vérifie que les foyers sont superposés à un support
for i in foyers.index:
    correspondance = False
    for j in supports.index:
        if foyers['geometry'][i] == supports['geometry'][j]:
            correspondance = True

    if correspondance == False:
        print(f"le foyer {foyers['NOMFOY'][i]} n'est pas superposé à un foyer")


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
