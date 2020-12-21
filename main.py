# Solving a sudoku using backtracking
from typing import List, Dict
import copy
from functools import reduce


class Board:
    def __init__(self, preconfig: List[int]) -> None:
        # constructor method for the board
        # check if we already have some data for this

        # if there is a 1x81 array already passed onto the board, we set that as
        # the principal value
        if preconfig:
            self.board = preconfig
        else:
            # initialize a blank 9x9 array, flattened as a 1x81 array
            self.board: List[int] = [0 for x in range(81)]
        # print("Board =>", self.board)

    def is_sequence_valid(self, sequence: List[int]) -> bool:
        # return if a sequence is valid.
        # a sequence is valid if it has only one of each number, and not more
        # (though less is possible if there are zeroes)
        # valid - 000010000
        # valid - 123456789
        # valid - 123456089
        # invalid - 000010001
        # invalid - 122345678

        # remove all zeroes, and check for repeats
        sequence = [x for x in sequence if x != 0]

        # print("checking validity of seq", sequence)

        # filter for repeats
        t = {x: 0 for x in range(1, 10)}

        for x in sequence:
            t[x] += 1

        # print(t)

        all_are_unique = all(map(lambda x: x <= 1, t.values()))
        # print(all_are_unique)

        numbers_in_limit = all(map(lambda x: x in range(1, 10), sequence))
        # print(numbers_in_limit)

        return numbers_in_limit and all_are_unique

    def is_correct(self) -> bool:

        # declare various parity variables, which will be reduced to single
        # boolean varibles as the last check
        row_parity: List[bool] = []
        column_parity: List[bool] = []
        grid_parity: List[bool] = []

        ## get row slices to check sum
        for x in range(0, 81, 9):
            segment: List[int] = self.board[x : x + 9]
            # this magic number has been hardcoded as 45
            if self.is_sequence_valid(segment):
                # print("passes row parity check")
                row_parity.append(True)
            else:
                # print("fails row parity check")
                row_parity.append(False)

        # print("Row parity - ", row_parity)

        ## get column slices to check for sum
        for x in range(0, 9):
            # get the columns
            segment: List[int] = [self.board[x + y * 9] for y in range(9)]
            if self.is_sequence_valid(segment):
                column_parity.append(True)
            else:
                column_parity.append(False)

        # print("column parity - ", column_parity)

        ## grid check
        ## co-ordinates of the top-left corners of the 3x3 grid
        grid: List[int] = [0, 3, 6, 27, 30, 33, 54, 57, 60]

        for index in grid:
            """
            0  1  2   3  4  5   6  7  8
            9  10 11  12 13 14  15 16 17
            18 19 20  21 22 23  24 25 26

            """
            # this will be explained later - it just gets the grid in constant
            # (relatively) time
            segment: List[int] = [
                self.board[index + (9 * x) + y] for y in range(3) for x in range(3)
            ]

            if self.is_sequence_valid(segment):
                grid_parity.append(True)
            else:
                grid_parity.append(False)

        # print("grid parity - ", grid_parity)

        # this is probably not a very optimized method of doing this, but it
        # will have to suffice.
        return all([all(grid_parity), all(column_parity), all(row_parity)])

    def get_possible_future_boards_states(self) -> List[List[int]]:

        # return none if there is no empty spot

        lb: int = len(self.board)

        # all possible future states
        states: List[List[int]] = []

        # find the first blank spot in the board
        for index in range(lb):

            if self.board[index] == 0:
                # generate all possible moves
                for possibility in range(1, 10):
                    test_board: List[int] = copy.copy(self.board)
                    # assign that value
                    test_board[index] = possibility
                    # print("testing board state -> ", test_board)
                    # generate a board and see if it's a valid state
                    test_board_object = Board(preconfig=test_board)
                    # if the state is valid, then pass it on to the list of
                    # playable states
                    correct: bool = test_board_object.is_correct()
                    if correct:
                        # print("Possible Config")
                        states.append(test_board)

                # print("states -> ", states)
                return states
        # this part of the loop only triggers when the whole for loop has
        # executed and nothing has happened
        else:
            # print("Solution Found! Here is the solution - ")
            print("".join([str(x) for x in self.board]))
            exit()

        if len(states) == 0:
            # print("Solution Found! Here is the solution - ")
            # print(self.board)
            return states


if __name__ == "__main__":
    sudoku = [int(x) for x in input()]

    genesis_board = Board(preconfig=sudoku)

    # keep a stack here, to store the states and perform DFS (which is
    # essentially what backtracking is)
    state_stack = [genesis_board]

    while len(state_stack) != 0:

        current = state_stack.pop()
        # print("current board state => ", current.board)
        # check for children
        children = current.get_possible_future_boards_states()

        # if there are children, move on
        if len(children) > 0:
            for child in children:
                state_stack.append(Board(preconfig=child))
        # if there are no children (i.e. no possible future game states, it
        # means that we have found a solution to the game. The program will
        # break on its own, and we do not need to register this as the solution
        # remains the same for each board, and we do not need to traverse other
        # paths.)
