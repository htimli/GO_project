import time
import Goban
from random import choice

def randomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles. Pour avoir un choix au hasard, il faut
    construire explicitement tous les mouvements. Or, generate_legal_moves() peut nous donner un itérateur (quand on
    l'utilise avec pychess).'''
    return choice(list(b.generate_legal_moves()))

def deroulementRandom(b):
    '''Déroulement d'une partie de go au hasard des coups possibles. Cela va donner presque exclusivement
    des parties très longues et sans gagnant. Cela illustre cependant comment on peut jouer avec la librairie
    très simplement.'''
    print("----------")
    b.prettyPrint()
    if b.is_game_over():
        print("Resultat : ", b.result())
        return
    b.push(randomMove(b))
    print("eval_board : ",eval_board(b))
    deroulementRandom(b)
    b.pop()
"""
board = Goban.Board()
deroulementRandom(board)
"""
''' Exemple de déroulement random avec weak_legal_moves()'''

def weakRandomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles mais attention, dans ce cas
    weak_legal_moves() peut renvoyer des coups qui entrainent des super ko. Si on prend un coup au hasard
    il y a donc un risque qu'il ne soit pas légal. Du coup, il faudra surveiller si push() nous renvoie
    bien True et sinon, défaire immédiatement le coup par un pop() et essayer un autre coup.'''
    return choice(b.weak_legal_moves())

def weakDeroulementRandom(b):
    '''Déroulement d'une partie de go au hasard des coups possibles. Cela va donner presque exclusivement
    des parties très longues. Cela illustre cependant comment on peut jouer avec la librairie
    très simplement en utilisant les coups weak_legal_moves().
    
    Ce petit exemple montre comment utiliser weak_legal_moves() plutot que legal_moves(). Vous y gagnerez en efficacité.'''

    print("----------")
    b.prettyPrint()
    if b.is_game_over():
        print("Resultat : ", b.result())
        return

    while True:
        # push peut nous renvoyer faux si le coup demandé n'est pas valide à cause d'un superKo. Dans ce cas il faut
        # faire un pop() avant de retenter un nouveau coup 
        valid = b.push(weakRandomMove(b))
        if valid:
            break
        b.pop()
    weakDeroulementRandom(b)
    b.pop()
"""
board = Goban.Board()
deroulementRandom(board)
"""
def eval_board(b):
    [score_blacks,score_white]=b.compute_score()
    return score_white-score_blacks    

def MinMax(b,p):
    if b.is_game_over():
        if b.result() == "1-0":         
            return 1000
        elif b.result() == "0-1":
            return -1000
        else :
            return 0         
    if p==0 :
        return eval_board(b)
    else :
        pire=10000
        for m in b.generate_legal_moves():
            b.push(m)
            pire=min(pire,MaxMin(b,p-1))
            b.pop()
        return pire

def MaxMin(b,p):
    if b.is_game_over():
        if b.result() == "1-0":         
            return 1000
        elif b.result() == "0-1":
            return -1000
        else :
            return 0         
    if p==0 :
        return eval_board(b)
    else :
        meilleur=-10000
        for m in b.generate_legal_moves():
            b.push(m)
            meilleur=max(meilleur,MinMax(b,p-1))
            b.pop()
        return meilleur

def best_move_MiniMax(b,p):
    if b.is_game_over() or p==0:
        return None
    else:     
        best_move = None
        score = -10000
        for m in b.generate_legal_moves():
            b.push(m)
            res=MinMax(b,p-1)
            if res > score :
                score = res
                best_move = m
            b.pop()
    return best_move        

def MiniMax_vs_Aleatoire(b,p,is_ennemi):
    print("----------")
    b.prettyPrint()
    if b.is_game_over():
        print("Resultat : ", b.result())
        return  
    if is_ennemi :
        b.push(randomMove(b))
    else :
        b.push(best_move_MiniMax(b,p))

    MiniMax_vs_Aleatoire(b,p,not is_ennemi)   
    b.pop()

def Mini_Max_a_b(b,p,alpha,beta):
    if b.is_game_over():
        res = b.result()
        if res == "1-0": 
            return 1000
        elif res =="0-1":
            return -1000
        else:
            return 0
    if p==0:      
        return eval_board(b)
    else :
        for m in b.generate_legal_moves():
            b.push(m)
            beta=min(beta,Max_Min_a_b(b,p-1,alpha,beta))
            b.pop()
            if alpha >= beta :
                return alpha 
        return beta  

def Max_Min_a_b(b,p,alpha,beta):
    if b.is_game_over():
        res = b.result()
        if res == "1-0": 
            return 1000
        elif res =="0-1":
            return -1000
        else :
            return 0
    if p==0:      
        return eval_board(b)
    else :
        for m in b.generate_legal_moves():
            b.push(m)
            alpha=max(alpha,Min_Max_a_b(b,p-1,alpha,beta))
            b.pop()
            if alpha >= beta :
                return beta 
        return alpha   

def best_move_Mini_Max_a_b(b,p):
    if p==0 or b.is_game_over() :
        return None 
    else:
        best_move=None 
        score=-10000
        for m in b.generate_legal_moves():
            b.push(m)
            res = Mini_Max_a_b(b,p,score,10000)
            if res > score : 
                best_move = m 
                score = res 
            b.pop()
        return best_move 

def MiniMax_a_b_vs_Aleatoire(b,p,is_ennemi,cpt):
    print("----------")
    b.prettyPrint()    
    if b.is_game_over():
        print("Resultat : ", b.result())
        return  
    else :
        cpt=cpt+1
        print("cpt = ",cpt)
        if(is_ennemi or cpt < 40 ):
            b.push(randomMove(b))
        else :
            b.push(best_move_Mini_Max_a_b(b,p))
        MiniMax_a_b_vs_Aleatoire(b,p,not is_ennemi,cpt)
        b.pop()    

        














board = Goban.Board()
MiniMax_a_b_vs_Aleatoire(board,1,True,0)
