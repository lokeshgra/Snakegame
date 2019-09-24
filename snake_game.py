import random, pygame , sys
from pygame.locals import *

#width and height of display window in pixels
windowwidth = 640
windowheight = 480

CELLSIZE = 20
CELLWIDTH = int(windowwidth / CELLSIZE)
CELLHEIGHT = int(windowheight / CELLSIZE)

#reading from file highest score of last game
fread = open('score.txt','r')
t = fread.read()
if len(t)==0:
    max_score=0
else:
    max_score=int(t)
#constant color values used in code
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (38, 132, 47)
BROWN     = (165, 42 , 42)
BGCOLOR = (23, 225, 232)
prev_color_food_item = RED
snake_color = GREEN
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 #worm head

def main():
    global fps_clock, display_surface,   BASICFONT , max_score ,windowwidth, windowheight , CELLHEIGHT , CELLWIDTH
    pygame.init()

    fps_clock = pygame.time.Clock()
    #return object of type Surface
    display_surface = pygame.display.set_mode((windowwidth, windowheight),pygame.RESIZABLE)
    #windowwidth, windowheight = pygame.display.get_surface().get_size()
    #CELLWIDTH = int(windowwidth / CELLSIZE)
    #CELLHEIGHT = int(windowheight / CELLSIZE)
    #BASICFONT = pygame.font.Font('fonts/lato_reg.ttf', 20)
    pygame.display.set_caption('Snake Game')
    showStartScreen()
    while True:
        score = runGame()
        if(score > max_score):
            max_score = score
        showGameOverScreen(score)        

def runGame():
    global wallcoords , score
    wallcoords = []
    bonus_coord = {}
    seconds=0
    direction = RIGHT
    FPS = 10
    hit = 0
    prev_score = 0
    score = 0
    ball_eaten = 0
    start_ticks = 0
    bonus = 0
    x = random.randint(5, CELLWIDTH - 6)
    y = random.randint(5, CELLHEIGHT - 6)
    snakecoords = [{'x': x,     'y': y} , {'x': x - 1, 'y': y} , {'x': x - 2, 'y': y}]

    #place the food_item in a random place.
    food_item = getRandomLocation(snakecoords)
    start = False
    while True: 
        for event in pygame.event.get(): 
            start = True
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_p):                              #pause the game
                    #display_surface.fill((23, 225, 232))
                    print_msg('fonts/monster.otf' , (9, 4, 84) , 'Paused.' , {'x':(windowwidth/2) , 'y':100} , 60)
                    print_msg('fonts/monster.otf' , (9, 4, 84) , 'Press \'r\' to resume.' , {'x':(windowwidth/2) , 'y':200} , 30)
                    pygame.display.update()
                    
                    while True:
                        value = checkForKeyPress()
                        if value == 'r':    
                            break
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
        if start:
        	#snake ate food_item
            if snakecoords[HEAD]['x'] == food_item['x'] and snakecoords[HEAD]['y'] == food_item['y']:
                food_item = getRandomLocation(snakecoords) 
                hit = 1
                ball_eaten = ball_eaten + 1
                score = score + 1
            else:
            	#will move one cell forward so deleting last block
                del snakecoords[-1]

            #collision detection with itself
            for snakebody in snakecoords[1:]:
                if snakebody['x'] == snakecoords[HEAD]['x'] and snakebody['y'] == snakecoords[HEAD]['y']:
                	#print "exit"
                	return score
            #collision detection with wall
            for block in wallcoords:
            	for i in range(3):
	                if block[i]['x'] == snakecoords[HEAD]['x'] and block[i]['y'] == snakecoords[HEAD]['y']:
	                	update_score()
	                	del wallcoords[wallcoords.index(block)]	
        	 #setting new coordinates of snake head 
            if direction == UP:
                temp = snakecoords[HEAD]['y'] - 1
                if temp == 0 and mode == 1:
                        return score
                elif temp == 0:
                    temp = CELLHEIGHT -1
                newHead = {'x': snakecoords[HEAD]['x'], 'y': temp }
            elif direction == DOWN:
                temp = snakecoords[HEAD]['y'] + 1
                if temp == CELLHEIGHT and mode == 1:
                        return score
                elif temp == CELLHEIGHT:
                    temp = 1
                newHead = {'x': snakecoords[HEAD]['x'], 'y': temp}
            elif direction == LEFT:
                temp = snakecoords[HEAD]['x'] - 1
                if temp == -1 and mode == 1:
                        return score
                elif temp == -1:
                    temp = CELLWIDTH -1
                newHead = {'x': temp, 'y': snakecoords[HEAD]['y']}
            elif direction == RIGHT:
                temp = snakecoords[HEAD]['x'] + 1
                if temp == CELLWIDTH and mode == 1:
                        return score
                elif temp == CELLWIDTH:
                    temp = 0
                newHead = {'x': temp, 'y': snakecoords[HEAD]['y']}
            snakecoords.insert(0, newHead)
		      #setting background colour of game 
        display_surface.fill((121, 211, 242))  
        drawGrid()
        drawsnake(snakecoords)	                    
        if(ball_eaten >= 5):
            if hit and ball_eaten%5 == 0:
            	#printing wall of 3 blocks if score is a mutliple of 5                
                bonus_coord=get_coord_bonus_food_item(food_item,snakecoords)
                start_ticks=pygame.time.get_ticks()
                setWall()               
                bonus = 1
                draw_bonus_food_item(bonus_coord)
        if  ball_eaten >= 5 and ball_eaten < 10:
            FPS = 14
        elif ball_eaten >= 10 and ball_eaten <15:
            FPS = 17
        elif ball_eaten >= 15 and ball_eaten <20:
            FPS = 19
        elif ball_eaten >=25:
            FPS = 22

        #handling bonus ball timer
        #print "in"            
        if bonus:
            seconds=(pygame.time.get_ticks()-start_ticks)/1000
            if seconds >= 5:
                bonus = 0
            else:
                if snakecoords[HEAD]['x'] == bonus_coord['x'] and snakecoords[HEAD]['y'] == bonus_coord['y']:
                    score = score + 3
                    bonus = 0
				#print str(bonus_coord['x'])+" "+str(bonus_coord['y'])
                draw_bonus_food_item(bonus_coord)

        
        drawfood_item(food_item,hit)
        drawScore(ball_eaten,score,bonus,seconds)
        drawblocks()
        hit = 0
        pygame.display.update()
        fps_clock.tick(FPS)

def get_coord_bonus_food_item(food_item,snakecoords):
	temp = getRandomLocation(snakecoords)
	while temp['x'] == food_item['x'] and temp['y']==food_item['y']:
		temp = getRandomLocation(snakecoords)
	return temp

def draw_bonus_food_item(temp):	
	x = temp['x'] * CELLSIZE
	y = temp['y'] * CELLSIZE
	#pygame.draw.circle(display_surface, BLACK,(x+(CELLSIZE/2),y+(CELLSIZE/2)),(CELLSIZE))
	pygame.draw.polygon(display_surface, BLACK, ( ( x+(CELLSIZE/2) , y ),( x+(CELLSIZE) ,
 y+ (CELLSIZE/2) ),( x+(CELLSIZE/2) , y+ (CELLSIZE) ) ,( x, y+ (CELLSIZE/2) ) ) )	

def update_score():
	global score
	if score < 3:
		score = 0
	else: 
		score=score-3

#draws grid of cellsize = CELLSIZE  
def drawGrid():
    for x in range(0, windowwidth, CELLSIZE): 
        pygame.draw.line(display_surface, BLACK, (x, CELLSIZE), (x, windowheight))
    for y in range(CELLSIZE, windowheight, CELLSIZE):
        pygame.draw.line(display_surface, BLACK, (0, y), (windowwidth, y))


def drawsnake(snakecoords):
    for coord in snakecoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        pygame.draw.rect(display_surface, snake_color, (x, y, CELLSIZE, CELLSIZE))  
        #draw eye on head block
        x = snakecoords[0]['x'] * CELLSIZE
        y = snakecoords[0]['y'] * CELLSIZE
        pygame.draw.circle(display_surface, BLACK, (x+10,y+10) , 4)


def drawfood_item(coord , hit ):
    global color , prev_color_food_item , snake_color
    if hit == 1:
        R=random.randint(0,150)
        G=random.randint(0,150)
        B=random.randint(0,150)
        color = (R,G,B)
        snake_color = prev_color_food_item
        prev_color_food_item = color
    else :
        color = prev_color_food_item
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    #pygame.draw.polygon(display_surface, color, ( ( x+(CELLSIZE/2) , y ),( x+(CELLSIZE) ,
     #y+ (CELLSIZE/2) ),( x+(CELLSIZE/2) , y+ (CELLSIZE) ) ,( x, y+ (CELLSIZE/2) ) ) )
  #  display_surface.blit(food_itemImg,(x,y))
    # pygame.draw.circle(display_surface, BLACK, (x+10,y+10) , 4)
    pygame.draw.circle(display_surface, color,(x+10,y+10),(10))



def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    if keyUpEvents[0].key == K_1 or keyUpEvents[0].key == K_KP1:
        return 1
    if keyUpEvents[0].key == K_2 or keyUpEvents[0].key == K_KP2:
        return 2
    if keyUpEvents[0].key == K_r:
        return 'r'
    return None

def print_msg(font_loc , color , msg , coord , font_size):
    ScreenSurf = pygame.font.Font(font_loc,font_size).render(msg , True , color)
    ScreenRect = ScreenSurf.get_rect()									#returns a rectangle on display with topleft = (0,0)
    ScreenRect.midtop = (coord['x'] , coord['y'])
    display_surface.blit(ScreenSurf,ScreenRect)

def showStartScreen():
    FPS = 15
    global mode
    display_surface.fill(BGCOLOR)
    print_msg('fonts/cs_regular.ttf' , (9, 4, 84) , 'Snake' , {'x':(windowwidth/2) , 'y':10} , 180)
    print_msg('fonts/monster.otf' , BLACK , 'Enter your choice' , {'x':(windowwidth/2) , 'y':120} , 40)
    print_msg('fonts/monster.otf' , BLACK , '1.Bounded mode' , {'x':(windowwidth/2)-20 , 'y':180} , 30)
    print_msg('fonts/monster.otf' , BLACK , '2.Unbounded mode' , {'x':(windowwidth/2) , 'y':220} , 30)
    
    while True:
        mode = checkForKeyPress()
        if mode == 1 or mode == 2:
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        fps_clock.tick(FPS)


def terminate():
    fread.close()
    fwrite = open('score.txt','w')
    fwrite.write(str(max_score))
    fwrite.close()  
    pygame.quit()
    sys.exit()

def getRandomLocation(snakecoords):
    temp = {'x':  random.randint(0,CELLWIDTH-1) , 'y': random.randint(1,CELLHEIGHT -1)}   
    for i in range(len(wallcoords)):
        for j in range(3):
	        if (wallcoords[i][j]['x'] == temp['x'] and wallcoords[i][j]['y'] == temp['y']) or ( snakecoords[HEAD]['x'] == temp['x'] and snakecoords[HEAD]['x'] == temp['x'] ):
	            temp = {'x':  random.randint(0,CELLWIDTH-1) , 'y': random.randint(1,CELLHEIGHT -1)}   
	            i=0
	            break
    return temp
    
def showGameOverScreen(score):
    global  prev_color_food_item , snake_color , max_score ,mode
    display_surface.fill(BGCOLOR)
    print_msg('fonts/cs_regular.ttf' , BLACK , 'Game Over' , {'x':(windowwidth/2) , 'y':30} , 80)
    
    print_msg(None , BLACK , 'Score: %s' % (score) , {'x':(windowwidth/2) , 'y':100} , 60)
    print_msg(None , BLACK , 'Highest Score: %s' % (max_score) , {'x':(windowwidth/2) , 'y':180} , 60)
    print_msg('fonts/cs_regular.ttf' , BLACK , 'Enter your choice' , {'x':(windowwidth/2) , 'y':250} , 60)
    print_msg('fonts/monster.otf' , BLACK , '1.Bounded mode' , {'x':(windowwidth/2)-20 , 'y':300} , 30)
    print_msg('fonts/monster.otf' , BLACK , '2.Unbounded mode' , {'x':(windowwidth/2) , 'y':340} , 30)
    
    prev_color_food_item = RED
    snake_color = GREEN
    
    pygame.display.update()
    pygame.time.wait(500)
    while True:
        mode = checkForKeyPress()
        if mode == 1 or mode == 2:
            pygame.event.get() # clear event queue
            return
def setWall():
    x = random.randint(2,CELLWIDTH-6)
    y = random.randint(2,CELLHEIGHT-6)
    alt =random.randint(0,1)
    if(alt):
        wallcoords.append([{'x': x,     'y': y} , {'x': x + 1, 'y': y} , {'x': x + 2, 'y': y}])
    else:
        wallcoords.append([{'x': x,     'y': y} , {'x': x , 'y': y+1} , {'x': x , 'y': y+2}])
    #print wallcoords[-1]['x'] , wallcoords[-1]['y']

def drawblocks():
    for coord in wallcoords:
    	for i in range(3):
	        x = coord[i]['x'] * CELLSIZE
	        y = coord[i]['y'] * CELLSIZE
        #print x , y
        	pygame.draw.rect(display_surface, BROWN, pygame.Rect(x, y, CELLSIZE, CELLSIZE))

def drawScore(ball_eaten,score,bonus , time):
    level = 'Level : Newbie'
    print_msg('fonts/cs_regular.ttf' , BLACK , 'Score: %s' % (score) , {'x':(windowwidth/2) , 'y':10} , CELLSIZE)
    if bonus:
    	
    	print_msg('fonts/cs_regular.ttf' , BLACK , 'TIME LEFT: %s' %(5-time) , {'x':(windowwidth/2)+230 , 'y':10} , CELLSIZE)
    if  ball_eaten >= 5 and ball_eaten < 10:
        level = 'Level: Beginner'
    elif ball_eaten >= 10 and ball_eaten <15:
        level = 'Level: Intermediate'
    elif ball_eaten >= 15 and ball_eaten <20:
        level = 'Level: Skilled'
    elif ball_eaten >=20:
        level = 'Level: Expert'
    print_msg('fonts/cs_regular.ttf' , BLACK , level , {'x':(windowwidth/2)-230 , 'y':10} , CELLSIZE)

if __name__ == '__main__':
    main()