# Travail
- Récap travail (cf. JdB).

## UE4
- AirSim
	- Vérifier que les output des images stéréo sont indépendantes gauche/droite et non fusionnées en une seule image.
	- Vérifier s'il est possible d'exporter nativement de simages equirectangulaires sinon toruver une script qui le fasse.
	- Vérifier s'il est possible de labelliser dles arbres par des couleurs comme sur UnrealCV sinon on va avoir un problème de conflit de version entre celle requise pour lenvironnement de GUIllaume + AirSim et celle requise pour l'env. de Dao + UnrealCV.

## Segmentation Sémantique
- Voir si le script de Dao performe toujours convenablement sur des données equirectangulaires annotées, mais implique qu'on puisse fournir de telles données (cf. dernier point de la section UE4).

## Méthodes de synchronisation
- Cette partie sera au finale assurée par l'équipe de Nice car cela n'est pas trivial compte tenu des caméra possédées :
	- Pas de genlock pour les caméra Ricoh.
	- Board de synchro arduino/raspberry pi existent pas impliqueraient de démonter les ricoh pour les mettre dessus ou d'obtenir d'autres objectifs.
	- D'autres tricks existent comme la synchronisation de l'allumage des caméra et l'augmentation du nombre de fps.
	- Enfin, il y a le matching de frames similaires mais ça ne permettra pas de fournir à la fois des images exactement similaires. Et si l'on produit une nouvelle image 'moyenne' on perd en précision visuelle.

## Autre
- Les sujets de thèses du labo vont bientôt arriver sur Adum.fr
- Une vague de sujets va arriver en Juillet pour un démarrage plus tôt que d'habitude en octobre : à scruter.
- Pascal a des contacts à Montpellier, Grenoble et Brest (Luc Jolin à l'ENSTA) -> lui soumettre des propositions de thèse et il me dira s'il connait du monde dans le labo en question

## Réunion
- Fin avril / Début mai il y aura une réunion de projet avec les équipes de Nice (et peut etre du Creusot).
	- Objectifs impératifs à atteindre : 
		- Obtenir une base d'images perspectives et/ou equirecangulaire de simulation de forêt
		- Pouvoir générer des cartes de disparité à partir des ces données
		- Pouvoir générer une seg. sem. satisfaisante sur ces données (en particulier les equirectangulaires.)
	- Objectifs optimaux:
		- Avoir une méthode de fusion de la disparité et de la seg. sem (superposition dans un premier temps)
