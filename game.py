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
    floor = 1
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
    next = False
#----------------------------------------------------------------------------------------------------------------------------------------
def create_map(game = GAME):
    if game.next:
        game.map.player.firstAtt = True
        game.map.player.attPoints += 1
    game.next = False
    game.map.player.key = False
    game.map.player.pos.y = 500
    game.map.player.pos.x = 500
    for y in range(1000):
        for x in range(1000):
            if y==0 or x==0 or y==999 or x==999:
                game.map.tiles[y,x] = 2
    mapY = game.map.player.pos.y
    mapX = game.map.player.pos.x
    i = 0
    while True:
        tamY = random.randint(2,5)
        tamX = random.randint(2,5)
        if game.map.floor==6:
            tamY = 25
            tamX = 25
    
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
    for x in range(0,1000,100):
        for y in range(0,1000,100):
            pygame.draw.rect(screen,"red",(x,y,100,100))

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