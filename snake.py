from tkinter import * #for "graphics"
import random #for randomly placed food
import time # only for game-over-flashlight

class field:
    def __init__(self):
        self.height = 20
        self.width = 20
        self.cellsize= 23 # only vor visuals
        self.array = [] # initialize array
        for i in range(self.height): # create array 40*40
            self.array.append([])
            for j in range(self.width):
                self.array[i].append(0)

class snake:
    def __init__(self):
        self.size = 2 #will change after every eaten food
        self.shape = [] # init shape array. Sublists of Y and X values will be added/deleted after every move

class program:
    def __init__(self):
        self.field = field() # create field object
        self.gui = Tk() # init TK
        self.gui.title("Snake Means Python")
        self.gui.config(bg='#888888') # Set colors: black: free cell, blue: snake, green: food, red/white: gameover animation
        self.c_free = '#000000'
        self.c_snake = '#0000FF'
        self.c_food = '#00FF00'
        self.c_red = '#FF0000'
        self.c_white = '#FFFFFF'
        self.directions = ['right']
        self.direction = self.directions[0] # set starting direction
        self.eaten = False
        self.pause = False
        self.gameover = False
        self.gui.bind('<Left>', self.left)  # Keys: up, down, left, right
        self.gui.bind('<Right>', self.right)
        self.gui.bind('<Up>', self.up)
        self.gui.bind('<Down>', self.down)
        self.gui.bind('<p>', self.pausegame)
        self.gui.bind('<n>', self.newgame)
        self.gui.bind('<q>', self.quitgame)
        self.setdirection = False
        self.points = 0
        try:
            self.highfile = open('highscore.txt','r')
            self.highscore = int(self.highfile.read())
        except:
            self.highfile = open('highscore.txt','w')
            self.highfile.write('0')
            self.highfile = open('highscore.txt','r')
            self.highscore = int(self.highfile.read())

        self.createme()
        self.placewindow()
        self.spawn()
        self.setfood()
        self.nextturn()

    def quitgame(self, event):
        self.gui.quit()

    def newgame(self, event):
        self.pga.config(text='p: Pause Game')
        self.points = 0
        self.pointscounter.config(text="0")
        for i in range(self.field.height):
            for j in range(self.field.width):
                self.field.array[i][j] = 0
                exec("self.cell_{}.config(bg='{}')".format(str(i)+'_'+str(j),self.c_free))
        self.spawn()
        self.setfood()
        if self.pause or self.gameover:
            self.gameover = False
            self.pause = False
            self.nextturn()
            

    def setfood(self):
        self.freespace = []
        for i in range(self.field.height):
            for j in range(self.field.width):
                if not self.field.array[i][j]:
                    self.freespace.append([i,j])
        self.food = random.choice(self.freespace)
        self.field.array[self.food[0]][self.food[1]] = 2
        exec("self.cell_{}.config(bg='{}')".format(str(self.food[0])+'_'+str(self.food[1]), self.c_food))

    def endgame(self):
        for i in range(20):
            if (i + 2) % 2 == 0:
                exec("self.cell_{}.config(bg='{}')".format(str(self.snake.head[0])+'_'+str(self.snake.head[1]), self.c_white))
            else:
                exec("self.cell_{}.config(bg='{}')".format(str(self.snake.head[0])+'_'+str(self.snake.head[1]), self.c_red))
            self.gui.update_idletasks()
            time.sleep(1/16)  
            self.pga.config(text='GAME OVER') 
            if self.points > self.highscore:
                self.highscore = self.points
                self.highfile = open('highscore.txt','w+')
                self.highfile.write(str(self.highscore))
                self.highfile = open('highscore.txt', 'r')    
                self.highs.config(text=self.highscore)             
        
    def left(self, event):
        if not self.direction == 'left':
            self.directions.append('left')
            self.setdirection = True
 
    def right(self, event):
        if not self.direction == 'right':
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
            if not self.pause:
                self.move()
                self.gui.after(70, self.nextturn)

    def pausegame(self, event):
        if not self.gameover:
            if not self.pause:
                self.pause = True
                self.pga.config(text='p: Continue Game')
            else:
                self.pause = False
                self.pga.config(text='p: Pause Game')
                self.nextturn()

    def move(self):
        if len(self.directions) > 1:
            del self.directions[0]

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
        if self.field.array[self.snake.head[0]][self.snake.head[1]] == 2:
            self.eaten = True
            self.setfood()
        elif self.field.array[self.snake.head[0]][self.snake.head[1]] == 1:
            self.gameover = True
        self.field.array[self.snake.head[0]][self.snake.head[1]] = 1
        self.snake.shape.append([(self.snake.head[0]),(self.snake.head[1])])
        exec("self.cell_{}.config(bg='{}')".format(str(self.snake.head[0])+'_'+str(self.snake.head[1]), self.c_snake))
        
        if not self.eaten:
            self.field.array[self.snake.shape[0][0]][self.snake.shape[0][1]] = 0
            exec("self.cell_{}.config(bg='{}')".format(str(self.snake.shape[0][0])+'_'+str(self.snake.shape[0][1]), self.c_free))
            del self.snake.shape[0]
        else:
            self.points += 100
            self.pointscounter.config(text=self.points)
            self.eaten = False
        if self.gameover:
            self.endgame()

    def createme(self):
        for i in range(self.field.height):
            for j in range(self.field.width):
                exec("self.cell_{0} = Canvas(self.gui, width={3}, height={3}, highlightthickness=0,  bg=self.c_free)"
                .format(str(i)+'_'+str(j),i,j, self.field.cellsize))
        for i in range(self.field.height):
            for j in range(self.field.width):
                exec("self.cell_{0}.grid(row={1}, column={2})".format(str(i)+'_'+str(j),i,j, self.field.cellsize))

        self.gameboard = Frame(self.gui, relief = 'sunken', bd=1)
        self.gameboard.grid(row = 0, column = self.field.width, rowspan = self.field.height, sticky = N)

        self.pointstitle = Label(self.gameboard, width = 20, bg='#000000', text = 'Points:', font=("Arial", 25), anchor = W,
        relief = 'groove', fg='#FFFFFF')
        self.pointstitle.grid(row = 0, column = 0)

        self.pointscounter = Label(self.gameboard, width = 20, bg='#000000', text=self.points, font=("Arial", 25), anchor=W,
        relief ='groove',fg='#FFFFFF')
        self.pointscounter.grid(row = 1, column = 0, sticky = W)

        self.null = Label(self.gameboard, width = 20, bg='#000000', text='', font=("Arial", 25), anchor=W,
        relief ='groove',fg='#FFFFFF')
        self.null.grid(row = 2, column = 0, sticky = W)

        self.hightitle = Label(self.gameboard, width = 20, bg='#000000', text = 'Highscore:', font=("Arial", 25), anchor = W,
        relief = 'groove', fg='#FFFFFF')
        self.hightitle.grid(row = 3, column = 0)

        self.highs = Label(self.gameboard, width = 20, bg='#000000', text=self.highscore, font=("Arial", 25), anchor=W,
        relief ='groove',fg='#FFFFFF')
        self.highs.grid(row = 4, column = 0, sticky = W)

        self.null = Label(self.gameboard, width = 20, bg='#000000', text='', font=("Arial", 25), anchor=W,
        relief ='groove',fg='#FFFFFF')
        self.null.grid(row = 5, column = 0, sticky = W)

        self.pga = Label(self.gameboard, width = 20, bg='#000000', text='p: Pause Game', font=("Arial", 25), anchor=W,
        relief ='groove',fg='#FFFFFF')
        self.pga.grid(row = 6, column = 0, sticky = W)

        self.ng = Label(self.gameboard, width = 20, bg='#000000', text='n: New Game', font=("Arial", 25), anchor=W,
        relief ='groove',fg='#FFFFFF')
        self.ng.grid(row = 7, column = 0, sticky = W)

        self.qg = Label(self.gameboard, width = 20, bg='#000000', text='q: Quit Game', font=("Arial", 25), anchor=W,
        relief ='groove',fg='#FFFFFF')
        self.qg.grid(row = 8, column = 0, sticky = W)

        self.gui.update_idletasks()

    def placewindow(self):
        self.x = self.gui.winfo_screenwidth()//2 - self.gui.winfo_width()//2
        self.y = self.gui.winfo_screenheight()//2 - self.gui.winfo_height()//2
        self.gui.geometry('{}x{}+{}+{}'.format(self.gui.winfo_width(), self.gui.winfo_height(),self.x, self.y))

    def spawn(self):
        self.snake = snake()
        self.directions = ['right']
        self.direction = self.directions[0]
        self.snake.head = [self.field.height//2, 0]
        for i in range(self.snake.size):
            self.snake.head[1] += 1
            self.field.array[self.snake.head[0]][self.snake.head[1]] = 1
            self.snake.shape.append([(self.snake.head[0]),(self.snake.head[1])])
            exec("self.cell_{}.config(bg='{}')".format(str(self.snake.head[0])+'_'+str(self.snake.head[1]), self.c_snake))
            
game = program()
game.gui.mainloop()
