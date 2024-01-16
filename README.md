# Vérifications SIG
Ce script a pour but de tester la validité de données cartographiques, selon un cahier des charges donné.  
Pour cet exemple il s'agit de données de réseaux d'éclairage public (cables, supports, foyers). Ce type de script peut être utilisé suite à des travaux publics, avant envoi de l'export au concessionnaire de réseau, afin de vérifier que les informations géographiques sont conformes au cahier des charges établi par le concessionnaire.    


## Vérifications effectuées
[x] Le nom des éléments répond à un formalisme de type nn-nnn (exemple: 01-023)  
[x] Un foyer est supperposé à un support  
[x] Un support supporte un foyer de même numéro  
[x] Un support est connecté à l'extrémité d'un câble du même nom (s'il existe)  
[x] Plusieurs supports ne doivent pas avoir la même géométrie  
[x] Plusieurs cables ne doivent pas avoir la même géométrie  
[x] Plusieurs supports / foyers / cables ne peuvent pas avoir le même nom  
[x] Les câbles ne présentent pas d'auto-intersections, ni d'autre géométrie invalide  
[x] La couche emprise comprends un seul enregistrement  
[x] Tous les éléments supports, foyers et câbles sont à l'intérieur de l'emprise  
[x] Les champs de la couche emprise sont renseignés, le champ INSEE est numérique compris entre 1000 et 99999


Les vérifications effectuées ici sont données à titre d'exemple, des règles plus complèxes peuvent être envisagéees.  


