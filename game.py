from pygame import *
import sys, random
import shelve

init()
screen = display.set_mode((1050,1050))
font = font.Font("font.ttf", 50)

shelveFile = shelve.open('shelveData')
high = shelveFile['highScore']
shelveFile.close()

activo = 0
number = 0
a = 0
vidas = 3
score = 0
escena = 1  
fps = 60
timer = time.Clock()
times = 100

def Hi(escena):
    global times, score
    fondo = transform.scale(image.load("./images/start.png"), (1050,1050))

    while True:
        screen.fill((255,255,255))
        for e in event.get():
            if e.type == QUIT: sys.exit()
            if e.type == KEYDOWN: 
                times = 100
                score = 0
                return 2

        screen.blit(fondo, (0,0))

        display.flip()

def Game(escena):
    global numbers, number, a, vidas,fps, times, score,activo,high

    #puras imagenes
    square = transform.scale(image.load("./images/square.png"),(150,150))
    asquare = transform.scale(image.load("./images/asquare.png"),(150,150))
    heart = transform.scale(image.load("./images/heart.png"), (100,100))
    size = 5
    numbers = random.sample(range(size*size),size*size)

    #lista de numeros como imagenes
    list = []
    for n in range(size*size):
        list.append(transform.scale(image.load("./images/"+str(n+1)+".png"),(150,150)))

    while True:
        timer.tick(fps)
        screen.fill((255,255,255))
        for e in event.get():

            if e.type == QUIT: sys.exit()

            if e.type == KEYDOWN and e.key == K_b:
                activo = 0
                vidas = 3
                number = 0
                return 1

            if e.type == MOUSEBUTTONDOWN and e.button==1:
                if times == 0:
                    if activo == numbers[a]:
                        a = a + 1
                        if a > number:
                            number = number + 1
                            numbers = random.sample(range(size*size),size*size)
                            a=0
                            times = 100
                            score = score+10
                            print(score)
                    else: 
                        numbers = random.sample(range(size*size),size*size)
                        a = 0
                        vidas = vidas - 1
                        times = 100
                elif times > 0:
                    times = 0

        #tiempo
        if times > 0:
            times = times - .25


        #vidas
        if vidas == 0:
            vidas = 3
            number = 0
            return 3
        
        #lista de posiciones x,y
        squares = []
        for n in range(size):
            for i in range(size):
                squares.append((i*150+150,n*150+150))

        #render de imagenes de numeros randomizados
        for n in range(number+1):
            if times > 0:
                for i in range(size*size):
                    if numbers[n] == i: screen.blit(list[n],squares[i])

        #activo segun la posicion del mouse
        x, y = mouse.get_pos()
        for n in range(size):
            if y>= n*150+150 and y<= n*150+300 and x>= 150 and x<= 900: activo = n*size + (x-150)//150

        #vidas
        for n in range(vidas):
            screen.blit(heart,(n*100+700,25))

        #animacion de cuadrado seleccionado
        for n in range(size*size):
            if activo == n:
                screen.blit(asquare,(squares[n]))

        #render de imagenes
        tim = font.render('Timer: ' + str(int(times)), True,(0,0,0))
        back = font.render('Press B to go back', True,(0,0,0))
        s = font.render('Score: '+ str(score), True,(0,0,0))
        h = font.render('High Score: '+ str(high), True,(0,0,0))
        screen.blit(back, (50,950))
        screen.blit(s, (400, 50))
        screen.blit(h,(600,950))
        screen.blit(tim , (50,50))

        #creacion de tablero
        for n in range (size):
            for i in range (size):
                screen.blit(square, (n * 150 + 150 ,i * 150 + 150))

        display.flip()

def GameOver(escena):
    global score,high
    gameover = transform.scale(image.load("./images/gameover.png"), (1050,1050))

    while True:
        screen.fill((255,255,255))
        for e in event.get():
            if e.type == QUIT: sys.exit()
            if e.type == KEYDOWN: 
                if score > high:
                    high = score
                return 1

        if score > high:
            shelveFile = shelve.open('shelveData.db')
            highScore = score
            shelveFile['highScore'] = highScore
            shelveFile.close()
            gh = score
            h = font.render('New High Score: '+ str(gh), True,(0,0,0))
            screen.blit(h,(300,150))
        else:
            s = font.render('Final Score: '+ str(score), True,(0,0,0))
            screen.blit(s, (355, 250))
            h = font.render('High Score: '+ str(high), True,(0,0,0))
            screen.blit(h,(355,150))



        screen.blit(gameover, (0,0))

        display.flip()
        
while True:
    if escena==1:
        escena = Hi(escena)
    elif escena==2:
        escena = Game(escena)
    elif escena==3:
        escena = GameOver(escena)
