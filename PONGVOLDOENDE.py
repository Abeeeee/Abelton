# imports
import arcade
import time

 # define arcade window characteristics 
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = " Pong1.0"
WINDOW_BACKGROUND_COLOR = arcade.color.PINK


class Ball:
    def __init__(self, position_x, position_y, delta_x, delta_y, radius, color):
         # define Ball functions
        self.position_x = position_x
        self.position_y = position_y
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.radius = radius
        self.color = color 
 
    def draw(self):
         # define what variables to draw when function is invoked
        arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)

    def update(self, delta_time, rectangle_list):
         # calls the functions that must be performed  
         # Movement speed & direction of the ball
        self.position_y += self.delta_y * delta_time * 4.1 
        self.position_x += self.delta_x * delta_time * 5.09
    
         # bounce the ball of the screen edges
        if self.position_y <= self.radius:
            self.delta_y *= -1
            self.position_y = self.radius
        if self.position_y >= WINDOW_HEIGHT - self.radius:
            self.delta_y *= -1
            self.position_y = WINDOW_HEIGHT - self.radius

        for rectangle in rectangle_list:
             # check for collision between paddle & ball, if so, change the ball it's trajectory and make it move faster.
            if self.position_x + self.radius >= rectangle.position_x - (rectangle.rect_width / 2) and \
            self.position_x - self.radius <= rectangle.position_x + (rectangle.rect_width / 2) and \
            self.position_y + self.radius >= rectangle.position_y - (rectangle.rect_height / 2) and \
            self.position_y - self.radius <= rectangle.position_y + (rectangle.rect_height / 2):
                self.delta_x *= -1.08

class Paddle:
    def __init__(self, position_x, position_y, rect_width, rect_height, color):
         # define Paddle functions
        self.position_x = position_x
        self.position_y = position_y
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.color = color
        self.delta_position_y = 0
        self.movement_speed = 10
    
    def draw(self):
         # define what variables to draw when function is invoked
        arcade.draw_rectangle_filled(self.position_x, self.position_y, self.rect_width, self.rect_height, self.color)

    def update(self, delta_time):
         # add the movement to the position
        self.position_y += self.delta_position_y

         # stops pabble when trying to move out of screen
        if self.position_y >= WINDOW_HEIGHT -(self.rect_height/2):
            self.delta_position_y = 0
            self.position_y = WINDOW_HEIGHT - (self.rect_height/2)
        if self.position_y <= 0 + (self.rect_height/2):
            self.delta_position_y = 0
            self.position_y = 0 + (self.rect_height/2)


class MyGame(arcade.Window):
    """ An Arcade game. """

    def __init__(self, width, height, title):
        """ Constructor. """
        super().__init__(width, height, title)
        arcade.set_background_color(WINDOW_BACKGROUND_COLOR)

         # adds one ball with functions
        self.ball_list = []
        ball = Ball(WINDOW_HEIGHT/2, WINDOW_WIDTH/2, 50, 50, 20, arcade.color.LIME_GREEN)
        self.ball_list.append(ball)

         # adds two rectangles with separate functions
        self.rectangle_list = []
        self.rectangle_list.append(Paddle(30, (WINDOW_HEIGHT/2), 20, 100, arcade.color.LIME_GREEN))
        self.rectangle_list.append(Paddle(WINDOW_WIDTH-30, (WINDOW_HEIGHT/2), 20, 100, arcade.color.LIME_GREEN))

         # define the scores
        self.left_score = 0
        self.right_score = 0

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
         # if ball is in list, draw the left score, a devider, and then the right score
        for ball in self.ball_list:
            ball.draw()
            arcade.draw_text("%(left_score)s" %{"left_score":self.left_score}, WINDOW_WIDTH / 2 - 20, WINDOW_HEIGHT - 40, arcade.color.LIME_GREEN,30)
            arcade.draw_text("%(right_score)s" %{"right_score":self.right_score}, WINDOW_WIDTH / 2 + 20, WINDOW_HEIGHT - 40, arcade.color.LIME_GREEN,30)
            arcade.draw_text(" I", WINDOW_WIDTH/2 - 8, WINDOW_HEIGHT - 45, arcade.color.LIME_GREEN, 40,)

         # if rectangles are called and available, draw them
        for rectangle in self.rectangle_list:
            rectangle.draw()

 
    def update(self, delta_time):
        """ Called to update our objects. Happens approximately 60 times per second. """
            # if rectangles are in list, update/redraw them
        for rectangle in self.rectangle_list:
            rectangle.update(delta_time)  

         # if balls are in list, update/redraw them
        for ball in self.ball_list:
            ball.update(delta_time, self.rectangle_list)
             # if the left side misses the ball, add one point to the right and respawn the ball in the left direction
            if ball.position_x <= ball.radius:
                ball.delta_x = -50
                ball.position_x = WINDOW_WIDTH/2
                ball.position_y = WINDOW_HEIGHT/2
                self.right_score += 1
            if self.right_score == 7:
                self.reset()

             # if the right side misses the ball, add one point to the left and respawn the ball in the right direction
            if ball.position_x >= WINDOW_WIDTH - ball.radius:
                ball.delta_x = 50
                ball.position_x = WINDOW_WIDTH/2
                ball.position_y = WINDOW_HEIGHT/2
                self.left_score += 1 
            if self.left_score == 7:
                self.reset()

    def reset(self): 
        # reset the scores for the left and the right side
        self.left_score = 0 
        self.right_score = 0 

        # reset the ball direction and movement speed
        for ball in self.ball_list:
            ball.delta_x = 50
            ball.delta_y = 50
        
        # reset the paddle position
        for rectangle in self.rectangle_list:
            rectangle.position_y = WINDOW_HEIGHT / 2


    def on_key_press(self, key, modifiers):
         # change the  pages when the space-bar is pressed 
        if key == arcade.key.SPACE:
                self.reset()

         # when key is pressed, activate movment for Y pos of left paddle
        if key == arcade.key.W:
            self.rectangle_list[0].delta_position_y = self.rectangle_list[0].movement_speed
        elif key == arcade.key.S:
            self.rectangle_list[0].delta_position_y = -self.rectangle_list[0].movement_speed

         # when key is pressed, activate movment for Y pos of right paddle
        if key == arcade.key.UP:
            self.rectangle_list[1].delta_position_y = self.rectangle_list[1].movement_speed
        elif key == arcade.key.DOWN:
            self.rectangle_list[1].delta_position_y = -self.rectangle_list[1].movement_speed

    def on_key_release(self, key, modifiers): 
         # if key released, stop movement of left paddle
        if key == arcade.key.W or key == arcade.key.S:
            self.rectangle_list[0].delta_position_y = 0

         # if key released, stop movement of right paddle
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.rectangle_list[1].delta_position_y = 0
    

def main():
    """ Create an instance of our game window and start the Arcade game loop. """
    window = MyGame(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    arcade.run()

 # only start the game if this script is executed as the main process
if __name__ == "__main__":
    main()