import pygame
import Objects_Game
import random

Width_Window = 700
Height_Window = 700

pygame.init()
gameDisplay = pygame.display.set_mode((Width_Window, Height_Window))
pygame.display.update()

player_image = pygame.image.load("images/player.jpg")
enemy_image = pygame.image.load("images/enemy.jpg")
box_image = pygame.image.load("images/box.jpg")

pygame.mixer.music.load("sound/now-or-never.wav")
pygame.mixer.music.play()
Map_Game = []
list_box = pygame.sprite.Group()

for i in range(10):
    Map_Game.append([])
    for j in range(10):
        Map_Game[i].append(False)


def Set_Position_To_All_Box():
    i = 0
    while i < 10:
        j = 0
        while j < 5:
            column = random.randint(0, 9)
            if Map_Game[i][column] is not True:
                Map_Game[i][column] = True
                j += 1
                current_box = Objects_Game.Box(box_image, i * 70, column * 70)
                list_box.add(current_box)
        i += 1


def Get_Position_In_Vacant_Place():
    sprite_is_set = False
    while sprite_is_set is not True:
        row = random.randint(0, 9)
        column = random.randint(0, 9)
        if Map_Game[row][column] is not True:
            sprite_is_set = True
            coord_sprite = [row * 70, column * 70]
            return coord_sprite


tanks = pygame.sprite.Group()


def Create_Pack_Enemies():
    i = 7
    while i > 0:
        i -= 1
        Coords_enemy = Get_Position_In_Vacant_Place()
        enemy = Objects_Game.Enemy_Tank(enemy_image, Coords_enemy[0], Coords_enemy[1], 5, "RIGHT")
        tanks.add(enemy)


def Check_Collision_Tanks():
    for tank1 in tanks:
        for tank2 in tanks:
            if tank1.rect != tank2.rect and tank1.rect.colliderect(tank2):
                tank1.kill()


def Check_Collision_Bullet():
    for tank in tanks:
        for bull in list_bullets:
            if tank.rect.colliderect(bull):
                bull.kill()
                tank.kill()


f1 = pygame.font.Font(None, 30)

yellow = (255, 255, 0)
blue = (0, 0, 255)


def Show_Message_over():
    fontObj = pygame.font.Font('freesansbold.ttf', 50)
    textSurfaceObj = fontObj.render('You lose!', True, blue, white)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (Width_Window/2, Height_Window/2)
    gameDisplay.blit(textSurfaceObj, textRectObj)


def Show_Message_win():
    fontObj = pygame.font.Font('freesansbold.ttf', 50)
    textSurfaceObj = fontObj.render('You win!', True, blue, white)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (Width_Window/2, Height_Window/2)
    gameDisplay.blit(textSurfaceObj, textRectObj)


def Check_Win_Player():
    end_game = False
    for tank in tanks:
        if isinstance(tank, Objects_Game.Player_Tank) and len(tanks) == 1:
            end_game = True
    return end_game


def Check_Lose_Player():
    end_game = False
    player_destroy = True
    for tank in tanks:
        if isinstance(tank, Objects_Game.Player_Tank):
            player_destroy = False
    if player_destroy is True:
        end_game = True
    return end_game


white = (255, 255, 255)
Set_Position_To_All_Box()
Coords = Get_Position_In_Vacant_Place()
player = Objects_Game.Player_Tank(player_image, Coords[0], Coords[1], 5, "RIGHT")
list_bullets = pygame.sprite.Group()
gameExit = False
game_win = False
game_over = False
Create_Pack_Enemies()
tanks.add(player)
while not gameExit:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
    if game_over is True:
        Show_Message_over()
    if game_win is True:
        Show_Message_win()
    if game_over is not True and game_win is not True:
        pygame.time.delay(20)
        gameDisplay.fill(white)
        game_win = Check_Win_Player()
        game_over = Check_Lose_Player()
        for bullet in list_bullets:
            bullet.update(list_box)
            gameDisplay.blit(bullet.image, (bullet.rect.x, bullet.rect.y))
        Check_Collision_Bullet()
        for box in list_box:
            gameDisplay.blit(box.image, (box.rect.x, box.rect.y))
        for tank in tanks:
            gameDisplay.blit(tank.image, (tank.rect.x, tank.rect.y))
            tank.update(list_box, list_bullets)
        Check_Collision_Tanks()
