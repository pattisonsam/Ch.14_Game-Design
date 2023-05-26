'''
SPRITE GAME
-----------
Here you will start the beginning of a game that you will be able to update as we
learn more in upcoming chapters. Below are some ideas that you could include:

1.) Find some new sprite images.
2.) Move the player sprite with arrow keys rather than the mouse. Don't let it move off the screen.
3.) Move the other sprites in some way like moving down the screen and then re-spawning above the window.
4.) Use sounds when a sprite is killed or the player hits the sidewall.
5.) See if you can reset the game after 30 seconds. Remember the on_update() method runs every 1/60th of a second.
6.) Try some other creative ideas to make your game awesome. Perhaps collecting good sprites while avoiding bad sprites.
7.) Keep score and use multiple levels. How do you keep track of an all time high score?
8.) Make a two player game.

'''


import random
import arcade

# --- Constants ---
hook_scale = 0.1
shadow_scale = 0.05
SW = 800
SH = 600
click = 0
fish = 0
shadow_count = 20
s_speed = 10
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/hook.png", hook_scale)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.left < 0:
            self.left = 0
        if self.right > SW:
            self.right = SW
        if self.top > SH:
            self.top = SH
        if self.bottom < 0:
            self.bottom = 0

class Shadow(arcade.Sprite):
    def __init__(self):
        super().__init__("images/shadow.png", shadow_scale)
        self.w = int(self.width)
        self.h = int(self.height)


    def update(self):
        move = random.randint(1,100)
        if move ==1:
            swim = random.randint(1,100)
            if swim <= 25:
                for i in range(random.randint(10,20)):
                    self.center_x += s_speed
            elif swim > 25 and swim <= 50:
                for i in range(random.randint(10,20)):
                    self.center_y += s_speed
            elif swim > 50 and swim <= 75:
                for i in range(random.randint(10,20)):
                    self.center_x -= s_speed
            else:
                for i in range(random.randint(10,20)):
                    self.center_y -= s_speed
        if self.left < 0:
            self.left = 0
        if self.right > SW:
            self.right = SW
        if self.top > SH:
            self.top = SH
        if self.bottom < 0:
            self.bottom = 0

# ------MyGame Class--------------
class MyGame(arcade.Window):

    def __init__(self, w, h, title):
        super().__init__(w, h, title)
        arcade.set_background_color(arcade.color.SAP_GREEN)
        self.set_mouse_visible(False)
        self.background = None

    def reset(self):
        self.player_list = arcade.SpriteList()
        self.shadow_list = arcade.SpriteList()
        self.score = 0
        self.hook = Player()
        self.hook.center_x = SW / 2
        self.hook.center_y = SH / 2
        self.player_list.append(self.hook)
        self.background = arcade.load_texture("Images/water.jpg")

        for i in range(shadow_count):
            shadow = Shadow()
            shadow.center_x = random.randint(shadow.w, SW - shadow.w)
            shadow.center_y = random.randint(shadow.h, SH - shadow.h)
            self.shadow_list.append(shadow)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SW, SH, self.background)
        self.shadow_list.draw()
        self.player_list.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output, SW - 80, SH - 20, arcade.color.BLACK, 14)



    def on_update(self, dt):
        self.player_list.update()
        self.shadow_list.update()

    def on_mouse_motion(self, x, y, dx, dy):
        self.hook.center_x = x
        self.hook.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        Shadow_hooked = arcade.check_for_collision_with_list(self.hook, self.shadow_list)
        if len(Shadow_hooked) > 0:
            for fish in Shadow_hooked:
                fish.kill()
                self.score += random.randint(1,10)






# -----Main Function-------
def main():
    window = MyGame(SW, SH, "Shark Attack")
    window.reset()
    arcade.run()

# ------Run Main Function-----
if __name__ == "__main__":
    main()