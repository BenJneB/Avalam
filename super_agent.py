#!/usr/bin/env python3
"""
Avalam agent.
Copyright (C) 2015, DAUBRY BENJAMIN & FICHEFET PIERRICK

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""

import avalam
import minimax
import time


class Agent:
    """This is the skeleton of an agent to play the Avalam game."""

    def __init__(self, name="Agent"):
        self.name = name
        self.passed=False
    
    def successors(self, state):
        """The successors function must return (or yield) a list of
        pairs (a, s) in which a is the action played to reach the
        state s; s is the new state, i.e. a triplet (b, p, st) where
        b is the new board after the action a has been played,
        p is the player to play the next move and st is the next
        step number.
        """
        board=state[0]
        player=state[1]
        stepnumber=state[2]
        for action in board.get_actions():
            yield (action,(board.clone().play_action(action),(-1)*player,stepnumber+1)) 
        """board=state[0]
        player=state[1]
        stepnumber=state[2]
        allMove=[]
        for action in board.get_actions():
            x1=action[0]
            x2=action[2]
            y1=action[1]
            y2=action[3]
            n1=board.m[x1][y1]
            n2=board.m[x2][y2]
            if (n1 >0 ):
                s=1
            else:
                s=-1
            """"""if (s<0 and player>0) or (s>0 and player<0):
                continue""""""

            """"""print("player",player)
            print("n1",n1)""""""
            number=s*(abs(n1)+abs(n2))
            """"""if((number==5 and player>0) or (number==-5 and player<0) or abs(number)<5):
                allMove.append(action)
                continue""""""
            if((number==5 and player<0) or (number==-5 and player >0)):
                continue
            allMove.append(action)
            """ """if ((number<0 and player<0) or (number >0 and player >0)):
                countGood=0
                for i in range(x2-1,x2+2):
                    for j in range(y2-1,y2+2):
                        if (i>=0 and i<=board.rows-1 and j>=0 and j<=board.columns-1 and (i!=x1 and j!=y1) and (i!=x2 and j!=y2)):
                            n3=board.m[i][j]
                            if n3>0:
                                s2=1
                            else:
                                s2=-1
                            number2=s2*(abs(n3)+abs(number))
                            if ((number2>0 and player<0) or (number2<0 and player>0)):
                                countGood+=1
                if (countGood==0):
                    allMove.append(action)""""""
        semFinL=[]
        inf = float("inf")
        curValA=(-inf)
        curValB=inf
        if (len(allMove)>0):
            for move in allMove:
                temp=self.evaluate((board.clone().play_action(move),(-1)*player,stepnumber+1))
                if(player>0 and curValA<temp):
                    print("alphabetter",curValA,temp)
                    curValA=temp
                    semFinL.insert(0,(move,(board.clone().play_action(move),(-1)*player,stepnumber+1)))
                elif(player<0 and curValB>temp):
                    curValB=temp
                    semFinL.insert(0,(move,(board.clone().play_action(move),(-1)*player,stepnumber+1)))
                else:
                    semFinL.append((move,(board.clone().play_action(move),(-1)*player,stepnumber+1)))
        else:
            for move in board.get_actions():
                semFinL.append((move,(board.clone().play_action(move),(-1)*player,stepnumber+1)))
        for e in semFinL:
            yield e"""
        """OBLIGE DE FAIRE CLONE????"""

    def cutoff(self, state, depth):
        """The cutoff function returns true if the alpha-beta/minimax
        search has to stop; false otherwise.
        """
        board=state[0]
        stepnumber=state[2]
        maxt=2
        if stepnumber>=13 and stepnumber < 16:
            maxd=3
        elif stepnumber >= 16 and stepnumber < 20:
            maxd=4
        elif stepnumber >=20 and stepnumber < 25:
            maxd=5
        elif stepnumber >= 25:
            maxd=10
        if board.is_finished() or depth >= maxt:
            return True
        return False

    def evaluate(self, state):
        """The evaluate function must return an integer value
        representing the utility function of the board.
        """
        board=state[0]
        tower=0
        towMax=0
        towIsol=0
        for i in range(board.rows):
            for j in range(board.columns):
                """number of tower for each player"""
                if board.m[i][j] < 0:
                    tower -= 1
                elif board.m[i][j] > 0:
                    tower += 1

                """number of tower (height:5) for each player"""
                if board.m[i][j] == -5:
                    towMax -= 1
                elif board.m[i][j] == 5:
                    towMax += 1
                number=abs(board.m[i][j])
                countNeigh=0
                countPoss=0
                if(not board.is_tower_movable(i,j)):
                    towIsol+=board.m[i][j]
                """for k in range(i-1,i+2):
                    for l in range(j-1,j+2):
                        """"""new X Y in bounds and it is a tower (not empty) with less than 5 pion""""""
                        if (k>=0 and k<=board.rows-1 and l>=0 and l<=board.columns-1):
                            if (board.m[k][l]!=0 and abs(board.m[k][l])!=5):
                                if (k!=i and l!=j):
                                    """"""count the number of neighbour""""""
                                    countNeigh+=1
                                    number2=abs(board.m[k][l])
                                    if (number+number2<=5):
                                        """"""count the number of possible move to have a tower""""""
                                        countPoss+=1

                if (countNeigh==0 or countPoss==0):
                    towIsol+=board.m[i][j]"""

        return tower + 5*towMax + 2.5*towIsol
    def play(self, board, player, step, time_left):
        """This function is used to play a move according
        to the board, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        """
        """if step == 1 :
            self.passed=True
            return (3,3,4,3)
        if self.passed==False and step==2:
            return (4,3,3,3)"""
        self.time_left = time_left
        newBoard = avalam.Board(board.get_percepts(player==avalam.PLAYER2))
        state = (newBoard, player, step)
        return minimax.search(state, self)



if __name__ == "__main__":
    avalam.agent_main(Agent())
