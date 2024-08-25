import numpy as np
from enum import Enum, auto


#Left person is denoted as I and they are positive 1
#Right person is denoted as J and they are negative 1
#turn is denoted as T 0 is Left and 1 is Right

chopsticksArray = np.full((15,15,2), None, dtype=object)
stack = []
LEFT_TURN = 0
RIGHT_TURN = 1

#the possible moves you can make on your turn
class Moves(Enum):
    I_ATTACK_I = auto()
    I_ATTACK_J = auto()
    J_ATTACK_I = auto()
    J_ATTACK_J = auto()
    SPLIT = auto()


#gets the win rate of two hands the the turn
#if turn is 0 then its left person 
#if turn is 1 then its right person
def chopsticks(i, j, t):
    #keep track of the function call to stop it from reaching an infinite loop 
    stack.append((i,j,t))

    #anything equal or above 5 is a dead hand so just set it to 5
    if i > 5: i = 5
    if j > 5: j = 5

    # if we have the value then return it
    if(chopsticksArray[i][j][t]):
        return chopsticksArray[i][j][t]
    
    #if the left person hand is dead then right person 100% wins 
    elif(hand(i) == (5,5)):
        return -1
    
    #if the right person hand is dead then left person 100% wins
    elif(hand(j) == (5,5)):
        return 1
    
    #if we already made this function call before and its not the one we just added that means we have ran into a loop
    #so return 0 meaning its a draw to keep going down this path
    elif((i,j,t) in stack and stack.index((i,j,t)) != len(stack) - 1):
        return 0
    
    #if they neither hand is dead we need to calculate the winrate of the next possible hands
    else:
        moveList = getMoves(i,j,t)
        winPercent = 0
        #there should never be a case where there is no moves
        if len(moveList) == 0: raise ValueError("ERROR: No moves possible for hand {i}, {j}, {t}")
        
        for move in moveList:
            newMain, newOpponent, newT = applyMove(move, i, j, t)
            winPercent += chopsticks(newMain, newOpponent, newT)
        
        chopsticksArray[i][j][t] = winPercent/len(moveList)
        return chopsticksArray[i][j][t]


def applyMove(moveType, i, j, t):
    #find the new I, J based on the move
    #T always just flips to the next turn

    mainHand = i
    opponentHand = j
    #default is left turn so newT is right turn
    newT = RIGHT_TURN

    #determine whos turn it is
    if (t): 
        mainHand = i
        opponentHand = j
        #if its right turn the next turn is left turn
        newT = LEFT_TURN

    
    mainI, mainJ, = hand(mainHand)
    opponentI, opponentJ, = hand(opponentHand)

    #the new hands that will appear, they are default their original hands
    mainNewI = mainI
    mainNewJ = mainJ 
    opponentNewI = opponentI
    opponentNewJ = opponentJ

    match moveType:
        case Moves.I_ATTACK_I:
            opponentNewI = mainI + opponentI
        case Moves.I_ATTACK_J:
            opponentNewJ = mainI + opponentJ
        case Moves.J_ATTACK_I:
            opponentNewI = mainJ + opponentI
        case Moves.J_ATTACK_J:
            opponentNewJ = mainJ + opponentJ
        case Moves.SPLIT:
            #if hand I is dead that means hand J is splittable
            if mainI >= 5:
                if mainJ % 2 == 0:
                    mainNewI = mainJ//2
                    mainNewJ = mainJ//2
                else: 
                    raise ValueError("ERROR: Trying to apply move SPLIT but hand J is not splittable!!!")
            
            elif mainJ >= 5:
                if mainI % 2 == 0:
                    mainNewI = mainI//2
                    mainNewJ = mainI//2
                else: 
                    raise ValueError("ERROR: Trying to apply move SPLIT but hand I is not splittable!!!")
            else: raise ValueError("ERROR: Neither hand could be SPLIT!!!")
    
    return index((mainNewI, mainNewJ)), index((opponentNewI, opponentNewJ)), newT

#gets you the possible moves based on your hand, the opponents hand and whos turn its is.
def getMoves(i,j,t):
    mainHand = i
    opponentHand = j
    moveList = []

    #determine whos turn it is
    if (t): 
        mainHand = i
        opponentHand = j

    mainI, mainJ, = hand(mainHand)
    opponentI, opponentJ, = hand(opponentHand)

    #if our I hand is in play
    if mainI <= 5:
        #and our opponents I hand is in play 
        if opponentI <= 5:
            #we can attack it
            moveList.append(Moves.I_ATTACK_I)

        #and our opponents J hand is in play
        if opponentJ <= 5:
            #we can attack it
            moveList.append(Moves.I_ATTACK_J)

    #if our J hand is in play
    if mainJ <= 5:
        #and our opponents I hand is in play 
        if opponentI <= 5:
            #we can attack it
            moveList.append(Moves.J_ATTACK_I)

        #and our opponents J hand is in play
        if opponentJ <= 5:
            #we can attack it
            moveList.append(Moves.J_ATTACK_J)
        
    # if either hand I or hand J is dead 
    if (mainI >= 5 or mainJ >= 5) and (mainI != mainJ):
        #and the remaining hand is even
        if(mainI < 5 and mainI % 2 == 0) or (mainJ < 5 and mainJ %2 == 0):
            #then we can split the hand
            moveList.append(Moves.SPLIT)

    return moveList

#gets you the hand based on the index
def hand(i):
    match i:
        case 0:
            return (1,1)
        case 1:
            return (2,1)
        case 2:
            return (3,1)
        case 3:
            return (4,1)
        case 4:
            return (5,1)
        case 5:
            return (2,2)
        case 6:
            return (3,2)
        case 7:
            return (4,2)
        case 8:
            return (5,2)
        case 9:
            return (3,3)
        case 10:
            return (4,3)
        case 11:
            return (5,3)
        case 12:
            return (4,4)
        case 13:
            return (5,4)
        case 14:
            return (5,5)
    raise ValueError("ERROR: HAND INPUTTED NUMBER GREATER THEN 15!!!")

#does the inverse of the hand function
def index(i):
    match i:
        case (1,1):
            return 0 
        case (2,1):
            return 1
        case (3,1):
            return 2
        case (4,1):
            return 3
        case (5,1):
            return 4
        case (2,2):
            return 5
        case (3,2):
            return 6
        case (4,2):
            return 7
        case (5,2):
            return 8
        case (3,3):
            return 9
        case (4,3):
            return 10
        case (5,3):
            return 11
        case (4,4):
            return 12
        case (5,4):
            return 13
        case (5,5):
            return 14
def main():
    #starting at base hand
    chopsticks(0,0,0)


if __name__ == "__main__":
    main()
    


