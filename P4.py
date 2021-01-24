# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 14:15:13 2020

@author: ikhla
"""
from sys import maxsize
import time

# Il s'agit de la matrice indiquant le nombre de possibilités d'aligner
# 4 jeton à la suite. Pour une grille de jeu 6*12 il s'agit d'une 
# matrice mirroir.

matrice_possibilité = [[3,4,5,7,7,7],[4,6,8,10,10,10],[5,8,11,13,13,13]]

def Possibilité(ligne,colonne):
    if(ligne > 2) : ligne = 5 - ligne
    if(colonne > 5) : colonne = 11 - colonne
    return matrice_possibilité[ligne][colonne]


def Grille(n,p):
    grille = [["-" for i in range(p)] for i in range(n)]
    return grille


def Affichage(grille):
    for i in range(len(grille)-1,-1,-1):
        for col in grille[i]:
            print("",col,end =" |")
        print("")
    print()
    for i in range(1,13) : print("",i,end="  ")
    
    
def Tour(grille):
    countX = 0
    countO = 0
    for ligne in grille:
        for col in ligne:
            if (col == "X") : countX += 1
            elif (col == "O") : countO += 1
    if countX == countO : return "X"
    else : return "O"
    
    
def Jouer(grille,col):
    copy = [list(ligne) for ligne in grille]
    for ligne in copy:
        if (ligne[col] == "-"):
            ligne[col] = Tour(grille)
            break
    return copy


def Possible(grille):
    possible = []
    for col in range(12):
        for i in grille:
            if(i[col] == "-"):
                possible.append(col)
                break
            
    milieu = int(len(possible)/2)
    l1 = possible[milieu-1::-1]
    l2 = possible[milieu:]
    resultat = []
    for i in range(len(l1)):
        resultat.extend([l1[i], l2[i]])
    if(len(possible) % 2 != 0): resultat.append(l2[-1])
    return resultat

# Renvoi l'index de la ligne sur laquelle se situe le pion
def Ligne(grille,col):
    index_ligne = -1
    for ligne in grille:
        if(ligne[col] != "-"): index_ligne += 1
        else : break
    return index_ligne
    

def Victoire(grille,col, choix = "X"):
    compte = 0
    precedent = ""
    resultat = None
    
# On a récupérer la ligne sur laquelle est la dernière pièce
    line = Ligne(grille,col)
    
    for i in range(1):
        #Condition colonne
        for ligne in grille:
            if (compte == 4 and precedent != "-") : 
                resultat = precedent
                break
            elif (precedent == ligne[col]): compte += 1
            else :
                precedent = ligne[col]
                compte = 1
        if (compte == 4 and precedent != "-") : 
            resultat = precedent
            break
        
        
        #Condition ligne
        compte = 0
        precedent = ""
    
        for i in range(12):
            if (compte == 4 and precedent != "-") : 
                resultat = precedent
                break
            elif (precedent == grille[line][i]): compte += 1
            else :
                precedent = grille[line][i]
                compte = 1
        if (compte == 4 and precedent != "-") : 
            resultat = precedent
            break
        
        
        #Condition Diagonale Montante Droite
        compte = 0
        precedent = ""
        
        ligneBas, colonneBas = 0, col - line
        if (colonneBas < 0) :
            ligneBas = - colonneBas
            colonneBas = 0
            
        diagonale = []
        Nb_case = None
        
        if( colonneBas == 0 ): Nb_case = 6 - ligneBas 
        elif( colonneBas >= 1 and colonneBas <= 6 ): Nb_case = 6
        else : Nb_case = 12 - colonneBas
            
        if( Nb_case >= 4) :
            for i in range (Nb_case):
                diagonale.append(grille[ ligneBas + i ][ colonneBas + i ])
    
            for j in range(len(diagonale)):
                if (compte == 4 and precedent != "-") : 
                    resultat = precedent
                    break
                elif (precedent == diagonale[j]): compte += 1
                else :
                    precedent = diagonale[j]
                    compte = 1
        				
        if (compte == 4 and precedent != "-") : 
            resultat = precedent
            break
        
        
        #Diagonale Montante Gauche
        compte = 0
        precedent = ""
        
        ligneBas, colonneBas = 0, col + line
        if (colonneBas > 11) :
            ligneBas = line - (11 - col)
            colonneBas = 11
            
        diagonale = []
        Nb_case = None
        
        if( colonneBas == 11 ): Nb_case = 6 - ligneBas 
        elif( colonneBas >= 5 and colonneBas <= 10 ): Nb_case = 6
        else : Nb_case = colonneBas + 1
            
        if( Nb_case >= 4) :
            for i in range (Nb_case):
                diagonale.append(grille[ ligneBas + i ][ colonneBas - i ])
    
            for j in range(len(diagonale)):
                if (compte == 4 and precedent != "-") : 
                    resultat = precedent
                    break
                elif (precedent == diagonale[j]): compte += 1
                else :
                    precedent = diagonale[j]
                    compte = 1
        				
        if (compte == 4 and precedent != "-") : 
            resultat = precedent
            break
  
    
    if (resultat == choix) : return 100000
    elif (resultat == None) : return 0
    else : return -100000


def Minimax(grille, choix):
    Actions = Possible(grille)
    grille_actions = [Minvalue(Jouer(grille,a),a,-maxsize,
                               maxsize,choix,3) for a in Actions]
    #On stock les index de chaque action ayant un heuristique max
    
    
    provisoire = []
    for i in range(len(grille_actions)):
        if (grille_actions[i] == max(grille_actions)):
            provisoire.append(i)
    
    if(len(provisoire)>=2):
        #Pour chaque actions on calcule le nombre de possibilités de gagner
        Possibilitees = { Actions[i] : 
                         Possibilité(Ligne(grille,Actions[i]), Actions[i])
                         for i in provisoire}
        
        #Enfin, si deux actions ont le meme heuristique et le même
        #nombre de possibilités de gagner, on prend celle plus proche
        #   du milieu.
        milieu = 5.5
        for action in Possibilitees.keys():
            if(abs(5.5 - action) < milieu) :  
                milieu = abs(5.5 - action)
                resultat = action
        return resultat
    else :
        return Actions[provisoire[0]]

    return Actions[grille_actions.index(max(grille_actions))]
 
   
def Maxvalue(grille,col,alpha,beta,choix,profondeur):
    if (Terminal(grille,col) or profondeur == 0): 
        A = Victoire(grille,col,choix)
        if(A==0): return Score_algo(grille,choix)
        else : return (profondeur+1)*Victoire(grille,col,choix)
        
    valeur = - maxsize
    for coup in Possible(grille):
        valeur = max(valeur,Minvalue(Jouer(grille,coup),coup,
                                     alpha,beta,choix,profondeur-1))
        if (valeur >= beta) : return valeur
        alpha = max(alpha,valeur)
    return valeur


def Minvalue(grille,col,alpha,beta,choix,profondeur):
    if (Terminal(grille,col) or profondeur == 0):
        A = Victoire(grille,col,choix)
        if(A==0): return Score_algo(grille,choix)
        else : return (profondeur+1)*Victoire(grille,col,choix)
    valeur = maxsize
    for coup in Possible(grille):
        valeur = min(valeur,Maxvalue(Jouer(grille,coup),coup,
                                     alpha,beta,choix,profondeur-1))
        if (valeur <= alpha) : return valeur
        beta = min(beta,valeur)
    return valeur


def Scoring(fen,choix,score):
    
    if choix=="X": adv = "O"
    else : adv = "X"
    
    if fen.count(choix) == 4: score += 200
    elif fen.count(choix) == 3 and fen.count("-") == 1:
        score += 40
    elif fen.count(choix) == 2 and fen.count("-") == 2:
        score += 8
    
    if fen.count(adv) == 3 and fen.count("-") == 1:
        score -= 50
    if fen.count(adv) == 2 and fen.count("-") == 2:
        score -= 10
    
    return score


def Score_algo(grille,choix):
    
    score = 0
    # Ligne
    for ligne in range(6):
        row = grille[ligne]
        for col in range(9):
            fen = row[col:col+4]
            score += Scoring(fen,choix,0)
            
    # Colonne    
    for col in range(12):
        column = [grille[i][col] for i in range(6)]
        for row in range(3):
            fen = column[row:row+4]
            score += Scoring(fen,choix,0)
            
    # Diagonale montante droite
    for ligne in range(3):
        for col in range(9):
            fen = [grille[ligne+i][col+i] for i in range(4)]
            score += Scoring(fen,choix,0)
            
    # Diagonale montante gauche        
    for ligne in range(3):
        for col in range(11,3,-1):
            fen = [grille[ligne+i][col-i] for i in range(4)]
            score += Scoring(fen,choix,0)
                
    return score
    
        
def Terminal(grille,col):
    if (Victoire(grille,col) != 0) : return True
    elif ("-" not in grille[5]) : return True
    else : return False
        
    
def Mode():
    choix = input("Si vous souhaitez-commencer, tapez 'y' sinon tapez n : ")
    if choix == "y" : adv = "O"
    else : adv = "X"
    return adv


def Exo():
    ia = Mode()
    grille = Grille(6,12)
    ia_jeton = 0
    x = 0
    y = 0
    compteur = 0
    Temps = 0
    while (not (Terminal(grille,x) or Terminal(grille,y)) and compteur!= 42 ): 
        if (Tour(grille) == ia):
            
            debut = time.time()
            y = Minimax(grille,ia)
            fin = time.time()
            grille = Jouer(grille, y)
            print("\n")
            Temps += (fin-debut)
            Affichage(grille)
            print("\n")
            print("L'ia a joué en colonne ",y+1)
            print("Temps de jeu : ", fin-debut)
            compteur += 1
            ia_jeton +=1
        else :
            if(not Terminal(grille,y)):
                x = eval(
                    input(("Entrez un chiffre entre 1 et 12 : ")))-1
                while (grille[Ligne(grille,x)][x] == 5) :
                   x = eval(
                    input(("Entrez un chiffre entre 1 et 12 : ")))-1    
                grille = Jouer(grille, x)
                Affichage(grille)
                print("")
                compteur += 1
    print("fin de jeu.")
    print("Temps final:",Temps)
    print("IA :",ia_jeton,"jetons\nJoueur :",compteur-ia_jeton,"jetons")


Exo()