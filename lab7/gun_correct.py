from random import randrange as rnd, choice
import tkinter as tk
import math
import time

# print (dir(math))



class Ball():
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball
		Args:
		x - начальное положение мяча по горизонтали
		y - начальное положение мяча по вертикали
		"""
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
		        self.x - self.r,
                self.y - self.r,
		        self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 30
    def hide(self):
        #self.id = canv.create_oval(
        #    self.x - self.r,
        #    self.y - self.r,
        #    self.x + self.r,
        #    self.y + self.r,
        #    fill='white',
        #    outline= 'white'
        #)
        self.y = self.x = -10
        self.set_coords()



    def set_coords(self):
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.
		Метод описывает перемещение мяча за один кадр перерисовки.
	    То есть, обновляет значения self.x и self.y с учетом 
		скоростей self.vx и self.vy, силы гравитации, действующей 
        на мяч, и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        self.x += self.vx
        self.y -= self.vy
        self.set_coords()

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с 
		целью, описываемой в обьекте obj.
		Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В 
			противном случае возвращает False.
        """
        #FIXME
        if ((self.x - obj.x)**2 + (self.y - obj.y)**2)**1/2 <=\
        self.r + obj.r:
            return True
        else:
            return False
		

class Gun():
    #FIXME:
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20,450,50,420, width=7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
		Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят
		от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball()
        new_ball.r += 5
        self.an = math.atan((event.y-new_ball.y) / (event.x-\
				  new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y-450) / (event.x-20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class Target():
    def __init__(self):
        #self.points = 0
        self.live = 1
        self.id = canv.create_oval(0,0,0,0)
        #self.id_points = canv.create_text(30,30,text =\
		#						self.points,font = '28')
        self.new_target()
        # FIXME: don't work!!! How to call this functions when object is created?
    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        color = self.color = 'red'
        canv.coords(self.id, x-r, y-r, x+r, y+r)
        canv.itemconfig(self.id, fill=color)

        self.an = math.atan(self.y / self.x)
        self.vx = math.cos(self.an)
        self.vy = math.sin(self.an)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)
        #self.points += points
        #canv.itemconfig(self.id_points, text=self.points)

    def move(self):
        if self.x + self.vx <= 0 + self.r or self.x + self.vx > 800 - self.r:
            self.vx = -self.vx
        if self.y + self.vy <= 0 + self.r or self.y + self.vy > 600 - self.r:
            self.vy = -self.vy
        self.x += self.vx
        self.y += self.vy
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)

def new_game():
    global g1, t1, screen1, balls, bullet

    target_count = 2
    targets = []
    for i in range(0, target_count):
        targets.append(Target())
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)

    #z = 0.03
    target_live = 2
    while targets: #or balls:
        for b in balls:
            b.move()
            i = 0
            while i < len(targets):
                if b.hittest(targets[i]):
                    targets[i].hit()
                    del targets[i]
                else:
                    i += 1
            for target in targets:
                target.move()
            if not targets:
                canv.bind('<Button-1>', '')
                canv.bind('<ButtonRelease-1>', '')
                canv.bind('<Motion>', '')
                canv.itemconfig(screen1, text='Вы уничтожили' +\
					' цель за ' + str(bullet) + ' выстрелов')
                break
        canv.update()
        time.sleep(0.03)
        g1.targetting()
        g1.power_up()
    for ball in balls:
        ball.hide()
    bullet = 0
    balls = []
    time.sleep(1.0)
    canv.itemconfig(screen1, text='')
    root.after(750, new_game)


root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)

#t1 = Target()
screen1 = canv.create_text(400, 300, text='', font='28')
g1 = Gun()
bullet = 0
balls = []


new_game()


tk.mainloop()
