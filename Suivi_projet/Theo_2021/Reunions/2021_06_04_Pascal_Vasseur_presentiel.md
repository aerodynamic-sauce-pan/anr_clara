# Travail
- Récap travail (cf. JdB).


# Mapping par bitterlich
- Améliorations
  - Récupération de la profondeur des arbres détectés à la source : améliore un peu l'estimation de grosseur
  - Plus le pas de largeur est fin, meilleure est la précision de la grosseur : impact significatif. Best case scenario : pas de largeur = largeur de l'image.
  - Superpositition des estimations de (position + grosseur) sur la vue equirectangulaire RGB : quelques bizarreries d'affichage au niveau des moustaches représentant la grosseur, mais globalement les arbres au premier plan sont plutôt bien situés. Les grosseurs restent assez peu satisfaisantes.

# UE4
- J'ai contacté les propriétaires de notre environnement forestier 3D Redwood Forest et ils m'ont dit qu'il était à priori possible de récupérer les propriétés d'arbres instanciés par génération procédurale en me redirigeant vers le post forum d'une personne ayant cherché à faire la même chose. Cette personne donne son script C++ pour y arriver : si ça marche on aura notre GT.

# ORB-SLAM 3
- Papier très solide avec de grosses promesses
- Installation hectique, surtout au niveau d'OpenCV, en cours de résolution...