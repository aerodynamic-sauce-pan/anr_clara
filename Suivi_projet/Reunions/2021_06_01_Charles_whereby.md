# UE4
- Identification arbres ID impossible car foret entière = entité accessible, donc à part refaire une monde à la main, pas moyen de récupérer les infos de chaque arbre.

- Avant, sans les LTU, il y avait 2 lissages sur les RGB : au moment du passage en cubemap et au moment du passage à l'equi
  -  Mais pas sûr que ce soit gênant : voir avec les réseaux

- Génération des vue equi sur le pc de Charles
  - Classique via Blender : de 12-15s pour RGB, Depth & SS
  - Dernière version à ce jour via LTU : RGB=1,6s + Depth=2,9s + SS=1,8s soit ~6s en tout. Donc 2x plus rapide.