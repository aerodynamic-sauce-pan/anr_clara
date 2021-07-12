<center><h1>CR de réunion d'avancement de projet</h1></center>

- **Participants** : Théo Larcher, Pascal Vasseur
- **Date** : 12/07/2021
- **Voie** : Présentiel 

## Travail
- Récap travail (cf. JdB).

## Mapping
- Vue polaire/radar laissée de côté au profit d'une vue en référentiel cartésien car instabilité dans la visualisation vérité terrain
    - Sera peut-être reprise si j'arrive à trouver la source du problème
- Démonstration de l'affichage temps réel du drone se déplaçant sur la carte d'arbres issue de la vérité terrain
    - Temps réel
    - Ajouter l'affichage de la trace du drone
- Démonstration de la carte cartesienne des prédictions des arbres
    - Revoir les axes
- Présentation des premières métriques
    - Problème de dépassement de bornes avec les angles à cause d'un offset dans `get_angle2D` pour satisfaire pyplot
	- Problème dans l'erreur sur les diamètres : beaucoup trop grande
	- Les positions sont globalement cohérentes mais revoir les axes de l'affichage bitterlich

## Objectifs prochains
- Régler les bugs et bizarreries mentionnées précédemment
- Produire une précision et un recall
- Adapter l'affichage des rédictions à un enchaînement d'images pour animation temps réel
- Produire des estimations de recalage pour decripteurs
- Entraîner et tweaker notre réseau de reconnaissance d'arbres sur le monde label