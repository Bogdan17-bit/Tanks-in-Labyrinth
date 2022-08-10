import pygame
import random


class Box(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.y = y
        self.rect.x = x


class Tank(pygame.sprite.Sprite):
    previous_x = 0
    previous_y = 0

    def __init__(self, image, coord_x, coord_y, speed, current_direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.x = coord_x
        self.y = coord_y
        self.speed = speed
        self.current_direction = current_direction
        self.default_image = image

    def Rotate(self, angle):
        loc = self.image.get_rect().center
        self.image = pygame.transform.rotate(self.image, angle)
        self.image.get_rect().center = loc

    def Set_New_Direction(self, new_direction):
        if new_direction == "LEFT":
            self.Rotate(-180)
        elif new_direction == "BOTTOM":
            self.Rotate(-90)
        elif new_direction == "TOP":
            self.Rotate(90)

    def Set_Value_Previous_Position(self):
        self.previous_x = self.rect.x
        self.previous_y = self.rect.y

    def Back_to_Previous_Position(self):
        self.x = self.previous_x
        self.y = self.previous_y
        self.rect.x = self.previous_x
        self.rect.y = self.previous_y

    def Move_Right(self):
        if self.x < 640:
            self.image = self.default_image
            self.x += self.speed
            self.current_direction = "RIGHT"
            self.Set_Value_Previous_Position()

    def Move_Left(self):
        if self.x > 5:
            self.x -= self.speed
            self.image = self.default_image
            self.Set_New_Direction("LEFT")
            self.current_direction = "LEFT"
            self.Set_Value_Previous_Position()

    def Move_Top(self):
        if self.y > 5:
            self.y -= self.speed
            self.image = self.default_image
            self.Set_New_Direction("TOP")
            self.current_direction = "TOP"
            self.Set_Value_Previous_Position()

    def Move_Bottom(self):
        if self.y < 630:
            self.y += self.speed
            self.image = self.default_image
            self.Set_New_Direction("BOTTOM")
            self.current_direction = "BOTTOM"
            self.Set_Value_Previous_Position()

    def Refresh_Rect_Coord(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def Check_Collision_With_Box(self, list_boxes):
        self.Refresh_Rect_Coord()
        for box in list_boxes:
            if self.rect.colliderect(box):
                self.Back_to_Previous_Position()


class Player_Tank(Tank):
    shoot_ready = 0

    def Control_Tank(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.Move_Right()
        elif keys[pygame.K_LEFT]:
            self.Move_Left()
        elif keys[pygame.K_UP]:
            self.Move_Top()
        elif keys[pygame.K_DOWN]:
            self.Move_Bottom()

    def update(self, list_boxes, list_bullets):
        self.Control_Tank()
        self.Shoot(list_bullets)
        self.Check_Collision_With_Box(list_boxes)

    def Shoot(self, list_bullets):
        if self.shoot_ready == 0:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if self.shoot_ready == 0:
                    if self.current_direction == "RIGHT":
                        bullet = Bullet(7, self.rect.x + 60, self.rect.y + 10, self.current_direction)
                        list_bullets.add(bullet)
                        self.shoot_ready = 40
                    elif self.current_direction == "LEFT":
                        bullet = Bullet(7, self.rect.x - 25, self.rect.y + 10, self.current_direction)
                        list_bullets.add(bullet)
                        self.shoot_ready = 40
                    elif self.current_direction == "TOP":
                        bullet = Bullet(7, self.rect.x + 10, self.rect.y - 25, self.current_direction)
                        list_bullets.add(bullet)
                        self.shoot_ready = 40
                    elif self.current_direction == "BOTTOM":
                        bullet = Bullet(7, self.rect.x + 10, self.rect.y + 60, self.current_direction)
                        list_bullets.add(bullet)
                        self.shoot_ready = 40
                else:
                    self.shoot_ready -= 1
        else:
            self.shoot_ready -= 1


class Enemy_Tank(Tank):
    shoot_ready = 50
    default_image = pygame.image.load("images/enemy.jpg")
    time = 0
    direction = 0

    def Random_Direction_and_Movement_Generate(self):
        self.time = random.randint(20, 40)
        self.direction = random.randint(1, 4)

    def update(self, list_box, list_bullets):
        self.Check_Collision_With_Box(list_box)
        if self.time > 0:
            if self.direction == 1:
                self.Move_Right()
            elif self.direction == 2:
                self.Move_Bottom()
            elif self.direction == 3:
                self.Move_Top()
            elif self.direction == 4:
                self.Move_Left()
            self.time -= 1
        else:
            self.Random_Direction_and_Movement_Generate()
        self.Shoot(list_bullets)

    def Shoot(self, list_bullets):
        self.Refresh_Rect_Coord()
        if self.shoot_ready == 0:
            if self.direction == 1:
                bullet = Bullet(7, self.rect.x + 60, self.rect.y + 10, self.current_direction)
                list_bullets.add(bullet)
                self.shoot_ready = 40
            elif self.direction == 2:
                bullet = Bullet(7, self.rect.x + 10, self.rect.y + 60, self.current_direction)
                list_bullets.add(bullet)
                self.shoot_ready = 40
            elif self.direction == 3:
                bullet = Bullet(7, self.rect.x + 10, self.rect.y - 60, self.current_direction)
                list_bullets.add(bullet)
                self.shoot_ready = 40
            elif self.direction == 4:
                bullet = Bullet(7, self.rect.x - 60, self.rect.y + 10, self.current_direction)
                list_bullets.add(bullet)
                self.shoot_ready = 40
        else:
            self.shoot_ready -= 1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, speed, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = pygame.image.load("images/bullet.jpg")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.direction = direction

    def Check_Collision_with_Box(self, list_box):
        for box in list_box:
            if self.rect.colliderect(box):
                self.kill()
                box.kill()
                break

    def update(self, list_box):
        self.Check_Collision_with_Box(list_box)
        if self.direction == "RIGHT":
            self.rect.x += self.speed
        elif self.direction == "LEFT":
            self.rect.x -= self.speed
        elif self.direction == "TOP":
            self.rect.y -= self.speed
        elif self.direction == "BOTTOM":
            self.rect.y += self.speed
        if self.rect.x > 640 or self.rect.x < 0 or self.rect.y > 640 or self.rect.y < 0:
            self.kill()