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
        
        def compareState(state):
            return self.evaluate(state[1])

        fringe = None 
        if player == self.player:
            fringe = PriorityQueue(compareState,max)
        else:
            fringe = PriorityQueue(compareState,min)

        for action in board.get_actions():
            fringe.append((action,(board.clone().play_action(action),(-1)*player,stepnumber+1)))

        if(10 < len(fringe)):
            length = 10
        else:
            length = len(fringe)
        while length != 0:
            yield fringe.pop()
            length -= 1

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
        towMax = 0
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
                    
                if(not board.is_tower_movable(i,j) and not(abs(board.m[i][j])==5)):
                    if board.m[i][j] < 0:
                        towIsol -= 1
                    elif board.m[i][j] > 0:
                        towIsol += 1

        return tower + 5*towMax+ 5*towIsol

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

class Queue:
    """Queue is an abstract class/interface. There are three types:
        Stack(): A Last In First Out Queue.
        FIFOQueue(): A First In First Out Queue.
        PriorityQueue(lt): Queue where items are sorted by lt, (default <).
    Each type supports the following methods and functions:
        q.append(item)  -- add an item to the queue
        q.extend(items) -- equivalent to: for item in items: q.append(item)
        q.pop()         -- return the top item from the queue
        len(q)          -- number of items in q (also q.__len())
    Note that isinstance(Stack(), Queue) is false, because we implement stacks
    as lists.  If Python ever gets interfaces, Queue will be an interface."""

    def __init__(self): 
        abstract

    def extend(self, items):
        for item in items: self.append(item)

def Stack():
    """Return an empty list, suitable as a Last-In-First-Out Queue."""
    return []

class PriorityQueueElmt:
    """ The elements of the priority queue """
    def __init__(self,val,e):
        self.val = val
        self.e = e
    
    def __lt__(self,other):
        return self.val < other.val
    
    def value(self):
        return self.val
    
    def elem(self):
        return self.e
        

class PriorityQueue(Queue):
    """A queue in which the minimum (or maximum) element (as determined by f and
    order) is returned first. If order is min, the item with minimum f(x) is
    returned first; if order is max, then it is the item with maximum f(x)."""
    def __init__(self, f, order=min):
        self.A=[]
        self.order=order
        self.f=f
    def append(self, item):
        queueElmt = PriorityQueueElmt(self.f(item),item)
        bisect.insort(self.A, queueElmt)
    def __len__(self):
        return len(self.A)
    def pop(self):
        if self.order == min:
            return self.A.pop(0).elem()
        else:
            return self.A.pop().elem()

if __name__ == "__main__":
    avalam.agent_main(Agent())
