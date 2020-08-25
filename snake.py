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
        self.size = 5
        self.shape = []


class food:
    def __init__(self):
        pass

class program:
    def __init__(self):
        self.field = field()
        self.gui = Tk()
        self.gui.title("Snake Means Python")
        self.c_free = '#DDDDDD'
        self.c_snake = '#0000FF'
        self.c_food = '#00FF00'
        self.direction = 'right'


        self.createme()
        self.placewindow()
        self.spawn()
        self.move()
    
    def move(self):
        if self.direction == 'right':
            self.snake.head[1] += 1
            self.field.array[self.snake.head[0]][self.snake.head[1]] = 1
            self.snake.shape.append([(self.snake.head[0]),(self.snake.head[1])])
            exec("self.cell_{}.config(bg='{}')".format(str(self.snake.head[0])+'_'+str(self.snake.head[1]), self.c_snake))
            exec("self.cell_{}.config(bg='{}')".format(str(self.snake.shape[0])+'_'+str(self.snake.shape[1]), self.c_free))
            del self.snake.shape[0]
        

    def createme(self):
        for i in range(self.field.height):
            for j in range(self.field.width):
                exec("self.cell_{0} = Canvas(self.gui, width={3}, height={3}, highlightthickness=1,  relief='sunken', bd=1, bg=self.c_free)\n" 
                "self.cell_{0}.grid(row={1}, column={2})".format(str(i)+'_'+str(j),i,j, self.field.cellsize))
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