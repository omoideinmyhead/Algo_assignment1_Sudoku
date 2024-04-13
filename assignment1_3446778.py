############ CODE BLOCK 0 ################
# DO NOT CHANGE THIS CELL.
# THESE ARE THE ONLY IMPORTS YOU ARE ALLOWED TO USE:

import numpy as np
import copy

RNG = np.random.default_rng()

############ CODE BLOCK 10 ################
class Sudoku():
    """
    This class creates sudoku objects which can be used to solve sudokus. 
    A sudoku object can be any size grid, as long as the square root of the size is a whole integer.
    To indicate that a cell in the sudoku grid is empty we use a zero.
    A sudoku object is initialized with an empty grid of a certain size.

    Attributes:
        :param self.grid: The sudoku grid containing all the digits.
        :type self.grid: np.ndarray[(Any, Any), int]  # The first type hint is the shape, and the second one is the dtype. 
        :param self.size: The width/height of the sudoku grid.
        :type self.size: int
    """
    def __init__(self, size=9):
        self.grid = np.zeros((size, size))
        self.size = size
    
    def __repr__(self):
        """
        This returns a representation of a Sudoku object.

        :return: A string representing the Sudoku object.
        :rtype: str
        """
        str_repr = ""
        for row in self.grid:
            for digit in row:
                str_repr += str(digit)
                str_repr += " "
            str_repr += "\n"
        
        return str_repr
        # return super(Sudoku, self).__repr__() 

############ CODE BLOCK 11 ################
    def set_grid(self, grid):
        """
        This method sets a new grid. This also can change the size of the sudoku.

        :param grid: A 2D numpy array that contains the digits for the grid.
        :type grid: ndarray[(Any, Any), int]
        """
        self.grid = grid
        self.size = grid.shape[0]

############ CODE BLOCK 12 ################
    def get_row(self, row_id):
        """
        This method returns the row with index row_id.

        :param row_id: The index of the row.
        :type row_id: int
        :return: A row of the sudoku.
        :rtype: np.ndarray[(Any,), int]
        """
        row = self.grid[row_id, :]
        return row

    def get_col(self, col_id):
        """
        This method returns the column with index col_id.

        :param col_id: The index of the column.
        :type col_id: int
        :return: A row of the sudoku.
        :rtype: np.ndarray[(Any,), int]
        """
        column = self.grid[:, col_id]
        return column

    def get_box_index(self, row, col):
        """
        This returns the box index of a cell given the row and column index.
        
        :param col: The column index.
        :type col: int
        :param row: The row index.
        :type row: int
        :return: This returns the box index of a cell.
        :rtype: int
        """
        num_box = int(np.sqrt(self.size))
        box_row = row // num_box
        box_col = col // num_box
        box_index = box_row * num_box + box_col
        return box_index

    def get_box(self, box_id):
        """
        This method returns the "box_id" box.

        :param box_id: The index of the sudoku box.
        :type box_id: int
        :return: A box of the sudoku.
        :rtype: np.ndarray[(Any, Any), int]
        """
        num_box = int(np.sqrt(self.size))
        first_row = (box_id // num_box) * num_box
        first_col = (box_id % num_box) * num_box
        box = self.grid[first_row:first_row+num_box, first_col:first_col+num_box]
        return box

############ CODE BLOCK 13 ################
    @staticmethod
    def is_set_correct(numbers):
        """
        This method checks if a set (row, column, or box) is correct according to the rules of a sudoku.
        In other words, this method checks if a set of numbers contains duplicate values between 1 and the size of the sudoku.
        Note, that multiple empty cells are not considered duplicates.

        :param numbers: The numbers of a sudoku's row, column, or box.
        :type numbers: np.ndarray[(Any, Any), int] or np.ndarray[(Any, ), int]
        :return: This method returns if the set is correct or not.
        :rtype: Boolean
        """
        # if numbers is a box, flatten it
        if numbers.ndim == 2:
            numbers = numbers.flatten()
        checked = set()
        for number in numbers:
            if number == 0:
                continue
            elif number < 0 or number > len(numbers):
                return False
            elif number in checked:
                return False
            checked.add(number)
        return True   

    def check_cell(self, row, col):
        """
        This method checks if the cell, denoted by row and column, is correct according to the rules of sudoku.
        
        :param col: The column index that is tested.
        :type col: int
        :param row: The row index that is tested.
        :type row: int
        :return: This method returns if the cell, denoted by row and column, is correct compared to the rest of the grid.
        :rtype: boolean
        """
        cell = self.grid[row,col]
        if cell == 0:  
            return True

        #checking row and column
        row_is_correct = self.is_set_correct(self.get_row(row))
        if not row_is_correct:
            return False
        
        col_is_correct = self.is_set_correct(self.get_col(col))
        if not col_is_correct:
            return False
        
        #check box
        box_idx = self.get_box_index(row, col)
        box = self.get_box(box_idx)
        if not self.is_set_correct(box):
            return False
        
        return True

    def check_sudoku(self):
        """
        This method checks, for all rows, columns, and boxes, if they are correct according to the rules of a sudoku.
        In other words, this method checks, for all rows, columns, and boxes, if a set of numbers contains duplicate values between 1 and the size of the sudoku.
        Note, that multiple empty cells are not considered duplicates.

        Hint: It is not needed to check if every cell is correct to check if a complete sudoku is correct.

        :return: This method returns if the (partial) Sudoku is correct.
        :rtype: Boolean
        """
        num_box = int(np.sqrt(self.size))
        # Check rows
        for row_idx in range(self.size):
            row_numbers = self.get_row(row_idx)
            if not self.is_set_correct(row_numbers):
                return False
        # Check columns
        for col_idx in range(self.size):
            col_numbers = self.get_col(col_idx)
            if not self.is_set_correct(col_numbers):
                return False
        # Check boxes
        for box_idx in range(self.size):
            box = self.get_box(box_idx)
            if not self.is_set_correct(box):
                return False
        return True

       

############ CODE BLOCK 14 ################
    def step(self, row=0, col=0, backtracking=True):
        """
        This is a recursive method that completes one step in the exhaustive search algorithm.
        A step should contain at least, filling in one number in the sudoku and calling "next_step" to go to the next step.
        If the current number for this step does not give a correct solution another number should be tried 
        and if no numbers work the previous step should be adjusted.

        This method should work for both backtracking and exhaustive search.
        
        Hint 1: Numbers, that are already filled in should not be overwritten.
        Hint 2: Think about a base case.
        Hint 3: The step method from the previous jupyter notebook cell can be copy-paste here and adjusted for backtracking.
    
        :param col: The current column index.
        :type col: int
        :param row: The current row index.
        :type row: int
        :param backtracking: This determines if backtracking is used, defaults to False.
        :type backtracking: boolean, optional
        :return: This method returns if a correct solution can be found using this step.
        :rtype: boolean
        """
        # base case: if we reach the last cell, return the checked result
        # if row == self.size - 1 and col == self.size - 1:
        if row == self.size and col == 0:
            return self.check_sudoku()

        if self.grid[row, col] != 0:
            return self.next_step(row, col, backtracking)

        # loop over all possible values to fill in the current cell
        for num in range(1, self.size + 1):
            self.grid[row, col] = num
            print(f"backtrack: trying {num} for {row, col}")
            if self.check_sudoku():
                # move to the next cell
                if self.next_step(row, col, backtracking):
                    print("True")
                    return True

        self.clean_up(row, col)
        print("False")
        return False

    def next_step(self, row, col, backtracking=True):
        """
        This method calculates the next step in the recursive exhaustive search algorithm.
        This method should only determine which cell should be filled in next.

        This method should work for both backtracking and exhaustive search.
        
        :param col: The current column index.
        :type col: int
        :param row: The current row index.
        :type row: int
        :param backtracking: This determines if backtracking is used, defaults to False.
        :type backtracking: boolean, optional
        :return: This method returns if a correct solution can be found using this next step.
        :rtype: boolean
        """
        next_col = (col + 1) % self.size
        if next_col == 0:
            next_row = row + 1
        else:
            next_row = row
        if self.step(next_row, next_col, backtracking=True):
            return True
        else:
            return False
    
    def clean_up(self, row, col):
        """
        This method cleans up the current cell if no solution can be found for this cell.

        This method should work for both backtracking and exhaustive search.
        
        :param col: The current column index.
        :type col: int
        :param row: The current row index.
        :type row: int
        :return: This method returns if a correct solution can be found using this next step.
        :rtype: boolean
        """
        self.grid[row, col] = 0
    
    def solve(self, backtracking=True):
        """
        Solve the sudoku using recursive exhaustive search or backtracking.
        This is done by calling the "step" method, which does one recursive step.
        This can be visualized as a process tree, where "step" completes the functionality of of node.
        
        This method is already implemented and you do not have to do anything here.

        :param backtracking: This determines if backtracking is used, defaults to False.
        :type backtracking: boolean, optional
        :return: This method returns if a correct solution for the whole sudoku was found.
        :rtype: boolean
        """
        return self.step(backtracking=backtracking)


############ END OF CODE BLOCKS, START SCRIPT BELOW! ################
