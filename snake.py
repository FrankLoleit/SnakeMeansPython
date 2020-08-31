from tkinter import *  # for the "graphics"
import random  # placing food in random positions
import time  # needed for gameover animation


class field: # play field area
    def __init__(self):
        self.height = 30
        self.width = 30
        self.cellsize = 22 # for visuals
        self.array = [] # init array
        for i in range(self.height): # generate array
            self.array.append([])
            for j in range(self.width):
                self.array[i].append(0)

class snake:
    def __init__(self):
        self.size = 2 # only the starting length, changes after every food catch
        self.shape = [] # needed to store Y and X coordinates of every active snake cell


class program:
    def __init__(self):
        self.field = field() # import play field
        self.gui = Tk() # init TK
        self.gui.title("Snake Means Python")
        self.gui.config(bg='#555555') # colors: black: cell is free, blue: snake, green: food, white, texts, grey, right unused board
        self.c_free = '#000000'
        self.c_snake = '#0000FF'
        self.c_food = '#00FF00'
        self.c_red = '#FF0000'
        self.c_white = '#FFFFFF'
        self.directions = ['right']
        self.direction = self.directions[0] # set starting direction
        self.eaten = False # True after every food catch for 1 round
        self.pause = False
        self.win = False
        self.gameover = False # True after collision
        self.gui.bind('<Left>', self.left) # controls
        self.gui.bind('<Right>', self.right)
        self.gui.bind('<Up>', self.up)
        self.gui.bind('<Down>', self.down)
        self.gui.bind('<p>', self.pausegame)
        self.gui.bind('<n>', self.newgame)
        self.gui.bind('<q>', self.quitgame)
        self.setdirection = False # True for 1 round when a new direction has been set
        self.points = 0
        try:
            self.highfile = open('highscore.txt', 'r') # searches for highscore file. If it doesn't exist creates new file with string '0'
            self.highscore = int(self.highfile.read())
        except:
            self.highfile = open('highscore.txt', 'w')
            self.highfile.write('0')
            self.highfile = open('highscore.txt', 'r')
            self.highscore = int(self.highfile.read())

        self.createme() # creates cells and texts
        self.placewindow() # places the window in middle of screen
        self.spawn() # spawns snake
        self.setfood() # sets food
        self.nextturn() # calls the move function, is repeated every 70ms

    def quitgame(self, event):
        self.gui.quit() # exits program when pressing 'q'

    def newgame(self, event):
        self.win = False
        self.pga.config(text='p: Pause Game') # now you can pause the game again
        self.points = 0
        self.pointscounter.config(text="0") # sets points to 0
        for i in range(self.field.height): # whipes the play field clean, every cell is a 0 now.
            for j in range(self.field.width):
                self.field.array[i][j] = 0
                exec("self.cell_{}.config(bg='{}')".format(str(i) + '_' + str(j), self.c_free))
        self.spawn() # spawns a new snake
        self.setfood() # sets a food cell on a random position
        if self.pause or self.gameover: # activates the game loop again
            self.gameover = False
            self.pause = False
            self.nextturn()

    def setfood(self): # sets randomly food on an unoccupied cell
        self.freespace = [] # candidates list with y and x values
        for i in range(self.field.height):
            for j in range(self.field.width):
                if not self.field.array[i][j]: # if there is no snake on this cell put in in the freelist list
                    self.freespace.append([i, j])
        try:
            self.food = random.choice(self.freespace) # chooses a random x/y-set from the freespace list
            self.field.array[self.food[0]][self.food[1]] = 2 #places 2 for food on the array
            exec("self.cell_{}.config(bg='{}')".format(str(self.food[0]) + '_' + str(self.food[1]), self.c_food)) # sets the food cell to green
        except:
            print('You Win')
            self.gameover = True
            self.win = True

    def endgame(self): # makes the bitten part of the snake flash in white and red
        if not self.win:
            for i in range(20):
                if (i + 2) % 2 == 0: # oscilates 20 times from white to red
                    exec("self.cell_{}.config(bg='{}')".format(str(self.snake.head[0]) + '_' + str(self.snake.head[1]),
                                                               self.c_white))
                else:
                    exec("self.cell_{}.config(bg='{}')".format(str(self.snake.head[0]) + '_' + str(self.snake.head[1]),
                                                               self.c_red))
                self.gui.update_idletasks() # execute color change
                time.sleep(1 / 16) # wait a litte before setting the next color
                self.pga.config(text='GAME OVER') #indicates GAME OVER to the player
        else:
            self.pga.config(text='*** You win!!! ***')
        if self.points > self.highscore: # checks if there is a new highscore
            self.highscore = self.points #if current score is higher than highscore from the highscore file set new hs
            self.highfile = open('highscore.txt', 'w+') #open highscorefile in write mode
            self.highfile.write(str(self.highscore)) # overwrite hs with new hs
            self.highfile = open('highscore.txt', 'r') #open file in readmode
            self.highs.config(text=self.highscore) # display new hs on screen

    def left(self, event):
        if not self.direction == 'left': # if pressed directions is not currently active
            self.directions.append('left') # appends left to directions-list
            self.setdirection = True

    def right(self, event):
        if not self.direction == 'right':  # if pressed directions is not currently active
            self.directions.append('right') # appends right to directions-list
            self.setdirection = True

    def up(self, event):
        if not self.direction == 'up': # if pressed directions is not currently active
            self.directions.append('up') # appends up to directions-list
            self.setdirection = True

    def down(self, event):
        if not self.direction == 'down': # if pressed directions is not currently active
            self.directions.append('down') # appends down to directions-list
            self.setdirection = True

    def nextturn(self): # when not gameover and not pause proceed with game loop
        if not self.gameover:
            if not self.pause:
                self.move()
                self.gui.after(70, self.nextturn) #set the speed to 70ms/turn

    def pausegame(self, event):
        if not self.gameover: # if game over no need to pause the game
            if not self.pause:
                self.pause = True
                self.pga.config(text='p: Continue Game') # changes pause label to continue label
            else:
                self.pause = False # continues game
                self.pga.config(text='p: Pause Game')
                self.nextturn() # starts game loop again

    def move(self): # moves the snake
        if len(self.directions) > 1: #if more than one direction in directions list kill the lates one
            del self.directions[0]

        self.direction = self.directions[0] # takes direction from directions list
        if self.direction == 'right':
            self.snake.head[1] += 1 # snake head X + 1
            if self.snake.head[1] > self.field.width - 1: # if snake head X bigger than play field set back to 0
                self.snake.head[1] = 0
        elif self.direction == 'left':  # snake head X - 1
            self.snake.head[1] -= 1
            if self.snake.head[1] < 0: # if snake head X smaller 0 set back to highest pos
                self.snake.head[1] = self.field.width - 1
        elif self.direction == 'up': # snake head Y - 1
            self.snake.head[0] -= 1
            if self.snake.head[0] < 0:  # if snake head Y smaller 0 set back to highest pos
                self.snake.head[0] = self.field.height - 1
        else:
            self.snake.head[0] += 1 # else=='down', # snake head Y + 1
            if self.snake.head[0] > self.field.height - 1: # if snake head Y higher play field Y set back to 0
                self.snake.head[0] = 0
        if self.field.array[self.snake.head[0]][self.snake.head[1]] == 2: # check if there is food (2) on the new field
            self.eaten = True # if True: snake butt not going to be deleted for 1 round
            self.setfood() # sets new randomly placed food
        elif self.field.array[self.snake.head[0]][self.snake.head[1]] == 1: # if there is 1 on the field snake has bitten itself
            self.gameover = True # game loop is going to stop, score and highscore will be checked
        self.field.array[self.snake.head[0]][self.snake.head[1]] = 1 # sets a new 1 (snake.head) on the play field
        self.snake.shape.append([(self.snake.head[0]), (self.snake.head[1])]) # snake shape gets new head position
        exec("self.cell_{}.config(bg='{}')".format(str(self.snake.head[0]) + '_' + str(self.snake.head[1]),
                                                   self.c_snake)) # new head positions turns from black to blue

        if not self.eaten:
            self.field.array[self.snake.shape[0][0]][self.snake.shape[0][1]] = 0 # snake butt deleted from play field
            exec("self.cell_{}.config(bg='{}')".format(str(self.snake.shape[0][0]) + '_' + str(self.snake.shape[0][1]),
                                                       self.c_free)) # former snake butt turns from blue to black
            del self.snake.shape[0] # snake butt deleted from snake
        else:
            self.points += 100 # 100 points for every catched food
            self.pointscounter.config(text=self.points) # display new score
            self.eaten = False # snake is stuffed now
        if self.gameover:
            self.endgame() # will end the game loop

    def createme(self): # creates play field and gameboard
        for i in range(self.field.height):
            for j in range(self.field.width):
                exec("self.cell_{0} = Canvas(self.gui, width={3}, height={3}, highlightthickness=0,  bg=self.c_free)"
                     .format(str(i) + '_' + str(j), i, j, self.field.cellsize)) # every cell gets row and column in its name, e. g. self.cell_4_16 etc.
        for i in range(self.field.height): # ads the new cell to the program grid
            for j in range(self.field.width):
                exec("self.cell_{0}.grid(row={1}, column={2})".format(str(i) + '_' + str(j), i, j, self.field.cellsize))

        self.gameboard = Frame(self.gui, relief='sunken', bd=1) # Frame on the right side of the play field
        self.gameboard.grid(row=0, column=self.field.width, rowspan=self.field.height, sticky=N)

        self.pointstitle = Label(self.gameboard, width=20, bg='#000000', text='Points:', font=("Arial", 20), anchor=W,
                                 relief='groove', fg='#FFFFFF') # Title for points to display
        self.pointstitle.grid(row=0, column=0)

        self.pointscounter = Label(self.gameboard, width=20, bg='#000000', text=self.points, font=("Arial", 20),
                                   anchor=W,
                                   relief='groove', fg='#FFFFFF') # dynamic: self.points changes after every food catch
        self.pointscounter.grid(row=1, column=0, sticky=W)

        self.null = Label(self.gameboard, width=20, bg='#000000', text='', font=("Arial", 20), anchor=W,
                          relief='groove', fg='#FFFFFF') # empty row
        self.null.grid(row=2, column=0, sticky=W)

        self.hightitle = Label(self.gameboard, width=20, bg='#000000', text='Highscore:', font=("Arial", 20), anchor=W,
                               relief='groove', fg='#FFFFFF') # title for highscore
        self.hightitle.grid(row=3, column=0)

        self.highs = Label(self.gameboard, width=20, bg='#000000', text=self.highscore, font=("Arial", 20), anchor=W,
                           relief='groove', fg='#FFFFFF') # dynamic: changes when game over and score > highscore
        self.highs.grid(row=4, column=0, sticky=W)

        self.null = Label(self.gameboard, width=20, bg='#000000', text='', font=("Arial", 20), anchor=W,
                          relief='groove', fg='#FFFFFF') # empty row
        self.null.grid(row=5, column=0, sticky=W)

        self.pga = Label(self.gameboard, width=20, bg='#000000', text='p: Pause Game', font=("Arial", 20), anchor=W,
                         relief='groove', fg='#FFFFFF') # Displays "Pause Game", "Continue Game" or "Game Over"
        self.pga.grid(row=6, column=0, sticky=W)

        self.ng = Label(self.gameboard, width=20, bg='#000000', text='n: New Game', font=("Arial", 20), anchor=W,
                        relief='groove', fg='#FFFFFF') # displays New Game key
        self.ng.grid(row=7, column=0, sticky=W)

        self.qg = Label(self.gameboard, width=20, bg='#000000', text='q: Quit Game', font=("Arial", 20), anchor=W,
                        relief='groove', fg='#FFFFFF') # displays Quit Game key
        self.qg.grid(row=8, column=0, sticky=W)

        self.gui.update_idletasks() # if you kill this line tkinter doesn't know the size of the widgets for some reason

    def placewindow(self): # places the window in the golden middle of the screen
        self.x = self.gui.winfo_screenwidth() // 2 - self.gui.winfo_width() // 2 # gets window and display size and
        # subtracts them to place the center of the window in the center of the screen
        self.y = self.gui.winfo_screenheight() // 2 - self.gui.winfo_height() // 2
        self.gui.geometry('{}x{}+{}+{}'.format(self.gui.winfo_width(), self.gui.winfo_height(), self.x, self.y))
        # needs a string with the x and y positions calculated above

    def spawn(self): # spawns a snake in the left middle of the play field
        self.snake = snake()
        self.directions = ['right'] # sets direction
        self.direction = self.directions[0] # sets direction
        self.snake.head = [self.field.height // 2, 0] # puts snake head on the screen
        for i in range(self.snake.size): # similiar to move method but without deleting the butt
            self.snake.head[1] += 1 # head moves from left to right
            self.field.array[self.snake.head[0]][self.snake.head[1]] = 1 # head is placed on screen
            self.snake.shape.append([(self.snake.head[0]), (self.snake.head[1])]) # new head position is added to the shape list
            exec("self.cell_{}.config(bg='{}')".format(str(self.snake.head[0]) + '_' + str(self.snake.head[1]),
                                                       self.c_snake)) # cells on screen where with 1 for snake turn from black to blue


game = program() # creating an instance of the whole program
game.gui.mainloop() # starting tkinter's mainloop