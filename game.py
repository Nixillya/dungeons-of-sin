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
    player = PLAYER()
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
def move_player(game = GAME()):
    if(time.perf_counter()-game.map.player.clockSpeed>0.1/game.map.player.attributes.dexterity):
        clock = False
        target = POS()
        target.y = 0
        target.x = 0
        forbiddenBlcoks = [0]
        if(keyboard.is_pressed('w')):
            target.y-=1
            clock = True
        if(keyboard.is_pressed('s')):
            target.y+=1
            clock = True
        if(keyboard.is_pressed('a')):
            target.x-=1
            clock = True
        if(keyboard.is_pressed('d')):
            target.x+=1
            clock = True
        if(keyboard.is_pressed('enter')):
            if(game.map.tiles[game.map.player.pos.y][game.map.player.pos.x]==2):
                game.next = True
        if(keyboard.is_pressed('esc')):
            game.play = False
        if(clock):
            game.map.player.clockSpeed = time.perf_counter()
        if((target.y!=0 and target.x==0) or (target.y==0 and target.x!=0)):
            game.map.player.pos.y+=target.y
            game.map.player.pos.x+=target.x
            if(game.map.tiles[game.map.player.pos.y][game.map.player.pos.x] in forbiddenBlcoks):
                game.map.player.pos.y-=target.y
                game.map.player.pos.x-=target.x
#----------------------------------------------------------------------------------------------------------------------------------------
def simulate_vision(game = GAME(),y=0,x=0,i=0):
    if(i>=1):
        if(random.random()<0.5):
            if(y<0):
                y-=1
            else:
                y+=1
        if(random.random()<0.5):
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
            Y = y*50+500
            X = x*50+500
            if(game.map.memory[game.map.player.pos.y+y][game.map.player.pos.x+x]==1):
                if(game.map.tiles[game.map.player.pos.y+y][game.map.player.pos.x+x]==0):
                    pygame.draw.rect(screen,"#545454",(X,Y,50,50))
                if(game.map.tiles[game.map.player.pos.y+y][game.map.player.pos.x+x]==1):
                    pygame.draw.rect(screen,"#a2a2a2",(X,Y,50,50))
                if(game.map.tiles[game.map.player.pos.y+y][game.map.player.pos.x+x]==2):
                    if(game.map.player.key):
                        pygame.draw.rect(screen,"#ffffff",(X,Y,50,50))
                    pygame.draw.rect(screen,"#363636",(X+5,Y+5,40,40))
                for monster in game.map.monsters:
                    if(monster.y==game.map.player.pos.y+y and monster.x==game.map.player.pos.x+x):
                        pygame.draw.circle(screen,"#ba0000",[X+25,Y+25],20)
                if(y==0 and x==0):
                    pygame.draw.circle(screen,"#ffffff",[X+25,Y+25],20)
#----------------------------------------------------------------------------------------------------------------------------------------
def create_map(game = GAME):
    screen.fill("black")
    font = pygame.font.SysFont('Comic Sans MS', 60)
    loading_text = font.render('Loading...', True, (255, 255, 255))
    screen.blit(loading_text, (500-loading_text.get_size()[0]/2,500-loading_text.get_size()[1]/2))
    pygame.display.flip()

    game.map.player.key = False
    mapY = 500
    mapX = 500
    i = 0
    for y in range(1000):
        for x in range(1000):
            game.map.tiles[y][x] = 0
            game.map.memory[y][x] = 0
    while(True):
        tamY = random.randint(1,game.map.floor)
        tamX = random.randint(1,game.map.floor)
        if(tamY>10):
            tamY = random.randint(1,10)
        if(tamX>10):
            tamX = random.randint(1,10)
        for y in range(0-tamY,tamY,1):
            for x in range(0-tamX,tamX,1):
                game.map.tiles[mapY+y][mapX+x] = 1 # FREEBLOCK
        if(i>=game.map.floor):
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
                direction = random.randint(0,3)
            if(random.randint(0,game.map.floor)==0):
                break
        if(i>=game.map.floor):
            if(random.random()<=0.5):
                game.map.tiles[mapY][mapX] = 2
                break
        i+=1
    while(True):
        game.map.player.pos.y = random.randint(0,999)
        game.map.player.pos.x = random.randint(0,999)
        if(game.map.tiles[game.map.player.pos.y][game.map.player.pos.x]==1):
            break
    for monster in game.map.monsters:
        monster.pos.y = -1
        monster.pos.x = -1
    for monster in game.map.monsters:
        while(True):
            monster.pos.y = random.randint(0,999)
            monster.pos.x = random.randint(0,999)
            if(game.map.tiles[monster.pos.y][monster.pos.x]!=1):
                monster.pos.y = -1
                monster.pos.x = -1
            else:
                break
    for item in game.map.items:
        item.pos.y = -1
        item.pos.x = -1
    for monster in game.map.items:
        item.pos.y = random.randint(0,999)
        item.pos.x = random.randint(0,999)
        if(game.map.tiles[item.pos.y][item.pos.x]!=1):
            item.pos.y = -1
            item.pos.x = -1
#----------------------------------------------------------------------------------------------------------------------------------------
def menu(game = GAME):
    global running
    screen.fill("black")
    font = pygame.font.SysFont('Comic Sans MS', 30)
    if game.menu.selection==0:
        play_text = font.render('> PLAY', True, (255, 245, 150))
    else:
        play_text = font.render('  PLAY', True, (255, 255, 255))
    if game.menu.selection==1:
        exit_text = font.render('> EXIT', True, (255, 245, 150))
    else:
        exit_text = font.render('  EXIT', True, (255, 255, 255))

    screen.blit(play_text, ((500-play_text.get_size()[0]/2)+random.randint(-1,1),(485-play_text.get_size()[1]/2)+random.randint(-1,1)))
    screen.blit(exit_text, ((500-exit_text.get_size()[0]/2)+random.randint(-1,1),(515-exit_text.get_size()[1]/2)+random.randint(-1,1)))
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
        game.map.floor+=1
        game.map.player.firstAtt = True
        game.map.player.attPoints += 1
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
        game.map = MAP()
        menu(game)
    else:
        play(game)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()