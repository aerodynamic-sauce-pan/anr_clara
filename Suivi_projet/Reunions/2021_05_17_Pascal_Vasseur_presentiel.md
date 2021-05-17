# Travail
- Récap travail (cf. JdB).

## UE4 & script Charles : génération dataset
- Pas de réponse de Rida pour le benchmark des captures 6 caméras VS 1 caméras : relancer
- Pas de réponse de Charles pour le paramétrage d'UE4 : relancer
	- Réponse de Charles arrivée pendant la réunion sans qu'on s'en aperçoive : visio Mardi 18/05

# Articles
## SLOAM
- Les parties mathématique et algorithmiques valent le coup de se pencher dessus car il s'agit d'estimer la position d'arbres par une approche similaire au filtre de Kalman à base d'estimations pas mesures, de mises à jour et de correction.
- Les représentations des arbres et de la caméra sont peut-être trop poussées pour notre cas d'utilisation mais le backbone logique de l'article correspond bien à celui dont on aurait besoin de notre projet.

## Color based clustering
### Points essentiels
- L'article propose d'effectuer une segmentation sémantique pas clustering à partir de vecteurs de _features_ basés uniquement sur la couleur de l'image. La classification de ces clusters comme appartenants à la classe 'arbre' ou '_background_' se fait ensuite grâce à un arbre de décision.
	- 8 _feature vectors_ sont proposés en dérivant l'espace RGB, HSV ou encore en définissant des écarts d'intensité entre canaux de couleur.
	- 1 _feature vector_ est rajouté lorsqu'un cluster est identifié comme appartenant à un arbre (par comparaison avec les labels des données) : le max des valeurs de la transformée de Radon verticale du cluster (qui caractérisera une forte composante verticale).
- L'article propose un cas d'utilisation qui nous intéresse : le dénombrement d'arbre par échantillonage angulaire (méthode de Bitterlich)
	- La méthode utilise des règles de géométrie simples pour estimer le nombre d'arbres dans une zone (nécessite de connaitre la distance observateur-arbre)

### Critique
Les pistes de représentation des arbres et clusters sont intéressantes mais le peu de données et le manque de clareté & de détails de l'article remettent en doute sa crédibilité.

## Classification of tree species and stock volume estimation
### Points essentiels
- L'article propose deux choses : une segmentation sémantique efficace de certaines espèces d'arbres et une estimation du volume de bois dans une zone géographique donnée, le tout à partir uniquement d'images RGB.
	- Seg. Sem.: utilisation d'un U-Net pré-entraîné sur VGG16 (ImageNet)
	- Stock Volume : utilisation d'un modèle de représentation des arbres correspondant à une approximation ellipsoïde (le modèle est modifié par des perturbations propres à chaque espèce d'arbre qui possède des volumes différents). Cependant, il s'agit ici d'estimer un volume approximatif de bois sur une région, sans individualisation d'arbre.
	
### Critique
L'article est complet, toutes les informations concernant le modèle U-Net sont disponibles pour le re-créer, idem pour le _stock volume estimation_. De plus, un grand nombre d'études comparatives a été mise en place pour justifier de l'efficacité des choix techniques.

## Général
Des questions subsistent et des décisions devront être prises concernant la représentation des arbres (cylindres ? pos + rayon ?) et du sol (plan ? relief ?).


# Objectifs prochains
Tester la solution de Bitterlich sur ~5 plans (lignes de niveaux) des images équirectangulaires, autour de leur milieu vertical puisque c'est là que les déformations sont minimes, pour générer des grilles d'occupation. Cette piste de cartes d'occupation sera probablement à exploiter mais il faudra s'assurer de minimiser leur taille de stockage.
