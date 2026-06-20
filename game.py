import pygame
import numpy
import random
import keyboard
import time

#----------------------------------------------------------------------------------------------------------------------------------------
class POS:
    x = -1
    y = -1
class ATTRIBUTES:
    hp = 1
    hpMax = 1
    defense = 1
    strength = 1
    dexterity = 1
    intelligence = 1
class ITEM:
    id = 0
    heal = 0
    hp = 0
    strength = 0
    defense = 0
    dexterity = 0
    intelligence = 0
    cursed = False
class PLAYER:
    attPoints = 5
    nivel = 1
    gold = 0
    exp = 0
    nextExp = 2
    keyInput = 0
    clockSpeed = time.perf_counter()
    alive = True
    inventoryOpened = False
    fallen = False
    key = False
    firstAtt = True
    inventory = numpy.array([[ITEM() for _ in range(4)] for _ in range(3)])
    pos = POS()
    inventorySelection = POS()
    attributes = ATTRIBUTES
class MONSTER:
    id = 0
    alive = False
    key = False
    clockSpeed = time.perf_counter()
    pos = POS()
    attributes = ATTRIBUTES
class MAP:
    tiles = numpy.zeros((1000,1000))
    memory = numpy.zeros((1000,1000))
    floor = 0
    player = PLAYER
    items = numpy.array([POS() for _ in range(floor)])
    monsters = numpy.array([MONSTER() for _ in range(floor*2)])
class MENU:
    selection = 0
class GAME:
    attSelection = 0
    map = MAP
    menu = MENU
    play = False
    next = True
#----------------------------------------------------------------------------------------------------------------------------------------
def move_player(game = GAME):
    if(keyboard.is_pressed=="w"):
        game.map.player.pos.y-=1
    if(keyboard.is_pressed=="s"):
        game.map.player.pos.y+=1
    if(keyboard.is_pressed=="a"):
        game.map.player.pos.x-=1
    if(keyboard.is_pressed=="d"):
        game.map.player.pos.x+=1
#----------------------------------------------------------------------------------------------------------------------------------------
def simulate_vision(game = GAME(),y=0,x=0,i=0):
    if(i>=1):
        if(random.random<0.5):
            if(y<0):
                y-=1
            else:
                y+=1
        if(random.random<0.5):
            if(x<0):
                x-=1
            else:
                x+=1
    if(game.map.tiles[game.map.player.pos.y+y][game.map.player.pos.x+x]!=0):
        i+=1
        game.map.memory[game.map.player.pos.y+y][game.map.player.pos.x+x] = 1
        if(i<game.map.player.attributes.intelligence):
            simulate_vision(game,y,x,i)
    game.map.memory[game.map.player.pos.y+y][game.map.player.pos.x+x] = 1
    return 0
#----------------------------------------------------------------------------------------------------------------------------------------
def render_game(game = GAME):
    if(game.map.player.attributes.hp<0):
        game.map.player.attributes.hp = 0
    for y in range(-1,2,1):
        for x in range(-1,2,1):
            simulate_vision(game,y,x)
    for y in range(-10,10,1):
        for x in range(-10,10,1):
            if(game.map.tiles[game.map.player.pos.y+y][game.map.player.pos.x+x]==0):
                pygame.draw.rect(screen,"#545454",((x*50)+500,(y*50)+500,50,50))
            if(game.map.tiles[game.map.player.pos.y+y][game.map.player.pos.x+x]==1):
                pygame.draw.rect(screen,"#a2a2a2",((x*50)+500,(y*50)+500,50,50))
            if(game.map.tiles[game.map.player.pos.y+y][game.map.player.pos.x+x]==2):
                pygame.draw.rect(screen,"#ffffff",((x*50)+500,(y*50)+500,50,50))
            if(y==0 and x==0):
                pygame.draw.circle(screen,"#ffffff",[525,525],20)
#----------------------------------------------------------------------------------------------------------------------------------------
def create_map(game = GAME):
    if(game.next):
        game.map.player.firstAtt = True
        game.map.player.attPoints += 1
    game.next = False
    game.map.player.key = False
    game.map.player.pos.y = 500
    game.map.player.pos.x = 500
    mapY = game.map.player.pos.y
    mapX = game.map.player.pos.x
    i = 0
    while(True):
        tamY = random.randint((game.map.floor+2),(game.map.floor+2)*2)
        tamX = random.randint((game.map.floor+2),(game.map.floor+2)*2)
        for y in range(0-tamY,tamY,1):
            for x in range(0-tamX,tamX,1):
                if(mapY+y>=0 and mapY+y<999 and mapX+x>=0 and mapX+x<999):
                    if(y==-tamY or y==tamY-1 or x==-tamX or x==tamX-1):
                        game.map.tiles[mapY+y][mapX+x] = 1 # FREEBLOCK
        if(i>=game.map.floor*2):
            if(random.random()<=0.5):
                game.map.tiles[mapY][mapX] = 2 # STAIR
                break
        direction = random.randint(0,3)
        while(True):
            if(direction==0):
                mapY-=1
            if(direction==1):
                mapY+=1
            if(direction==2):
                mapX-=1
            if(direction==3):
                mapX+=1
            if(mapY>=1 and mapY<999 and mapX>=1 and mapX<999):
                game.map.tiles[mapY][mapX] = 1
            else:
                direction = random.randint(0,3)
            if(random.random()<=0.25):
                direction = direction = random.randint(0,3)
            if(random.random()<=0.01):
                break
        if(i>=game.map.floor*2):
            if(random.random()<=0.5):
                game.map.tiles[mapY][mapX] = 2
                break
        i+=1
#----------------------------------------------------------------------------------------------------------------------------------------
def menu(game = GAME):
    global running
    screen.fill("black")
    font_size = 30
    font = pygame.font.SysFont('Comic Sans MS', font_size)
    if game.menu.selection==0:
        play_text = font.render('> PLAY', True, (255, 245, 150))
    else:
        play_text = font.render('  PLAY', True, (255, 255, 255))
    if game.menu.selection==1:
        exit_text = font.render('> EXIT', True, (255, 245, 150))
    else:
        exit_text = font.render('  EXIT', True, (255, 255, 255))

    screen.blit(play_text, ((500-font_size*2)+random.randint(-1,1),(500-font_size)+random.randint(-1,1)))
    screen.blit(exit_text, ((500-font_size*2)+random.randint(-1,1),(500+font_size)+random.randint(-1,1)))
    if(keyboard.is_pressed('w')):
        game.menu.selection = 0
    if(keyboard.is_pressed('s')):
        game.menu.selection = 1
    if(keyboard.is_pressed('enter')):
        if game.menu.selection == 1:
            running = False
        if game.menu.selection == 0:
            game.play = True
#----------------------------------------------------------------------------------------------------------------------------------------
def play(game = GAME):
    screen.fill("black")
    if(game.next):
        create_map(game)
        game.next = False
    render_game(game)
    move_player(game)

#----------------------------------------------------------------------------------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
running = True

game = GAME()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if game.play == False:
        menu(game)
    else:
        play(game)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()