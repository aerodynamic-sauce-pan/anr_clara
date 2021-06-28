<center><h1>CR de réunion d'avancement de projet</h1></center>

- **Participants** : Théo Larcher, Pascal Vasseur
- **Date** : 28/06/2021
- **Voie** : Présentiel 

## Travail
- Récap travail (cf. JdB).
- Retour sur les points abordés dans le CR précédent envoyé par mail

## ORB-SLAM3
- Les keyframes correspondent à des images clefs d'ouverture et fermeture de 'boucles'. Lorsque que le robot repasse par des endroits, l'algo note des images de référence pour comparer les positions et ajuster ses paramètres d'estimations.
- Le mapping se perd parfois lorsq des avancées en profondeurs mais les modèles de caméra utilisés dans les expériences ne correspondent pas aux déformations des vues equi donc c'est prévisible. Le modèle de caméra pinhole perspective résiste mieux que le modèle KannalaBrandt8 fisheye.
- Par défaut, le nuage de point n'est pas exporté autrement que visuellement

## Mapping
- Développer l'estimation de l'algo de mapping par les vérités terrain sorties d'UE4

## Prochains objectifs
- La question de la mise à, jour de la carte dans le temps demeurre :
  - Utiliser OBR-SLAM3 sur des sections d'images ?
    - Il faudrait fouiller dans le code où extraire les bonnes données,, cela peut être dur sachant que le projet est très gros et que tout est en C++
  - Kalman maison ?