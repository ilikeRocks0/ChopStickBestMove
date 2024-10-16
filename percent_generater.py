import numpy as np
from enum import Enum, auto
import csv

#Left person is denoted as I and they are positive 1
#Right person is denoted as J and they are negative 1
#turn is denoted as T 0 is Left and 1 is Right
#anyvalue in the table is the percent chance that left hand will win

chopsticksArray = np.full((15,15,2), -1, dtype=object)
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


    # if we have the value then return it
    if(chopsticksArray[i][j][t] != -1):
        stack.pop()
        return chopsticksArray[i][j][t]
    
    #if the left person hand is dead then right person 100% wins 
    elif(hand(i) == (5,5)):
        stack.pop()
        return 0
    
    #if the right person hand is dead then left person 100% wins
    elif(hand(j) == (5,5)):
        stack.pop()
        return 1
    
    #if we already made this function call before and its not the one we just added that means we have ran into a loop
    #so return 0 meaning its a draw to keep going down this path
    elif((i,j,t) in stack and stack.index((i,j,t)) != len(stack) - 1):
        stack.pop()
        return 0.5
    
    #if they neither hand is dead we need to calculate the winrate of the next possible hands
    else:
        moveList = getMoves(i,j,t)
        winPercent = 0
        #there should never be a case where there is no moves
        if len(moveList) == 0: raise ValueError("ERROR: No moves possible for hand {i}, {j}, {t}")
        
        for move in moveList:
            leftHands, rightHands, newT = applyMove(move, i, j, t)
            winPercent += chopsticks(leftHands, rightHands, newT)
        
        chopsticksArray[i][j][t] = winPercent/len(moveList)
    stack.pop()
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
        mainHand = j
        opponentHand = i
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
    
    
    #anything equal or above 5 is a dead hand so just set it to 5
    if mainNewI > 5: mainNewI = 5
    if mainNewJ > 5: mainNewJ = 5
    if opponentNewI > 5: opponentNewI = 5
    if opponentNewJ > 5: opponentNewJ = 5


    #left hand is the left person
    #right hand is the right person
    leftHands = index((mainNewI, mainNewJ))
    rightHands = index((opponentNewI, opponentNewJ))

    if(t):
        leftHands = index((opponentNewI, opponentNewJ))
        rightHands = index((mainNewI, mainNewJ))

    #always return consistantly
    return leftHands, rightHands, newT

#gets you the possible moves based on your hand, the opponents hand and whos turn its is.
def getMoves(i,j,t):
    mainHand = i
    opponentHand = j
    moveList = []

    #determine whos turn it is
    if (t): 
        mainHand = j
        opponentHand = i

    mainI, mainJ, = hand(mainHand)
    opponentI, opponentJ, = hand(opponentHand)

    #if our I hand is in play
    if mainI < 5:
        #and our opponents I hand is in play 
        if opponentI < 5:
            #we can attack it
            moveList.append(Moves.I_ATTACK_I)

        #and our opponents J hand is in play
        if opponentJ < 5:
            #we can attack it
            moveList.append(Moves.I_ATTACK_J)

    #if our J hand is in play
    if mainJ < 5:
        #and our opponents I hand is in play 
        if opponentI < 5:
            #we can attack it
            moveList.append(Moves.J_ATTACK_I)

        #and our opponents J hand is in play
        if opponentJ < 5:
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
#also does both ways so its easier on the other programs calling it
def index(i):
    match i:
        case (1,1):
            return 0 
        case (2,1):
            return 1
        case (1,2):
            return 1
        case (3,1):
            return 2
        case (1,3):
            return 2
        case (4,1):
            return 3
        case (1,4):
            return 3
        case (5,1):
            return 4
        case (1,5):
            return 4
        case (2,2):
            return 5
        case (3,2):
            return 6
        case (2,3):
            return 6
        case (4,2):
            return 7
        case (2,4):
            return 7
        case (5,2):
            return 8
        case (2,5):
            return 8
        case (3,3):
            return 9
        case (4,3):
            return 10
        case (3,4):
            return 10
        case (5,3):
            return 11
        case (3,5):
            return 11
        case (4,4):
            return 12
        case (5,4):
            return 13
        case (4,5):
            return 13
        case (5,5):
            return 14
    raise ValueError("ERROR: INDEX INPUTTED NUMBER GREATER THEN 15!!!")

def main():
    #starting at base hand
    chopsticks(0,0,0)
    print(chopsticksArray[0][0][0])
    print(chopsticksArray[0][1][0])
    print(chopsticksArray[0][2][0])
    # Replace None with a placeholder (e.g., np.nan)
    array = chopsticksArray
    # array = np.where(array == None, np.nan, array)

    # Write the first slice (t = 0) to a CSV file
    with open('slice_t0.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['t=0'])  # Optional header
        for row in array[:, :, 0]:
            writer.writerow(row)

    # Write the second slice (t = 1) to another CSV file
    with open('slice_t1.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['t=1'])  # Optional header
        for row in array[:, :, 1]:
            writer.writerow(row)

print("Slices saved to 'slice_t0.csv' and 'slice_t1.csv'")
if __name__ == "__main__":
    main()
    


