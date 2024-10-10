from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.geometry(f"{width}x{height}")
        self.__root.title("Maze Runner")
        self.canvas = Canvas(self.__root, width=width, height=height, bg='white')
        self.canvas.pack()
        self.running = False  
        self.__root.protocol("WM_DELETE_WINDOW", self.close) 

    def redraw(self):
        self.__root.update()
        
            

    def wait_for_close(self):
        self.__root.mainloop() 

    def close(self):
        self.running = False
        self.__root.destroy()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x, self.point1.y, 
            self.point2.x, self.point2.y, 
            fill=fill_color, width=2
        )

class Cell:
    def __init__(self,canvas =None ):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall= True
        self.has_bottom_wall= True
        self._win = canvas
        self.color = "black"
        self.visited = False

    def draw(self, topLeftPoint, bottomRightPoint):
        self._x1 = topLeftPoint.x
        self._x2  = bottomRightPoint.x
        self._y1 = topLeftPoint.y
        self._y2 = bottomRightPoint.y

        # create_rectangle
        self._win.create_rectangle(
            self._x1,
            self._y1,
            self._x2,
            self._y2,
            outline = "white", 
            width=2)
        

        # Top wall
        if self.has_top_wall:
            self._win.create_line(
            self._x1,
            self._y1,
            self._x2,
            self._y1,
            fill = self.color)  
    
        # Left Wall
        if self.has_left_wall:
            self._win.create_line(
            self._x1,
            self._y1,
            self._x1,
            self._y2,
            fill = self.color)
            
        # Right Wall
        if self.has_right_wall:
            self._win.create_line(
            self._x2,
            self._y1,
            self._x2,
            self._y2,
            fill = self.color) 

        # Bottom Wall
        if self.has_bottom_wall:
            self._win.create_line(
            self._x1,
            self._y2,
            self._x2,
            self._y2,
            fill = self.color) 

    def draw_move(self, to_cell, undo =False): # need to have nums_row and num_cols to calc mid point
        if undo:
            color = "gray"
        else:
            color = "red"
        
        p1 = Point((self._x1 + self._x2) /2 , (self._y1 + self._y2)/ 2)
        p2 = Point((to_cell._x1 + to_cell._x2)/2 , (to_cell._y1 + to_cell._y2) / 2 )

        line = Line(p1,p2)
        line.draw(self._win,color)

        
        

class Maze:
    def __init__(self,x1,y1,num_rows,num_cols,cell_size_x,cell_size_y, canvas =None, seed = None ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        # self._win = None # for test
        self._win = canvas
        # self._wins = win
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self.seed = seed
        if self.seed is not None:
            random.seed(self.seed)
         # to recreate random sequence
        
        self._break_walls_r(0,0)

    def _create_cells(self): # notice the cells and not cell
        
        """ Initialize the cells."""
        for col in range(self.num_cols):
            cols = []
            for row in range(self.num_rows):
                cell = Cell(self._win)
                cols.append(cell)
            # print(cols) 
            self._cells.append(cols)
        
        self._draw_all_cells()
        
    def _draw_all_cells(self):
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                self._draw_cell(col, row) 


    def _draw_cell(self,i,j):
        """ Calculate x/y of cell and draw a cell."""

        topLeftPoint = Point(self.x1 + i * self.cell_size_x, self.y1 + j * self.cell_size_y)
      

        bottomRightPoint = Point(self.x1 + (i+1) * self.cell_size_x , self.y1 + (j+1)* self.cell_size_y)

        cell = self._cells[i][j]  # Get the cell
        cell._x1 = topLeftPoint.x  # Update internal state of the cell inside 
        cell._y1 = topLeftPoint.y
        cell._x2 = bottomRightPoint.x
        cell._y2 = bottomRightPoint.y
        cell.draw(topLeftPoint, bottomRightPoint)

        self._animate()
    
    def _break_entrance_and_exit(self):
        # Entrace top-left, Exit bottom-right
        # what cell it is
        # break the wall
        # call draw cell method on each.
        entryCell = self._cells[0][0]
        entryCell.has_top_wall =False
        self._draw_cell(0,0)

        exitCell = self._cells[self.num_cols -1][self.num_rows -1]
        exitCell.has_bottom_wall = False
        self._draw_cell(self.num_cols -1,self.num_rows -1)
        

    def _break_walls_r(self, i, j):
        """Dfs"""
        # self._cells holds the all the nodes
        # find adjacent nodes of current node. 
        # choose random node to visit.
        # recurse until all nodes in self._cells are visited.
        ### rawdogged it, could finesse it.
        
        current_cell = self._cells[i][j]
        current_cell.visited = True

        directions = {
            "top": (0, -1),
            "bottom": (0, 1),
            "right": (1, 0),
            "left": (-1, 0)
        }

        # On edges
        if i == 0:
            del directions["left"]
        if i == self.num_cols - 1:
            del directions["right"]
        if j == 0:
            del directions["top"]
        if j == self.num_rows - 1:
            del directions["bottom"]
       
        adjacentCells = [(i + value[0], j + value[1]) for key, value in directions.items()]
        print(f"({i,j}: {adjacentCells})") 

        random.shuffle(adjacentCells)

        for coordToVisit in adjacentCells:
            x, y = coordToVisit  # col, row
            if not self._cells[x][y].visited:
                # (1,0)
                # (1,1)
                # (1,2)
                if x == i: 
                    if y < j:  
                        current_cell.has_top_wall = False
                        self._cells[x][y].has_bottom_wall = False
                    else:  
                        current_cell.has_bottom_wall = False
                        self._cells[x][y].has_top_wall = False

                elif y == j:  # (0,1),(1,1),(2,1)
                    if x < i:  
                        current_cell.has_left_wall = False
                        self._cells[x][y].has_right_wall = False
                    else: 
                        current_cell.has_right_wall = False
                        self._cells[x][y].has_left_wall = False

                # Update walls
                self._draw_cell(i, j)
                self._draw_cell(x, y)
                ### self._draw_all_cells() slows down.

                # Recur for the next cell
                self._break_walls_r(x, y)

        # for coordToVisit in adjacentCells:
        #      if self._cells[coordToVisit[0]][coordToVisit[1]].visited == False :
        #         self._break_walls_r(coordToVisit[0],coordToVisit[1])
        #         print(coordToVisit)


    def _animate(self):
        win.redraw()     
        time.sleep(0.05) 
                      
                  
        
if __name__ == "__main__":
    win = Window(500, 500)

    maze =Maze(10,10, 10,10,40,40,win.canvas)
    # maze =Maze(3,3, 3,3,40,40,win.canvas)

    # line.draw(win.canvas, "red")
    win.wait_for_close()
