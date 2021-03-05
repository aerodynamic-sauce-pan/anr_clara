# Thèse
Caméra evenementielle -> Omnidirectionnelle pour la navigation robot
Surtout dev algo derrière, pas bcp d'utilisation capteur

- Sujet presque soumis, en décembre. Les autres sujets resteront proches, ex : à partir d'un modèle 3D HD, faire du recalage from données évenementielles (estimer position caméra). Recalage 3D existe depuis longtemps l'enjeux est de le faire avec des données minimales d'un coté et HD de l'autre en temps réel sur système faiblement performant.

- Autre projet soumis ne lien avec le médical, aussi du recalage. Pour implant cochléaire, les interventions robotisées need poser repères sur patient comme motion capture. Là on n'aurait besoin que du flux vidéo via recalage, et s'viter modélisation 3D du patient.

- Les projets sont soumis à financement donc certains seront acceptés, d'autres non. Le premier though nécessite engagement étudiant rapide.

# Stage

- **Second sujet** :
	- Estimation de pose de caméra en se basant sur droites détectées dan l'environnement. Destiné à robotique intérieurs ou urbaine : from prise caméras, estimation position relatives des caméras par extraction des droites. Centrale inertielle associées aux caméras => on connait le tangage des cam => réduit le nb de droites à estimer => algo robustes d'estimation pas trop lents.
	- La théorie a déjà été développée. Un partenaire en Chine développe des choses. Idée ici = reconstruire 3D from estimation de pose. Pour l'instant ça marche sur simulation, pas images réelles.
