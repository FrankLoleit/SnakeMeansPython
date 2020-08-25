from tkinter import *

class field:
    def __init__(self):
        self.height = 40
        self.width = 40
        self.cellsize= 15
        self.array = []
        for i in range(self.height):
            self.array.append([])
            for j in range(self.width):
                self.array[i].append(0)

class snake:
    def __init__(self):
        self.size = 12
        self.shape = []

class food:
    def __init__(self):
        pass

class program:
    def __init__(self):
        self.field = field()
        self.gui = Tk()
        self.gui.title("Snake Means Python")
        self.gui.config(bg='#FFFFFF')
        self.c_free = '#000000'
        self.c_snake = '#0000FF'
        self.c_food = '#00FF00'
        self.directions = ['right']
        self.direction = self.directions[0]
        self.eaten = False
        self.gameover = False
        self.gui.bind('<Left>', self.left)
        self.gui.bind('<Right>', self.right)
        self.gui.bind('<Up>', self.up)
        self.gui.bind('<Down>', self.down)
        self.gui.bind('<p>', self.pause)
        self.setdirection = False

        self.createme()
        self.placewindow()
        self.spawn()
        self.nextturn()

    def left(self, event):
        if not self.direction == 'right':
            self.directions.append('left')
            self.setdirection = True
 

    def right(self, event):
        if not self.direction == 'left':
            self.directions.append('right')
            self.setdirection = True


    def up(self, event):
        if not self.direction == 'up':

            self.directions.append('up')
            self.setdirection = True


    def down(self, event):
        if not self.direction == 'down':
            self.directions.append('down')
            self.setdirection = True

    def nextturn(self):
        if not self.gameover:
            self.move()
            self.gui.after(70, self.nextturn)

    def pause(self):
        pass


    def move(self):
        if len(self.directions) > 2:
            del self.directions[0]
        if self.direction == self.directions[-1]:
            self.direction = self.directions[-1]
        else:
            self.direction = self.directions[0]
        if self.direction == 'right':
            self.snake.head[1] += 1
            if self.snake.head[1] > self.field.width - 1:
                self.snake.head[1] = 0
        elif self.direction == 'left':
            self.snake.head[1] -= 1
            if self.snake.head[1] < 0:
                self.snake.head[1] = self.field.width - 1
        elif self.direction == 'up':
            self.snake.head[0] -= 1
            if self.snake.head[0] < 0:
                self.snake.head[0] = self.field.height - 1
        else:
            self.snake.head[0] += 1
            if self.snake.head[0] > self.field.height - 1:
                self.snake.head[0] = 0
        #if self.field.array[self.snake.head[0]][self.snake.head[1]] == 1:
            #self.gameover = True
        self.field.array[self.snake.head[0]][self.snake.head[1]] = 1
        self.snake.shape.append([(self.snake.head[0]),(self.snake.head[1])])
        exec("self.cell_{}.config(bg='{}')".format(str(self.snake.head[0])+'_'+str(self.snake.head[1]), self.c_snake))
        exec("self.cell_{}.config(bg='{}')".format(str(self.snake.shape[0][0])+'_'+str(self.snake.shape[0][1]), self.c_free))


        if not self.eaten:
            del self.snake.shape[0]
            self.eaten = False
        if self.setdirection:
            del self.directions[0]
            self.setdirection = False

        

    def createme(self):
        for i in range(self.field.height):
            for j in range(self.field.width):
                exec("self.cell_{0} = Canvas(self.gui, width={3}, height={3}, highlightthickness=0,  bg=self.c_free)"
                .format(str(i)+'_'+str(j),i,j, self.field.cellsize))
        for i in range(self.field.height):
            for j in range(self.field.width):
                exec("self.cell_{0}.grid(row={1}, column={2})".format(str(i)+'_'+str(j),i,j, self.field.cellsize))
        self.gui.update_idletasks()

    def placewindow(self):
        self.x = self.gui.winfo_screenwidth()//2 - self.gui.winfo_width()//2
        self.y = self.gui.winfo_screenheight()//2 - self.gui.winfo_height()//2
        self.gui.geometry('{}x{}+{}+{}'.format(self.gui.winfo_width(), self.gui.winfo_height(),self.x, self.y))


    def spawn(self):
        self.snake = snake()
        self.snake.head = [self.field.height//2, 0]
        for i in range(self.snake.size):
            self.snake.head[1] += 1
            self.field.array[self.snake.head[0]][self.snake.head[1]] = 1
            self.snake.shape.append([(self.snake.head[0]),(self.snake.head[1])])
            exec("self.cell_{}.config(bg='{}')".format(str(self.snake.head[0])+'_'+str(self.snake.head[1]), self.c_snake))
            #print(self.snake.head)
        #print(self.snake.shape)
        print(self.field.array[self.snake.head[0]])


            
game = program()
game.gui.mainloop()
