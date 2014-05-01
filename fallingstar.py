import pygame
from livewires import games, color

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

games.init(screen_width = SCREEN_WIDTH, screen_height = SCREEN_HEIGHT, fps = 50)

class Player(games.Sprite):
    """ This class represents the player sprite, Pixel. """

    # Attributes
    right_walk = games.load_image("pixel_right1.png")
    left_walk = games.load_image("pixel_left1.png")
    gravity = 0.3
    moving = False
    jumping = False

    # speed attributes
    change_x = 0
    change_y = 0

    # list of platforms to move
    platform_list = []

    level = 1
    
    def __init__(self, platform_list):
        # call parent constructor
        super(Player, self).__init__(image = Player.right_walk, left = 155,
                                     bottom = games.screen.height - 43)

        # add score text
        self.score = games.Text(value = 0, size = 25,
                                color = color.white,
                                top = 5, right = games.screen.width - 10)
        games.screen.add(self)
        games.screen.add(self.score)
        self.platform_list = platform_list

    def update(self):
        """ Move the player. """

        # change image direction
        if self.change_x > 0:
            self.image = Player.right_walk
        if self.change_x < 0:
            self.image = Player.left_walk

        # check to see if we're standing on a platform
        self.y += 2
        platform_hit_list = self.overlapping_sprites
        self.y -= 2

        # we're not jumping if we're on the ground
        if self.bottom >= games.screen.height:
            self.bottom = games.screen.height
            self.jumping = False

        # we're not jumping if we're on a platform
        if len(platform_hit_list) > 0:
            self.jumping = False

        # not jumping and the jump key is pressed...
        if self.jumping == False and games.keyboard.is_pressed(games.K_UP):
            # when standing on platforms
            if len(platform_hit_list) > 0:
                self.change_y = -10
                self.jumping = True
            # when standing on ground
            else:
                self.change_y = -10
                self.jumping = True


        # if we're jumping
        if self.jumping:
            # if we won't jump out of bounds...
            if self.y + self.change_y < games.screen.height:
                self.y += self.change_y
                self.change_y += self.gravity
            # make sure we stay on the ground, stop jumping
            else:
                self.bottom = games.screen.height
                self.jumping = False

        # for every sprite above and below us...
        for block in self.overlapping_sprites:
            if self.change_y > 0:
                if isinstance(block, Gem):
                    self.overlapping_sprites.remove(block)
                    self.platform_list.remove(block)
                    block.destroy()
                    self.score.value += 10
                    self.score.right = games.screen.width - 10
                elif isinstance(block, Sign):
                    self.update_level()
                else:
                    self.bottom = block.top
                    self.jumping = False
            elif self.change_y < 0:
                if isinstance(block, Gem):
                    self.overlapping_sprites.remove(block)
                    self.platform_list.remove(block)
                    block.destroy()
                    self.score.value += 10
                    self.score.right = games.screen.width - 10
                elif isinstance(block, Sign):
                    self.update_level()
                else:
                    self.top = block.bottom
                    self.jumping = False
            # stop jumping
            self.change_y = 0

        if self.moving == False and games.keyboard.is_pressed(games.K_LEFT):
            self.moving = True
            self.change_x = -8
        elif self.moving == False and games.keyboard.is_pressed(games.K_RIGHT):
            self.moving = True
            self.change_x = 8
        else:
            self.moving = False

        if self.moving:
            self.x += self.change_x
            self.jumping = True
            if self.x >= 400:
                diff = 400 - self.x
                self.x = 400
                for platform in self.platform_list:
                    platform.shift_world(diff)
            if self.x <= 120:
                diff = 120 - self.x
                self.x = 120
                for platform in self.platform_list:
                    platform.shift_world(diff)

        
        for block in self.overlapping_sprites:
            # if we're moving right
            if self.change_x > 0:
                if isinstance(block, Gem):
                    self.overlapping_sprites.remove(block)
                    self.platform_list.remove(block)
                    block.destroy()
                    self.score.value += 10
                    self.score.right = games.screen.width - 10
                elif isinstance(block, Sign):
                    self.update_level()
                else:
                    self.right = block.left
            # if we're moving left
            if self.change_x < 0:
                if isinstance(block, Gem):
                    self.overlapping_sprites.remove(block)
                    self.platform_list.remove(block)
                    block.destroy()
                    self.score.value += 10
                    self.score.right = games.screen.width - 10
                elif isinstance(block, Sign):
                    self.update_level()
                else:
                    self.left = block.right


        # make sure we stay bounded in screen
        if self.left < 0:
            self.left = 0

        if self.right > games.screen.width:
            self.right = games.screen.width

        if self.top <= 0:
            self.top = 0

        if self.bottom >= games.screen.height:
            self.bottom = games.screen.height

        games.screen.remove(self.score)

        games.screen.add(self.score)

    def update_level(self):
        games.screen.remove(Level_01.display)
        if self.score.value >= 80:
            won_message = games.Message(value = "You won!",
                                        size = 100,
                                        color = color.white,
                                        x = games.screen.width/2,
                                        y = games.screen.height/2,
                                        lifetime = 125,
                                        after_death = games.screen.quit)
            games.screen.add(won_message)
        else:
            for block in self.platform_list:
                block.destroy()
            self.left = 155
            self.bottom = games.screen.height - 43
            level_02 = Level_02()
            self.platform_list = level_02.get_platforms()

              
class Platform(games.Sprite):
    """ Platform the player can jump on. """

    image = games.load_image("platform.png")
    world_shift = 0
    def __init__(self, x, y):
        super(Platform, self).__init__(image = Platform.image,
                                       x = x, y = y)

    def shift_world(self, diff):
        self.x += diff
        self.world_shift -= diff

    def is_collectible(self):
        return 1

class Ground(games.Sprite):
    """ Platform the player can jump on. """

    image = games.load_image("ground.png")
    def __init__(self, x, y):
        super(Ground, self).__init__(image = Ground.image,
                                       x = x, y = y)

    def shift_world(self, diff):
        self.x += diff

    def is_collectible(self):
        return 1

class Wall(games.Sprite):
    """ Platform the player can jump on. """

    image = games.load_image("stonewall.png")
    def __init__(self, x, y):
        super(Wall, self).__init__(image = Wall.image,
                                       x = x, y = y)

    def shift_world(self, diff):
        self.x += diff

    def is_collectible(self):
        return 1
    
class Door(games.Sprite):
    """ Platform the player can jump on. """

    image = games.load_image("doorway.png")
    def __init__(self, x, y):
        super(Door, self).__init__(image = Door.image,
                                       x = x, y = y)

    def shift_world(self, diff):
        self.x += diff

    def is_collectible(self):
        return 1

class Gem(games.Sprite):

    image = games.load_image("gem.png")
    def __init__(self, x, y):
        super(Gem, self).__init__(image = Gem.image,
                                  x = x, y = y)
    def shift_world(self, diff):
        self.x += diff

    def is_collectible(self):
        return 0

class Sign(games.Sprite):

    image = games.load_image("exit.png")

    def __init__(self, x, y):
        super(Sign, self).__init__(image = Sign.image,
                                 x = x, y = y)

    def shift_world(self, diff):
        self.x += diff
    
class Level_01():

    display = games.Text(value = "Level 01", size = 25,
                         color = color.white,
                         top = 5, left = 10)

    platform_list = []
    level = [[440, 350],[740, 260],[1040, 260],[1320, 350]]
    def __init__(self):
        games.screen.add(self.display)
        floor = []
        left_wall = []
        i = -1
        while i < 800:
            floor.append([i, 468])
            i += 70
        i = 0
        while i < 480:
            left_wall.append([0, i])
            left_wall.append([106, i])
            left_wall.append([1750, i])
            left_wall.append([1820, i])
            left_wall.append([1890, i])
            left_wall.append([1960, i])
            i += 70
            
        for wall in left_wall:
            block = Wall(wall[0], wall[1])
            if wall[0] == 0:
                block.left = 0
            self.platform_list.append(block)
            games.screen.add(block)
            
        for ground in floor:
            block = Ground(ground[0], ground[1])
            block.bottom = games.screen.height
            games.screen.add(block)

        for build in self.level:
            block = Platform(build[0], build[1])
            self.platform_list.append(block)
            games.screen.add(block)

        block = Door(1780, 383)
        self.platform_list.append(block)
        games.screen.add(block)

        block = Sign(1650, 400)
        block.bottom = games.screen.height - 40
        self.platform_list.append(block)
        games.screen.add(block)

        block = Gem(440, 280)
        self.platform_list.append(block)
        games.screen.add(block)

        block = Gem(740, 190)
        self.platform_list.append(block)
        games.screen.add(block)

        block = Gem(1040, 190)
        self.platform_list.append(block)
        games.screen.add(block)

        block = Gem(1320, 280)
        self.platform_list.append(block)
        games.screen.add(block)

        games.screen.add(self.display)


    def get_platforms(self):
        return self.platform_list

    def get_level(self):
        return self.level

class Level_02():

    display = games.Text(value = "Level 02", size = 25,
                         color = color.white,
                         top = 5, left = 10)

    platform_list = []
    level = [[440, 350],[740, 350],[1040, 260],[1320, 260]]
    def __init__(self):
        games.screen.add(self.display)
        floor = []
        left_wall = []
        i = -1
        while i < 800:
            floor.append([i, 468])
            i += 70
        i = 0
        while i < 480:
            left_wall.append([0, i])
            left_wall.append([106, i])
            left_wall.append([1750, i])
            left_wall.append([1820, i])
            left_wall.append([1890, i])
            left_wall.append([1960, i])
            i += 70
            
        for wall in left_wall:
            block = Wall(wall[0], wall[1])
            if wall[0] == 0:
                block.left = 0
            self.platform_list.append(block)
            games.screen.add(block)
            
        for ground in floor:
            block = Ground(ground[0], ground[1])
            block.bottom = games.screen.height
            games.screen.add(block)

        for build in self.level:
            block = Platform(build[0], build[1])
            self.platform_list.append(block)
            games.screen.add(block)

        block = Door(1780, 383)
        self.platform_list.append(block)
        games.screen.add(block)

        block = Sign(1650, 400)
        block.bottom = games.screen.height - 40
        self.platform_list.append(block)
        games.screen.add(block)

        block = Gem(440, 280)
        self.platform_list.append(block)
        games.screen.add(block)

        block = Gem(740, 280)
        self.platform_list.append(block)
        games.screen.add(block)

        block = Gem(1040, 190)
        self.platform_list.append(block)
        games.screen.add(block)

        block = Gem(1320, 190)
        self.platform_list.append(block)
        games.screen.add(block)

        games.screen.add(self.display)


    def get_platforms(self):
        return self.platform_list

    def get_level(self):
        return self.level

            
def main():
    """ Play the game. """
    wall_image = games.load_image("starrynight.png", transparent = False)
    games.screen.background = wall_image

    level_01 = Level_01()

    the_player = Player(level_01.get_platforms())

    games.mouse.is_visible = False

    games.screen.event_grab = True
    games.screen.mainloop()

# start it up!
main()





                
