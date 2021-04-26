# Travail
- Récap travail (cf. JdB).

## UE4
- Des questions demeurent pour compléter le 'monde label' car très peu de tuto / documentation sur le sujet -> voir avec Charles et Rida.
- L'environnement de Dao fonctionne, on pourrait l'utiliser mais il faudrait s'occuper des rajouter des caméras pour avoir une vue 360 et ré-utiliser le script de Charles (cubemap -> sphère -> vue équirectangulaire)

## 360SD-Net
- Entrée 'polar angle' correspond à la valeur de theta\_t dans l'article pour la vue du dessus. Ils en extraient des features qu'ils concatènent par convolution avec les features visuelles des vues top/bottom, ce qui les pondèrent en fonction de leur proximité du sol ou du plafond (~ leur déformation). Ensuite, la déformation spatiale est prise en compte par le modue ASPP qui convolutionne les features, issues de la fusion des features de polar angle et des vues top/bottom, avec des _sparse kernels_ qui caractérisent des déformations d'autant plus importantes que leur _kernel_ est dilaté (5 niveaux dilatation).

## Cartographie

- Objectif : modélisation 3D du sol + localisation 2D des arbres avec leur diamètre
- La stéréo et l'estimation de profondeur nous donneront le relief du sol. Voir pour appliquer la segmentation sur chaque vue pour plus de précision.
- Article utilisant des techniques SLAM (mmonocular) : [Visual  Appearance  Analysis  of  Forest  Scenes  for  Monocular  SLAM](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8793771)

# Réunion
- Jeudi 29/04 (réunion rapide d'équipe pour faire le point sur les objectifs de chaque projet, les ressources utilisées, développées, et celles qui nous intéresseraient)

# Autre
- Je serai en télétravail sur Rouen dès Mercredi 28/04 matin jusqu'à Vendredi 30/04 inclus
