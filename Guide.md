*Plan du programme*

# **Substitution**

1. permettre à l'utilisateur de choisir parmi tous les produits OFF (en filtrant d'abord par catégorie)
    - consultation API OFF ?
    - copie locale de la BD OFF ?
2. récupérer le nutriscore associé à l'aliment choisi par l'utilisateur
3. trouver un produit de la même famille avec un nutriscore meilleur
4. soumettre la proposition à l'utilisateur

# **Lieu de vente**
1. L'affichage des détails d'un aliment permet de proposer des lieux où l'acquérir
    - renvoi vers drive de supermarché ? Amazon ? 

# **SVG**

1. Le programme propose à l'utlisateur de svg le résultat de sa recherche. 
    
    - recherche + proposition associée à stocker dans BD du prog 
    
2. L'utilisateur peut consulter son historique de recherche.

    - BD du prog à consulter


# **Difficultées rencontrées**
*API OFF*
- Compréhension de l'organisation de l'API OFF. De multiples critères non forcément bien renseignés ni renvoyé dans
le même ordre par l'API => impact sur le traitement des données extraites par la suite

- Utilisation du module Requests et paramétrage pour obtenir une quantité controlée de produits, avec que certains 
critères en particulier. En particulier il a fallut trouver la bonne façon d'écrire le paramètre fields pour 
qu'il intègre tous les critères voulus.

- Implémentation de la classe

*Base de donnée*
- Import du module msql-connector-python. Porte un nom qui n'est pas le même sous lequel il est utilisé dans 
le programme. Par ailleurs quelque difficulté d'installation dans l'environnement pipenv.

- Définir l'ordre d'intégration des données. D'abord les catégories de produits. Ensuite les produits auxquels
il faut intégrer la catégorie à laquelle ils correspondent.