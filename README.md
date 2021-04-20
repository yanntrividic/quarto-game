# quarto-game

**Authors**\
Elie Duboux\
Yann Trividic

A Python implementation of the board game *Quarto!* with an artificial intelligence playing against the user. This program is partly based on the work of Mohrmann et al. (2013) and on the video tutorial of the YouTube channel *Tech with Tim*

## Structure des états et représentation PEAS

Jeu à somme nulle, information complète; nombre d'états possibles de l'ordre de 16!^2 sans compter les symétries et les
parties finies. L'exploration complète de l'arbre est donc impossible.




## PEAS

#### Mesure de performance

L'agent développé dans le cadre de ce projet est un **agent focalisé sur l'utilité**. C'est-à-dire que l'agent est doté d'une fonction d'utilité qu'il va chercher à maximiser grâce à ses actions. L'idée est de calculer récursivement le résultat de la fonction d'évaluation de chaque état de l'arbre des possibilités du jeu à partir de l'état courant.

#### Environnement
Observable, déterministe, épisodique, statique et discret
Si deux IA jouent l'une contre l'uatre, l'environnement peut être considéré comme un système multiagent en compétition **(voc ?)**

#### Actionneurs

Les actionneurs sont les décisions concernant où placer une pièece et quelle pièce choisir

#### Capteurs

Les capteurs sont les représentations logiques de la grille quatre par quatre avec les positions des seize pièces.


## Algorithme
Facteur de branchement moyen : 8.5 (somme de 1 à 16 sur 16)
Il est difficile de trouver quel coup doit être examiné en premier. Or, pour une efficacité maximale, il faudrait qu'alpha-beta puisse le faire.

#### Heuristique

####


## References

*An artificial intelligence for the board game* 'Quarto!' *in Java.*, Mohrmann, Jochen & Neumann, Michael & Suendermann, David. (2013). 141-146. 10.1145/2500828.2500842.\
[www.researchgate.net/publication/261848662](https://www.researchgate.net/publication/261848662)

*Python/Pygame Checkers Tutorial*, Tech with Tim (2020)\
<https://www.youtube.com/playlist?list=PLzMcBGfZo4-lkJr3sqpikNyVzbNZLRiT3>

*Découverte du langage Go pour ma deuxième semaine d'intégration : Go Go Quarto Ranger !*, Julien Mattiussi (2018)\
<https://marmelab.com/blog/2018/10/09/go-go-quarto-ranger.html>

*Quarto et intelligence artificielle*, Marien Fressinaud (2013)\
<https://marienfressinaud.fr/quarto-et-intelligence-artificielle.html>
