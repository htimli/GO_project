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
    [score_blacks, score_white] = b.compute_score()
    return score_white-score_blacks


def MinMax(b, p):
    if b.is_game_over():
        if b.result() == "1-0":
            return 1000
        elif b.result() == "0-1":
            return -1000
        else:
            return 0
    if p == 0:
        return eval_board(b)
    else:
        pire = 10000
        for m in b.generate_legal_moves():
            b.push(m)
            pire = min(pire, MaxMin(b, p-1))
            b.pop()
        return pire


def MaxMin(b, p):
    if b.is_game_over():
        if b.result() == "1-0":
            return 1000
        elif b.result() == "0-1":
            return -1000
        else:
            return 0
    if p == 0:
        return eval_board(b)
    else:
        meilleur = -10000
        for m in b.generate_legal_moves():
            b.push(m)
            meilleur = max(meilleur, MinMax(b, p-1))
            b.pop()
        return meilleur


def best_move_MiniMax(b, p):
    if b.is_game_over() or p == 0:
        return None
    else:
        best_move = None
        score = -10000
        for m in b.generate_legal_moves():
            b.push(m)
            res = MinMax(b, p-1)
            if res > score:
                score = res
                best_move = m
            b.pop()
    return best_move


def MiniMax_vs_Aleatoire(b, p, is_ennemi):
    print("----------")
    b.prettyPrint()
    if b.is_game_over():
        print("Resultat : ", b.result())
        return
    if is_ennemi:
        b.push(randomMove(b))
    else:
        b.push(best_move_MiniMax(b, p))

    MiniMax_vs_Aleatoire(b, p, not is_ennemi)
    b.pop()


def Mini_Max_a_b(b, p, alpha, beta, is_ennemi):
    if b.is_game_over():
        res = b.result()
        if res == "1-0":
            return 1000
        elif res == "0-1":
            return -1000
        else:
            return 0
    if p == 0:
        return eval_board(b)
    else:
        for m in b.generate_legal_moves():
            b.push(m)
            beta = min(beta, Max_Min_a_b(b, p-1, alpha, beta))
            b.pop()
            if alpha >= beta:
                return alpha
        return beta


def Max_Min_a_b(b, p, alpha, beta, is_ennemi):
    if b.is_game_over():
        res = b.result()
        if res == "1-0":
            return 1000
        elif res == "0-1":
            return -1000
        else:
            return 0
    if p == 0:
        return eval_board(b)
    else:
        for m in b.generate_legal_moves():
            b.push(m)
            alpha = max(alpha, Mini_Max_a_b(b, p-1, alpha, beta))
            b.pop()
            if alpha >= beta:
                return beta
        return alpha


def best_move_Mini_Max_a_b(b, p, opti):
    if p == 0 or b.is_game_over():
        return None
    else:
        best_move = []
        score = -10000
        for m in b.generate_legal_moves():
            b.push(m)
            res = Mini_Max_a_b(b, p, score, 10000)
            if res > score:
                best_move.clear()
                score = res
            if res == score:
                best_move.append(m)
            b.pop()
        return choice([m for m in best_move])


def LV1_Min_Max_a_b(b, p, is_ennemi, opti):

    possibleMoves = b.generate_legal_moves()
    bestMoveScore = -10000
    bestMove = []

    alpha = -10000
    beta = 10000

    for m in possibleMoves:
        b.push(m)
        score = max(bestMoveScore, Min_Max_a_b(b, p-1,
            alpha, beta, is_ennemi))
        b.pop()
        if score > bestMoveScore:
            bestMoveScore = score
            bestMove.clear()
        if score == bestMoveScore:
            bestMove.append(m)
    if(opti == True):
        for n in bestMove:
            l = from_locations_to_pattern(b, get_neighbors_square(b, n))
            if(is_pattern(b, l)):
                print("###############################################"")
                print("              Pattern on Move ", b.move_to_str(n))
                print("##############################################"")
                return n

    return choice([m for m in bestMove])

def Min_Max_a_b(b, p, alpha, beta, is_ennemi):
    if p == 0 or b.is_game_over():
        return eval_board(b)

    possibleMoves = b.generate_legal_moves()

    if(not is_ennemi):
        for m in possibleMoves:
            b.push(m)
            alpha = max(alpha, Min_Max_a_b(b,p-1,
                alpha,beta, not is_ennemi))
            b.pop()
            if alpha >= beta:
                return beta
        return alpha
    else:
        for m in possibleMoves:
            b.push(m)
            beta = min(beta,Min_Max_a_b(b,p-1,
                alpha,beta,not is_ennemi))
            b.pop()
            if beta <= alpha:
                return alpha
        return beta



def MiniMax_a_b_vs_Aleatoire(b, p):
    
    cpt = 0
    is_ennemi = False

    while b.is_game_over() == False:
        is_ennemi = not is_ennemi
        cpt += 1
        print("cpt = ",cpt,"is_ennemi = ", is_ennemi)
        if(is_ennemi):
            b.push(randomMove(b))
        else:
            debut = time.time()
            move = LV1_Min_Max_a_b(b,p,is_ennemi,True)
            fin = time.time()
            print("Running time: ", fin-debut, " seconds")
            b.push(move)
            print("Move played", b.move_to_str(move))
        b.prettyPrint()
    print("Resultat : ", b.result())

def MiniMax_a_b_vs_MinMax(b, p1,p2):
    cpt = 0
    is_ennemi = False

    while b.is_game_over() == False:
        is_ennemi = not is_ennemi
        cpt += 1
        print("cpt = ",cpt,"is_ennemi = ", is_ennemi)
        if(is_ennemi):
            b.push(best_move_MiniMax(b,p2))
        else:
            debut = time.time()
            move = LV1_Min_Max_a_b(b,p1,is_ennemi,True)
            fin = time.time()
            print("Running time: ", fin-debut, " seconds")
            b.push(move)
            print("Move played", b.move_to_str(move))
        b.prettyPrint()
    print("Resultat : ", b.result())
    

def get_neighbors_square(b, fcoord):
    x, y = b.unflatten(fcoord)
    neighbors = ((x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y),
                 (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1))
    return [b.flatten(c) for c in neighbors if b._isOnBoard(c[0], c[1])]


def from_locations_to_pattern(b, l):
    return [b[a] for a in l]


def apply_pattern(b, l, pattern):
    x = 0
    l1 = l.copy()
    for a in pattern:
        if pattern[x] == 3:
            l1[x] = 3
        x += 1
    return l1

# 0 = vide
# 1 = B
# 2 = W
# 3 = Any
# 4 = not(2,2,2)


pattern_B = (1, 2, 2, 0, 0, 3, 0, 3)  # Black normal pattern // size 8
pattern_1_B_side = (3, 1, 2, 3, 3)  # side pattern // size 5

# pattern_side
pattern_W_side = ((3, 1, 2, 3, 1), (3, 1, 2, 2, 1))

# normal pattern
pattern_1 = (1, 2, 1, 0, 0, 3, 3, 3)
pattern_2 = (1, 2, 0, 0, 0, 3, 0, 3)
pattern_3 = (1, 2, 3, 1, 0, 3, 0, 3)
pattern_4 = (1, 2, 3, 2, 3, 3, 3, 3)
pattern_5 = (1, 2, 3, 2, 2, 3, 0, 3)
pattern_6 = (1, 2, 3, 2, 0, 3, 2, 3)

normal_pattern = (pattern_1, pattern_2, pattern_3,
                  pattern_4, pattern_5, pattern_6)

special_pattern = (3, 1, 3, 2, 2, 4, 4, 4)  # special_case

pattern_side = ((1, 0, 3, 2, 3), (3, 1, 3, 1, 2))


def is_pattern(b, l):
    if b.next_player() == 2:  # Black turn
        if(len(l) == 5 and apply_pattern(b, l, pattern_1_B_side) == pattern_1_B_side):
            return True
        elif(len(l) == 8 and apply_pattern(b, l, pattern_B) == pattern_B):
            return True
    else:  # White turn
        if(len(l) == 5 and (apply_pattern(b, l, pattern_W_side[0]) == pattern_W_side[0] or apply_pattern(b, l, pattern_W_side[1]) == pattern_W_side[1])):
            return True

    # Any color

    
    if len(l) == 8:
        # normal pattern
        for p in normal_pattern:
            if apply_pattern(b, l, p) == p:
                return True

        # special pattern
        for i in range(5):
            if(l[i] != special_pattern[i]):
                break
            if i == 4:
                if(l[i+1] == l[i+2] and l[i+1] == l[i+3]):
                    return False
                else:
                    return True

    # pattern side
    if(len(l) == 5 and (apply_pattern(b, l, pattern_side[0]) == pattern_side[0] or apply_pattern(b, l, pattern_side[1]) == pattern_side[1])):
        return True

    return False



board = Goban.Board()

# val = get_neighbors_square(board, 12)
# board.pretty_print()
# board.push(12)
# board.push(13)
# print(val)
# val = board.__getitem__(12)
# print(val)
# val = board.__getitem__(13)
# print(val)

# pattern = from_locations_to_pattern(board, val)
# after_pattern = apply_pattern(board, pattern, pattern_1)
# res = is_pattern(board,after_pattern)

# a = val[4]
# print(a)
# print(board[a])

# print(pattern)
# print(after_pattern)
# print(res)

# board.pretty_print()


# MiniMax_a_b_vs_Aleatoire(board,2)
MiniMax_a_b_vs_MinMax(board,2,2)
