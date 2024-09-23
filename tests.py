import unittest
from tkinter import Tk, Canvas
from maze import Maze, Window

class Tests(unittest.TestCase):
    def test_maze_cells_initialization(self):   
        self.num_cols = 10
        self.num_rows = 9
        self.maze = Maze(0, 0, self.num_rows, self.num_cols, 10, 10)
        self.assertEqual(len(self.maze._cells), self.num_cols)
        self.assertEqual(len(self.maze._cells[0]), self.num_rows) 
    
    def test_break_entrance_and_exit(self):
        self.assertEqual(self.maze._cells[0][0].has_top_wall, False)
        self.assertEqual(self.maze._cells[self.num_cols][self.num_rows].has_bottom_wall, False)


if __name__ == '__main__':
    unittest.main()
