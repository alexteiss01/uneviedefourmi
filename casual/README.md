# **Projet : "Une vie de fourmi"**

## **Problématique**

Dans ce projet, nous avons simulé le **déplacement d'une colonie de fourmis** à travers une fourmilière. L'idée est simple : les fourmis commencent dans une salle appelée **Vestibule**, qui est l'entrée de la fourmilière, et elles doivent atteindre une autre salle, le **Dortoir**, située plus loin dans la structure.

La **difficulté** réside dans le fait que :
- Chaque salle a une **capacité limitée**, donc un nombre maximum de fourmis qui peuvent y séjourner.
- Les fourmis ne peuvent se déplacer que dans des **salles adjacentes** (qui sont distantes d'une seule unité).
- Toutes les fourmis doivent arriver au Dortoir **avec le minimum d'étapes**, en respectant les contraintes de capacité et de distance.

Le but du projet est donc de **modéliser** cette fourmilière, d'**optimiser le déplacement** des fourmis et de **visualiser** leur progression à travers les salles jusqu'à ce que toutes aient atteint le Dortoir.

## **Solution Apportée**

Pour répondre à ce problème, deux classes ont été utilisées pour modéliser la fourmilière et les déplacements des fourmis : 

### **Classe _Ant_ (Fourmi)**

Chaque fourmi est représentée par un objet de la classe **Ant**, et chaque objet a deux attributs principaux :
- **number** : Un numéro unique qui identifie chaque fourmi. C'est comme un identifiant ou pour chaque fourmi.
- **lieu** : C'est l'index de la salle (ou nœud) dans laquelle la fourmi se trouve actuellement. Par exemple, si une fourmi est dans la première salle de la liste des nœuds, son `lieu` sera 0.

#### **Méthode principale : `move()`**

La méthode `move` est celle qui permet à la fourmi de se déplacer d'une salle à une autre, selon certaines règles que nous avons définies. Voici comment elle fonctionne :

1. **Récupération de la salle actuelle** : 
   - La fourmi commence par identifier dans quelle salle (ou nœud) elle se trouve actuellement, en accédant à la salle dans la liste des nœuds à l'index `self.lieu`. Cela lui permet de savoir combien de fourmis sont déjà présentes dans la salle et quelles sont les salles adjacentes.

2. **Détection des mouvements possibles** :
   - Ensuite, la fourmi analyse les nœuds adjacents (c'est-à-dire ceux dont la distance est de 1 par rapport à la salle actuelle). Elle ne peut se déplacer que vers une salle qui a encore de la place, donc elle vérifie que le nombre de fourmis dans chaque nœud adjacent est inférieur à la capacité maximale de ce nœud.

3. **Choix du nœud de destination** :
   - Si plusieurs salles adjacentes sont disponibles, la fourmi choisit celle qui est **la plus proche de la distance 0** (le dortoir). Cette logique simule une stratégie d'optimisation où la fourmi cherche à se rapprocher du dortoir à chaque étape.

4. **Mise à jour des informations** :
   - Une fois le nœud de destination choisi, la fourmi met à jour sa position en passant de l'index du nœud actuel à celui du nœud de destination. De plus, elle diminue le nombre de fourmis dans la salle qu'elle quitte et augmente celui de la salle où elle arrive.

### **Classe _Node_ (Nœud)**

Un **nœud** représente une salle dans la fourmilière. Chaque salle a des caractéristiques propres qui influencent la façon dont les fourmis peuvent se déplacer d'une salle à une autre. Voici les attributs principaux d'un nœud :

- **name** : Le nom de la salle, qui permet de l'identifier facilement. Par exemple, le Vestibule pourrait avoir comme nom "Sv" et le Dortoir "Sd".
- **capacity** : La capacité maximale de la salle, c'est-à-dire le nombre de fourmis que la salle peut accueillir en même temps. Si ce nombre est atteint, plus aucune fourmi ne pourra entrer dans cette salle avant que d'autres ne partent.
- **dist** : La distance relative de la salle dans la fourmilière. Cette distance est utilisée pour savoir à quel point la salle est proche du dortoir (plus la distance est petite, plus la salle est proche de "Sd").
- **ants** : Le nombre actuel de fourmis présentes dans la salle. Cet attribut est mis à jour à chaque fois qu'une fourmi entre ou sort de la salle.

Cette classe est très simple, mais elle est essentielle pour garder une trace du **nombre de fourmis présentes** dans chaque salle, et pour **vérifier si une salle a atteint sa capacité maximale**.

## **Fichier `main.py`**

Le fichier `main.py` est celui qui orchestre toute la simulation. Il va charger les nœuds (salles), initialiser les fourmis, les faire se déplacer dans la fourmilière et, enfin, visualiser le tout sous forme de graphe.

### **Fonction `charger_nodes()`**

Cette fonction permet de **charger les nœuds** (ou salles) depuis un fichier texte (`infograph.txt`) qui contient toutes les informations nécessaires sur chaque salle : 
1) **Nom** (pour identifier la salle),
2) **Capacité** (combien de fourmis peuvent entrer),
3) **Distance** (sa position relative dans la fourmilière par rapport au Dortoir).

Pour chaque ligne du fichier texte, on crée un objet **Node**, qui est ensuite ajouté à une liste représentant toute la fourmilière.

### **Initialisation des fourmis**

Une fois les nœuds créés, on initialise les fourmis. Par exemple, on crée 10 fourmis (de 0 à 9), et on les place toutes dans le **Vestibule** (qui est le premier nœud dans la liste des nœuds). On met ensuite à jour le nombre de fourmis présentes dans le Vestibule.

### **Fonction `move_ants()`**

Cette fonction est essentielle pour la simulation, car elle fait bouger toutes les fourmis à chaque étape. Chaque fourmi utilise sa méthode `move` pour choisir un nœud vers lequel se déplacer, en respectant les règles de distance et de capacité.

### **Fonction `all_ants_in_sd()`**

Cette fonction permet de vérifier si **toutes les fourmis** sont arrivées dans le **Dortoir** (le nœud dont le nom est "Sd"). Elle est utilisée pour savoir quand arrêter la simulation.

### **Simulation des étapes**

Ici, on lance la boucle principale de la simulation. Tant que toutes les fourmis ne sont pas dans le dortoir, la boucle continue :

1. **Boucle while** : Elle s'exécute tant que toutes les fourmis ne sont pas arrivées dans le Dortoir.
2. **Appel de `move_ants()`** : À chaque itération, on déplace toutes les fourmis.
3. **Affichage des étapes** : À chaque étape, on affiche le nombre de fourmis présentes dans chaque salle pour voir l’évolution en temps réel.
4. **Incrémentation du compteur d'étapes** : On garde une trace du nombre d’étapes nécessaires pour que toutes les fourmis arrivent dans le Dortoir.

### **Visualisation graphique avec _NetworkX_**

Pour rendre la simulation plus claire, nous utilisons la bibliothèque **NetworkX** afin de représenter la fourmilière sous forme de **graphe**. Chaque salle de la fourmilière est un **nœud**, et les **tunnels** qui relient ces salles sont des **arêtes**.

#### **Étapes de la création du graphe** :

1. **Création du graphe** :
   - Un objet graphe `G` est créé pour représenter la fourmilière.

2. **Ajout des nœuds** :
   - Chaque salle est ajoutée au graphe en tant que nœud avec des attributs comme le nom, la capacité et la distance.

3. **Ajout des arêtes** :
   - Les tunnels entre les salles sont représentés par des arêtes. Si une salle est adjacente au Dortoir (distance de 1), une arête est ajoutée entre cette salle et le Dortoir. Les autres salles sont reliées par des arêtes selon leur proximité (distance de 1 entre elles).

4. **Positionnement des nœuds** :
   - Nous utilisons l'algorithme **spring layout** pour bien disposer les nœuds et éviter les chevauchements. Cela garantit que le graphe reste lisible et bien organisé.

5. **Affichage du graphe** :
   - Les noms des salles sont affichés, et les nœuds sont colorés. Le graphe est dessiné avec des nœuds de taille fixe et une couleur uniforme. Les arêtes relient les salles, et le tout est visualisé avec `plt.show()`.

## **Conclusion**

Le projet a permis de modéliser et de simuler avec succès le **déplacement d'une colonie de fourmis** à travers une fourmilière, en respectant les contraintes de **capacité des salles** et de **distances** entre elles. Grâce à l'algorithme mis en place, l'intégralité des fourmis a pu rejoindre le dortoir en un **minimum d'étapes**, et la visualisation sous forme de graphe a fourni une **représentation claire** de la structure de la fourmilière.




