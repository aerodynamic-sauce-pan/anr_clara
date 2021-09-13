# Travail
- Récap travail (cf. JdB).

## Général
- On va partir du principe qu'on a nos images et caméras calibrées en utilisant directement les images extraites de UE4 comme si c'étaient les vraies

## Profondeur et Seg Sem
- Possible d'appliquer les 2 (le smodèles de Dao) sur les 6 vues perspective pour avoir une cubemap Depth/Seg Sem comme Charles dont il faudra comparer les perfs versus l'estimation de depth sur images equi

## Cartographie
- On commencera pas utiliser la vérité terrain (en ajoutant un petit bruit) pour la profondeur pour commencer la fusion sem/depth
- Pour une carte simplifiée :
	- Phase 1 : identifier uniquement les arbres avec les informations de position et diamètre
	- Phase 2 : vérifier qu'on arriver à se localiser dans la carte comme suit.
		- 1er parcours pour construire la carte
		- 2e parcours similaire pour vérifier qu'on arriver à se localiser dans la carte construite
- Voir les ressources de [David Filliat](https://perso.ensta-paris.fr/~filliat/Courses/index.html) pour se documenter sur les méthodes SLAM et récupérer des bouts de codes. On utilisera sûrement un filtre de Kalman pour estimer la carte où les arbres seront les balises.
	- On se limitera à un rayon proche car l'estimation à longue distance perd trop en précision
	- Dans la futur on pourra envisager de pré-charger les éléments lointains en estimant uniquement leur prosition approximative


# Visual Appearance Analysis of Forest Scenes for Monocular SLAM
- N'est qu'une comparaison d'algo SLAM connus, ne propose pas les méthodes.
- SFU dataset : [https://autonomy.cs.sfu.ca/sfu-mountain-dataset/](https://autonomy.cs.sfu.ca/sfu-mountain-dataset/) possède des données stereo en foret mais sur un chemin

# Autre

