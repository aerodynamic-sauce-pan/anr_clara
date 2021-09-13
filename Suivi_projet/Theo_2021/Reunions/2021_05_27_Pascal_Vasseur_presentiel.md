# Travail
- Récap travail (cf. JdB).


# Mapping par bitterlich
- V1 de la construction de carte terminée :
  - Explication du fonctionnement complet
  - Incertitude croissante sur l'estimation de la largeur des arbres au fur et à mesure qu'ils s'éloignent
  - Petits soucis d'effets de bords quand on joue avec les paramètres à régler

## Evolution
- Pour l'instant le script marche pour de simages simples.
  - Il faut l'adapter pour utiliser une vraie carte de profondeur avec de vraies valeurs
  
- L'estimation de la largeur des arbres se base sur la règle de proportionnalité des triangles équivalents de Thalès en déterminant une longueur étalon pour chaque tranche de profondeur, basée sur le périmètre autour de la caméra pour une tranche de profondeur donnée. La largeur d'une image equirectanguliaire correspond au périmètre autour de la caméra à une certaine profondeur : c'est cette estimation qui nous permet de définir une relation section-de-pixels/longueur-dans-la-scène.
  - Pour améliorer la précision du périmètre, plutôt que de le pré-calculer pour chaque tranche de profondeur, on peut le calculer chaque fois que l'on repère un arbre dans la table d'occupation, dont on a précisément la distance à la caméra (sa depth). 
  - On peut également n'utiliser que les paramètres intrinsèques de la caméra pour déterminer la largeur d'un tronc à partir de l'angle d'ouverture qu'il faut pour le faire rentrer dans le champ focal de la caméra.

-  Il serait possible,  grâce à la connaissance à priori des données, de définir des prototypes de gaussiennes caractéristiques d'arbres pour chaque tranche de distance pour pouvoir décider ensuite d'écarter les gaussiennes correspondant à des faus positifs et qui seraient captées par sélection via seuil simple.

# Prochains objectifs
- Maintenant qu'on a les cartes, il faut ajouter la dimension temporelle et déterminer des mises à jours + renforcement des cartes à partir des déplacements du robot (de la caméra).
  - Creuser du côté de **Orb SLAM 3** qui est un *all-in-one package* embarquant des descripteurs et filtres pour déterminer des similitudes et déplacements entre 2 cartes sparses de points d'intérêts.
- (non prioritaire) Prendre en compte l'angle de bascule du drone, dont on peut récupérer l'information via le fichier de log d'airsim, pour prendre en compte les vues majoriatirement du sol ou du ciel, où la ligne d'horizon n'est pas dans le champ, et éviter des incohérences de matching de cartes
