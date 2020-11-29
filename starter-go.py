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
    print("eval_board : ", eval_board(b))
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
    if b.is_game_over():
        if b.result() == "1-0":
            return 1000
        elif b.result() == "0-1":
            return -1000
        else:
            return 0
    [score_blacks, score_white] = b.compute_score()
    return score_white-score_blacks


def MinMax_A_B(b, p, alpha, beta, is_ennemi):
    if p == 0 or b.is_game_over():
        return eval_board(b)

    if(is_ennemi):
        for m in b.generate_legal_moves():
            b.push(m)
            beta = min(beta, MinMax_A_B(b, p-1,
             alpha, beta, not is_ennemi))
            b.pop()
            if beta <= alpha:
                return alpha
        return beta
    else:
        for m in b.generate_legal_moves():
            b.push(m)
            alpha = max(alpha,MinMax_A_B(b,p-1,
             alpha, beta, not is_ennemi))
            b.pop()
            if alpha >= beta:
                return beta
        return alpha


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
    

def Alpha_Beta(b,p,is_ennemi):

    bestMoveScore = -10000
    bestMove = []

    alpha = -10000
    beta = 10000

    for m in b.legal_moves():
        b.push(m)
        score = max(bestMoveScore,
         MinMax_A_B(b,p,alpha,beta,not is_ennemi))
        b.pop()
        if score > bestMoveScore:
            bestMoveScore = score
            bestMove.clear()
        if score == bestMoveScore:
            bestMove.append(m)
    return choice([m for m in bestMove])

def Alpha_Beta_vs_Aleatoire(b):
    print("-----------------------------------")
    print(" Début de partie A_B_vs_RandomMove ")
    print("-----------------------------------")
    b.prettyPrint()
    
    i = 90
    is_ennemi = False
    while i > 0 and b.is_game_over() == False:
        if i%2 == 0:
            print("Tour de l'IA")
            move = Alpha_Beta(b,1, is_ennemi)
            print(move)
            b.push(move)
        else:
            print("Tour ennemi")
            b.push(weakRandomMove(b))
        
        b.prettyPrint()
        i-=1
        print(i)
        print("Score: ", eval_board(b))

    print("Resultat : ", b.result())





board = Goban.Board()

# weakDeroulementRandom(board)

# MiniMax_vs_Aleatoire(board,1,True)

Alpha_Beta_vs_Aleatoire(board)