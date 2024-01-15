import geopandas as gpd
from shapely.geometry import Point, LineString
import re
import os

def valider_nom_regex(data_set, data_set_name, regex):
    for nom in data_set:
        if not regex.match(nom):
            print(f"la valeur {nom} n'est valide pour un {data_set_name}")


path = os.path.realpath(__file__) 
dir = os.path.dirname(path) 
dir_data = dir.replace('sources', 'test_data')

supports = gpd.read_file(dir_data + "/supports.shp")
foyers = gpd.read_file(dir_data + "/foyers.shp")
cables = gpd.read_file(dir_data + "/cables.shp")

print(supports)

# pour test si nom de type nn-nnn (ex: 01-234)
regex = re.compile(r'\d{2}-\d{3}')

valider_nom_regex(supports['NOMSUP'], 'support', regex)
valider_nom_regex(foyers['NOMFOY'], 'support', regex)
valider_nom_regex(cables['NOMCAB'], 'support', regex)

# On vérifie que les supports sont sous le foyer du même nom
for i in supports.index:
    correspondance = False
    for j in foyers.index:
        print("support = " + supports['NOMSUP'][i] + " , foyers = " + foyers['NOMFOY'][j])

        if supports['NOMSUP'][i] == foyers['NOMFOY'][j]:
            print('le support ' + supports['NOMSUP'][i] + ' possède un foyer correspondant')
            correspondance = True

            if supports['geometry'][i] != foyers['geometry'][j]:
                print('Le support et le foyer de même nom ' + supports['NOMSUP'][i] + ' ne se superposent pas')

    if correspondance == False:
        print('le support ' + supports['NOMSUP'][i] + ' ne possède pas de foyer correspondant à sa numérotation')

