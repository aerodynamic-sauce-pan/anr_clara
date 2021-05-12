# Travail
- Récap travail (cf. JdB).

## Général
- Priorité : réussir la distinction individuelle d'arbres avant le SLAM
	- Etat de l'art
	- Plane sweeping


## UE4 & script Charles : génération dataset
- Stand-by car paramétrisation de l'environnement de manière à corriger les couleurs de l'equi : impossible
	- En attente d'une réponse de Charles pour faire le paramétrage en visio ou conclure de récupérer son environnement
	- En attente de Rida pour récupérer ses résultats sur le benchmark de sa solution à 6 caméras fixes avec look-up table VS la notre à 1 caméra tournante
		- Si une différence notable est constatée en faveur de sa méthode : voir avec lui pour recompiler AirSim à la main
- Constatation déchirure sur images équirectengulaire pour une dimension de 1000x500 à partir de perspectives 900x900
- Prendre des perspectives de côté `c` pour générer des équirectangulaires de tailles `4*c x 2*c` n'est pas suffisant pour fournir une bonne qualité de détail
- Rida a partagé sa Look-Up Table et un script de navigation dans le cas où l'on aurait re-compilé AirSim pour intégrer 6 caméras

# Articles
## SLOAM
- Rdv la semaine prochaine pour revenir sur les maths avec Pascal

## Articles Rida
A lire et synthétiser :
- [Classification of tree species and stock volume estimation in ground forestimages using Deep Learning](https://www.sciencedirect.com/science/article/abs/pii/S0168169919308713)
- [Color Based Clustering for Trunk Segmentation](https://ieeexplore.ieee.org/document/8439358)


# Objectifs prochains
- Pour la semaine prochaine, aboutir à une sélection d'idées voire de prototypes d'idées
	- Créer des cahiers de recherche

