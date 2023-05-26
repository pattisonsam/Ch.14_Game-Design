# Sign your name: Samuel Pattison

# You will use the starting code below and build the program "BB8 Attack" as you go through Chapter 15.


import random
import arcade

# --- Constants ---
BB8_scale = 0.3
trooper_scale = 0.1
bullet_scale = 1
bullet_speed = -10
trooper_count = 10
SW = 800
SH = 600
SP = 4
t_speed = 2

t_score = 5
b_score = 1
explosion_texture_count = 50


class Explosion(arcade.Sprite):
    def __init__(self, texture_list):
        super().__init__("images/explosions/explosion0000.png")
        self.current_texture = 0
        self.textures = texture_list
        self.explosion = arcade.load_sound("sounds/explosion.wav")

    def update(self):
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.kill()


# ------ Player Class ---------
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("images/bb8.png", BB8_scale)
        self.laser_sound = arcade.load_sound("sounds/laser.wav")
        self.explosion = arcade.load_sound("sounds/explosion.wav")

    def update(self):
        self.center_y += self.change_y
        self.center_x += self.change_x
        if self.left < 0:
            self.left = 0
            arcade.play_sound(self.laser_sound)
        elif self.right > SW:
            self.right = SW
            arcade.play_sound(self.laser_sound)
        if self.bottom < 0:
            self.bottom = 0
            arcade.play_sound(self.laser_sound)
        elif self.top > SH:
            self.top = SH
            arcade.play_sound(self.laser_sound)


# ------ Trooper Class ---------
class Trooper(arcade.Sprite):
    def __init__(self):
        super().__init__("images/stormtrooper.png", trooper_scale)
        self.w = int(self.width)
        self.h = int(self.height)
        self.explosion = arcade.load_sound("sounds/explosion.wav")

    def update(self):
        self.center_y -= t_speed
        if self.top < 0:
            self.center_x = random.randrange(self.w, SW - self.w)
            self.center_y = random.randrange(SW + self.h, SH * 2)


class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("images/bullet.png", bullet_scale)
        self.explosion = arcade.load_sound("sounds/explosion.wav")

    def update(self):
        self.center_y -= bullet_speed
        if self.bottom > SH:
            self.kill()


class Enemy_Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("images/rbullet.png", bullet_scale)

    def update(self):
        self.center_y += bullet_speed
        if self.center_y > SH:
            self.kill()
        if self.top < 0:
            self.kill()


# ------MyGame Class--------------
class MyGame(arcade.Window):

    def __init__(self, SW, SH, title):
        super().__init__(SW, SH, title)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.set_mouse_visible(False)
        self.explosion_texture_list = []
        for i in range(explosion_texture_count):
            texture_name = f"Images/explosions/explosion{i:04}.png"
            self.explosion_texture_list.append(arcade.load_texture(texture_name))

    def reset(self):
        # Creature Sprite Lists
        self.player_list = arcade.SpriteList()
        self.trooper_list = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.ebullets = arcade.SpriteList()
        self.explosions = arcade.SpriteList()

        # set score
        self.score = 0

        # create the player
        self.BB8 = Player()
        self.BB8.center_x = SW / 2
        self.BB8.center_y = 30
        self.player_list.append(self.BB8)

        # create the Troopers
        for i in range(trooper_count):
            trooper = Trooper()
            trooper.center_x = random.randint(trooper.w, SW - trooper.w)
            trooper.center_y = random.randint(trooper.h, SH - trooper.h)
            self.trooper_list.append(trooper)

    def on_draw(self):
        arcade.start_render()
        self.trooper_list.draw()
        self.player_list.draw()
        self.bullets.draw()
        self.ebullets.draw()
        self.explosions.draw()

        # self.score = 0
        self.gameover = False

        output = f"Score: {self.score}"
        arcade.draw_text(output, SW - 80, SH - 20, arcade.color.DARK_RED, 14)

        # Draw the gameover screen
        if self.gameover == True:
            arcade.draw_rectangle_filled(SW / 2, SH / 2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Game Over: Press P to Play Again", SW / 2, SH / 2, arcade.color.NEON_GREEN, 14,
                             anchor_x="center", anchor_y="center")
            arcade.draw_text(f"High Score: {self.score}", SW / 2, SH / 2 + 30, arcade.color.NEON_GREEN, 14,
                             anchor_x="center", anchor_y="center")

    def on_update(self, dt):
        self.trooper_list.update()
        self.player_list.update()
        self.bullets.update()
        self.ebullets.update()
        self.explosions.update()

        if len(self.trooper_list) == 0:
            self.gameover = True

        BB8_hit = arcade.check_for_collision_with_list(self.BB8, self.trooper_list)
        if len(BB8_hit) > 0 and not self.gameover:
            self.BB8.kill()
            arcade.play_sound(self.BB8.explosion)
            self.gameover = True

        # randomly drop bombs
        for trooper in self.trooper_list:
            if random.randrange(1000) == 1:
                ebullet = Enemy_Bullet()
                ebullet.angle = -90
                ebullet.center_x = trooper.center_x
                ebullet.top = trooper.center_y
                self.ebullets.append(ebullet)

        # detect if BB8 gets nuked
        BB8_bombed = arcade.check_for_collision_with_list(self.BB8, self.ebullets)
        if len(BB8_bombed) > 0 and not self.gameover:
            self.BB8.kill()
            arcade.play_sound(self.BB8.explosion)
            self.gameover = True

        for bullet in self.bullets:
            hit_list = arcade.check_for_collision_with_list(bullet, self.trooper_list)
            if len(hit_list) > 0:
                arcade.play_sound(bullet.explosion)
                bullet.kill()
                explosion = Explosion(self.explosion_texture_list)
                explosion.center_x = hit_list[0].center_x
                explosion.center_y = hit_list[0].center_y
                self.explosions.append(explosion)

            for trooper in hit_list:
                trooper.kill()
                self.score += t_score
            if len(self.trooper_list) == 0:
                self.reset()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.BB8.change_x = -SP
        if key == arcade.key.D:
            self.BB8.change_x = SP
        if key == arcade.key.P:
            self.reset()
        if key == arcade.key.SPACE and not self.gameover:
            self.bullet = Bullet()
            self.bullet.center_x = self.BB8.center_x
            self.bullet.center_y = self.BB8.center_y
            self.bullet.bottom = self.BB8.top
            self.bullet.angle = 90
            self.bullets.append(self.bullet)
            self.score -= b_score
            arcade.play_sound(self.BB8.laser_sound)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A or arcade.key.D:
            self.BB8.change_x = 0


# -----Main Function--------
def main():
    window = MyGame(SW, SH, "BB8 Attack")
    window.reset()
    arcade.run()


# ------Run Main Function-----
if __name__ == "__main__":
    main()