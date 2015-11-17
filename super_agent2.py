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
import bisect
import avalam
import minimax
import time


class Agent:
    """This is the skeleton of an agent to play the Avalam game."""

    def __init__(self, name="Agent"):
    	self.name = name
    	self.player = 0
    	self.passed=False
    	self.totalTime=0


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
        listState = []

        for action in board.get_actions():
            self.allFilter(player,board,action,stepnumber,listState)

        if len(listState) == 0:
            listTemp=[]
            for e in board.get_actions():
                new=(e,(board.clone().play_action(e),(-1)*player,stepnumber+1))
                listTemp.append(new)
            if player==self.player:
                listF=sorted(listTemp,key=lambda a:self.evaluate(a[1]),reverse=True)
                for e in listF:
                    yield e
            else:
                listF=sorted(listTemp,key=lambda a:self.evaluate(a[1]))
                for e in listF:
                    yield e
        else:
            if player==self.player:
                listF=sorted(listState, key=lambda a: self.evaluate(a[1]),reverse=True)
                for e in listF:
                    yield e
            else:
                listF=sorted(listState,key=lambda a:self.evaluate(a[1]))
                return listF

    def cutoff(self, state, depth):
        """The cutoff function returns true if the alpha-beta/minimax
        search has to stop; false otherwise.
        """
        board=state[0]
        stepnumber=state[2]
        maxt=2
        if stepnumber>=12 and stepnumber < 19:
            maxt=3
        elif stepnumber >= 19 and stepnumber < 27:
            maxt=4
        elif stepnumber >=27:
            maxt=5
        if board.is_finished() or depth >= maxt:
            return True
        return False

    def evaluate(self, state):
        """The evaluate function must return an integer value
        representing the utility function of the board.
        """
        board=state[0]
        tower=0
        towIsol=0
        towNextStep=0
        towOne=0
        towTwo=0
        towThree=0
        towFour=0
        for i in range(board.rows):
            for j in range(board.columns):
                """number of tower for each player"""
                tow=board.m[i][j]

                if tow !=0 :
                    n1=abs(tow)
                    s=tow/n1
                    check=False
                    for k in range(i-1,i+2):
                        for h in range(j-1,j+2):
                            if (k>=0 and k<=board.rows-1 and h>=0 and h<=board.columns-1) and not(k==i and h==j):
                                n2=board.m[k][h]
                                if(n2!=0):
                                    s2 = n2/abs(n2)
                                    number=(abs(n2)+n1)
                                    if (number == 5):
                                        if s2 < 0 :
                                            check=True
                                        towNextStep+=s2*50

                    if tow < 0:
                        tower -= 1
                                        
                    elif tow > 0:
                        tower += 1

                    if(not board.is_tower_movable(i,j)):
                        if n1 == 5:
                            towIsol+=s*100
                        else:
                            towIsol+=s*75

                    elif(board.is_tower_movable(i,j) and (not check)):
                        if n1 == 1:
                            towOne+=s*5
                        elif n1 == 2:
                            towTwo+=s*40
                        elif n1 == 3:
                            towThree+=s*15
                        else:
                            towFour+=s*20

        towTot=towOne+towTwo+towThree+towFour
        return tower + towIsol + towTot +towNextStep

    def BackUpFilter(self,player,board,action,check):
        x1=action[0]
        x2=action[2]
        y1=action[1]
        y2=action[3]
        n1=board.m[x1][y1]
        n2=board.m[x2][y2]
        isolTower = False
        s=n1/abs(n1)
        number = s*(abs(n1)+abs(n2)) 
        if(number == 5):
            return True
        for i in range(x2-1,x2+2):
            for j in range(y2-1,y2+2):
                if (i>=0 and i<=board.rows-1 and j>=0 and j<=board.columns-1 and not (i==x1 and j==y1) and not (i==x2 and j==y2)):
                    n3=board.m[i][j]
                    if(n3!=0):
                        s2 = n3/abs(n3)
                        number2=s2*(abs(number)+abs(n3))
                        if n3>0 :
                            return True
                        else:
                            board.m[i][j] = 0
                            board.m[x1][y1] = 0
                            board.m[x2][y2] = number2
                            if(check):
                                print(board.m[x2][y2],i,j)
                                print(not board.is_tower_movable(x2,y2))
                            if (not board.is_tower_movable(x2,y2)):
                                isolTower = True
                            board.m[x1][y1] = n1
                            board.m[x2][y2] = n2
                            board.m[i][j] = n3
        if(isolTower):                
            return False
        else:
            return True

    def noBad5Filter(self,player,board,action):
        x1=action[0]
        x2=action[2]
        y1=action[1]
        y2=action[3]
        n1=board.m[x1][y1]
        n2=board.m[x2][y2]

        s = n1/abs(n1)
        number=s*(abs(n1)+abs(n2))
        if (player == self.player and number == -5 ):
            return False
        else:
            for i in range(x2-1,x2+2):
                for j in range(y2-1,y2+2):
                    if (i>=0 and i<=board.rows-1 and j>=0 and j<=board.columns-1 and not (i==x1 and j==y1) and not (i==x2 and j==y2)):
                        n3=board.m[i][j]
                        if(n3!=0):
                            s2=n3/abs(n3)
                            number2=s2*(abs(n3)+abs(number))
                            if (number2 == -5):
                                return False
        #else:
        return True

    def towerDifferentColourFilter(self,player,board,action):
        listState = []
        x1=action[0]
        x2=action[2]
        y1=action[1]
        y2=action[3]
        n1=board.m[x1][y1]
        n2=board.m[x2][y2]
        if(n1 > 0 and n2 < 0):
            return True
        else: 
            return False

    def allFilter(self,player,board,action,stepnumber,listState):
        #print('noBad5Filter =', self.noBad5Filter(player,board,action))
        #print('towerDifferentColourFilter =', self.towerDifferentColourFilter(player,board,action))
        #print('BackUpFilter =', self.BackUpFilter(player,board,action))
        if(self.noBad5Filter(player,board,action) and self.towerDifferentColourFilter(player,board,action) and self.BackUpFilter(player,board,action,False)):
            new=(action,(board.clone().play_action(action),(-1)*player,stepnumber+1))
            listState.append(new)



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

        self.player=player
        self.time_left = time_left
        newBoard = avalam.Board(board.get_percepts(player==avalam.PLAYER2))
        state = (newBoard, player, step)
        start_time = time.time() 
        result=minimax.search(state,self)
        #print('towerDifferentColourFilter =', self.towerDifferentColourFilter(player,board,action))
        interval = time.time() - start_time
        self.totalTime+=interval

        print('Decision Time:', interval )
        print('Total time:',self.totalTime)
        return result
