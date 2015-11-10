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
        self.player=0
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
        listAction=[]
        #print(player,self.player)
        #print(board.m[6][7])
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
            number=s*(abs(n1)+abs(n2))
            if (player == self.player and number == -5 ):
                continue
            else:
                new=(action,(board.clone().play_action(action),(-1)*player,stepnumber+1))
                listAction.append(new)
                yield new
            """elif (player == self.player):
                bad=False
                for i in range(x2-1,x2+2):
                    for j in range(y2-1,y2+2):
                        if (i>=0 and i<=board.rows-1 and j>=0 and j<=board.columns-1 and (i!=x1 and j!=y1) and (i!=x2 and j!=y2)):
                            n3=board.m[i][j]
                            if n3>0:
                                s2=1
                            else:
                                s2=-1
                            number2=s2*(abs(n3)+abs(number))
                            if (number2 == -5):
                                bad=True
                if (bad==True):
                    continue
                else:
                    new=(action,(board.clone().play_action(action),(-1)*player,stepnumber+1))
                    listAction.append(new)
                    yield new
            """

         
        if len(listAction)== 0 :
            #for e in listAction:
            #    yield e
        #else:
            for e in board.get_actions():
                yield e

        """for e in listAction:
            yield e
        else:
            if player < 0:
                listF=sorted(listAction,key=lambda st:self.evaluate(st[1]),reverse=True)
            else:
                listF=sorted(listAction,key=lambda st:self.evaluate(st[1]))
            for e in listF:
                yield e"""
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
        if stepnumber>=15 and stepnumber < 18:
            maxd=3
        elif stepnumber >= 18 and stepnumber < 22:
            maxd=4
        elif stepnumber >=22 and stepnumber < 27:
            maxd=5
        elif stepnumber >= 27:
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
        towOne=0
        towTwo=0
        towThree=0
        towFour=0
        for i in range(board.rows):
            for j in range(board.columns):
                """number of tower for each player"""
                tow=board.m[i][j]

                if tow !=0 :
                    number=abs(tow)
                    s=tow/number
                    if tow < 0:
                        tower -= 1
                        if tow == -5 :
                            towMax-=1
                    elif tow > 0:
                        tower += 1
                        if tow == 5 :
                            towMax+=1


                    if(not board.is_tower_movable(i,j) and not(number==5)):
                        if tow < 0:
                            towIsol -= 1
                        elif tow > 0:
                            towIsol += 1
                        if number == 1:
                            towOne+=s*2
                        elif number == 2:
                            towTwo+=s*4
                        elif number == 3:
                            towThree+=s*6
                        else:
                            towFour+=s*8
                    elif(board.is_tower_movable(i,j) and not(number==5)):
                        if number == 1:
                            towOne+=s
                        elif number == 2:
                            towTwo+=s*2
                        elif number == 3:
                            towThree+=s*3
                        else:
                            towFour+=s*4
        towTot=towOne+towTwo+towThree+towFour
        return tower + 5*towMax + 5*towIsol + towTot

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
        start_time = time.time() 
        self.player=player
        self.time_left = time_left
        newBoard = avalam.Board(board.get_percepts(player==avalam.PLAYER2))
        state = (newBoard, player, step)
        result=minimax.search(state,self)
        interval = time.time() - start_time
        self.totalTime+=interval

        print('Decision Time:', interval )
        print('Total time:',self.totalTime)
        return result



if __name__ == "__main__":
    avalam.agent_main(Agent())
