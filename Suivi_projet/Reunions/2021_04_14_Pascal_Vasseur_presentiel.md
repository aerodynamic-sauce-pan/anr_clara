# Travail
- Récap travail (cf. JdB).

## UE4
### Guillaume & AirSim
- AirSim :
	- Comporte une API C++ et une Python qui contiennent toutes deux des problèmes car AirSim est basé sur UnrealCV, est donc récent, et comporte plusieurs bugs et issues non résolues
	- Blocage au niveau de l'utilisation du mode Computer Vision d'AirSim
	- La plugin comporte par défaut une visualisation de la profondeur et d'une segmentation sémantique des groupes d'objets (végétation, sol, ciel, liquides...) mais aucune idée de si c'est possible de récupérer ces flux et quand bien même, la segmentation ne permet pas la distinction individuelle des arbres. On devrait plutôt utiliser l'API en mode Computer Vision qui permet de changer les textures à partir des ID des objets (de leur 'meshes') mais pour l'instant il y a des blocages.
- Environnement Guillaume :
	- Possibilité d'attribuer une texture à couleure unie aux objets : sachant qu'il y a plusieurs prototypes d'arbres, si la distribution des arbres est riche, on pourrait modifier à la main les couleurs des prototypes (une douzaine) et obtenir une segmentation 'native' ddans l'éditeur d'UE4
- Solution dégradée : acquérir des images de points de vues statiques

### Dao & UnrealCV
- Ne pas abandonner au cas où l'aspect expérimental de AirSim bloque complètement le projet
- L'environnement de Dao semble corrompu d'après les logs UE4 : dans l'attente d'une réponse de sa part
- UnrealCV est à la base de AirSim mais plus vieux : problèmes de compatibilité avec la version d'UE4 utilisée pour l'environnement de Guillaume

## Autre
- Contacts certainement utiles : Rida + bientot un postDoc pour l'aspect dev
- Demande si Guillaume a pu faire des acquisitions et est-ce qu'ils s'en sont sortis avec le calibrage

# Réunion
- Prochain point : Lundi 19/04 matin
