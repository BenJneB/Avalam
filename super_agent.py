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
    
    def abmax(self, move1,move2):
        return self.evaluate(move1[0])- self.evaluate(move2[0])
    
    def abmin(self, move1,move2):
        return -(self.evaluate(move1[0])-self.evaluate(move2[0]))
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
         
        if len(listAction)== 0 :

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
                listF=sorted(listAction, key=lambda a: self.evaluate(a[1]),reverse=True)
                for e in listF:
                    yield e
            else:
                listF=sorted(listAction,key=lambda a:self.evaluate(a[1]))
                return listF

    def cutoff(self, state, depth):
        """The cutoff function returns true if the alpha-beta/minimax
        search has to stop; false otherwise.
        """
        board=state[0]
        stepnumber=state[2]
        maxt=2
        if stepnumber>=12:
            maxt=3
        elif stepnumber >= 19:
            maxt=4
        elif stepnumber >=27:
            maxt=5
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
                        #if tow < 0:
                        #    towIsol -= 1
                        #elif tow > 0:
                        #    towIsol += 1
                        if number == 1:
                            towIsol+=s*8
                        elif number == 2:
                            towIsol+=s*6
                        elif number == 3:
                            towIsol+=s*4
                        else:
                            towIsol+=s*2
                    elif(board.is_tower_movable(i,j) and not(number==5)):
                        if number == 1:
                            towOne+=s*4
                        elif number == 2:
                            towTwo+=s*3
                        elif number == 3:
                            towThree+=s*2
                        else:
                            towFour+=s
        towTot=towOne+towTwo+towThree+towFour
        return tower + 10*towMax + 5*towIsol + towTot

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
