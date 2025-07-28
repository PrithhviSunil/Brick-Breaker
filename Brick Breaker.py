import pygame
from pygameRogers import Game, Room, GameObject, TextRectangle, Alarm
import random
import time
import math
g= Game(1000, 750)
global score
#resources
BLUE = (0,0,255)
WHITE = (255,255,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
RED = (255,0,0)
PURPLE = (160, 32, 240)
YELLOW = (255, 255, 0)
ORANGE = (255,92,0)
CYAN = (0,255,255)


gameFont = g.makeFont("Arial", 40)
ball_radius = 10
bg = g.makeBackground(BLACK)
custom_bg = g.makeBackground("arkanoid bg.jpg")
score =0
score_text = TextRectangle(f"Score:{score}",20, 700, gameFont, WHITE)
win_text = TextRectangle("YOU WIN", g.windowWidth//2, g.windowHeight//2, gameFont, GREEN)
win_text.rect.center = (g.windowWidth//2, g.windowHeight//2)
#create a room
r1 = Room("Game", custom_bg)
g.addRoom(r1)

r2 = Room("Win", bg)
g.addRoom(r2)

r3 = Room("Lose", bg)
g.addRoom(r3)

r1.addObject(score_text)




#classes for game objects
class platform(GameObject): #Player 

    def __init__(self, picture, xPos, fixed_yPos,  color ):
        GameObject.__init__(self, picture)
        self.rect.x= xPos
        self.rect.y = fixed_yPos #making it so that the player can only move horizontally
        self.color = color
        
    def update(self):
        
        
        self.rect.y = fixed_ypos
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]: #get the keyboard input for left
            if self.rect.left>0:
                self.rect.x -=20 #move the player left
            
        elif keys_pressed[pygame.K_RIGHT]:
            if self.rect.right <g.windowWidth:
                self.rect.x +=20 #move the player right
            

class Block(GameObject): #bricks to be destroyed
    def __init__(self, picture, xpos, ypos, color =None):
        GameObject.__init__(self, picture)
        self.rect.x = xpos
        self.rect.y = ypos
        self.has_pu = False #powerup attribute, if true, then the brick would release a powerup when broken
        self.color = color
        
    
    def update(self):
        global score
        if ball.rect.colliderect(self.rect):
            #ball bounce depends on where it collides with the block
            
            if ball.dx>0: #ball moving right
                change_x = ball.rect.right - self.rect.left
            if ball.dx <0: #ball moving left
                change_x = self.rect.right - ball.rect.left
            if ball.dy >0: #ball moving down
                change_y = ball.rect.bottom-self.rect.top
            if ball.dy<0: #ball moving up
                change_y = self.rect.bottom - ball.rect.top
            
            
            if change_x>change_y: #if yspeed is smaller, then the ball is more likely to bounce off the top or bottom, and it gets reversed vertically
                ball.yspeed *=-1
            elif change_y>change_x: #if xspeed is smaller, then the ball is more likely to bounce off the left or right, and it gets reversed horizontally
                ball.xspeed *=-1            
            r1.roomObjects.remove(self) #remove the brick if it collides with the ball
            block_list.remove(self)
            score +=10 #add score 
            score_text.setText(f"Score:{score}")
            if score==360: #if score is 360 that would mean all the bricks are destroyed, Player wins
                r2.addObject(win_text)
                g.nextRoom()
        
            if self.has_pu== True: #checks if the brick has a powerup
                powerup_color = random.choice([ORANGE, BLUE, RED])  # Randomly choose color
                powerup = PowerupBall(g.makeCircle(ball_radius, powerup_color), self.rect.x, self.rect.y, powerup_color) #assigns a powerup based on the color
                r1.addObject(powerup)
        
         

class Ball(GameObject):
    def __init__(self, picture, color, xPos, yPos):
        GameObject.__init__(self, picture)
        self.color = color
        self.xspeed = 10
        self.rect.x = xPos
        self.rect.y = yPos
        self.yspeed = 10
        self.dx = 1 #direction (either forward or backward)
        self.dy = -1 #direction

        ball_velocity = (self.xspeed**2 + self.yspeed**2)**0.5
        xdir = self.xspeed/ball_velocity
        ydir = self.yspeed/ball_velocity

        self.new_x = self.xspeed*xdir
        self.new_y = self.yspeed*ydir
          
    def update(self):
        self.rect.x += self.xspeed * self.dx #ball would move based on speed and direction
        self.rect.y += self.yspeed *self.dy

        self.wall_collide()
        self.ball_collide()
        
        
    def wall_collide(self): #checks if the bricks are colliding with the wall
        

        
        
        if self.rect.centery<ball_radius: #if the vertical coordinate of the center is smaller than the radius, the ball reverses vertically
            self.dy = -self.dy
        
        if self.rect.left <= 0:
            self.dx = -self.dx  # Reverse horizontal direction
            self.rect.left = 0  # Prevent the ball from getting stuck in the left wall

        # Handle collision with the right wall
        elif self.rect.right >= g.windowWidth:
            self.dx = -self.dx  # Reverse horizontal direction
            self.rect.right = g.windowWidth  # Prevent the ball from getting stuck in the right wall
                
            
        elif self.rect.bottom >=g.windowHeight: #game over if the ball falls below the player platform
            game_over_text = TextRectangle("GAME OVER", g.windowWidth//2, g.windowHeight//2, gameFont, RED)
            game_over_text.rect.center= (g.windowWidth//2, g.windowHeight//2)
            r3.addObject(game_over_text)
            g.goToRoom(2)
    
                
        
      
    
    def ball_collide(self):
        # Check for collision with the player paddle
        if self.rect.colliderect(Player.rect):
            # Only bounce if the ball is moving towards the paddle (left to right)
            self.dy = -self.dy
    

class PowerupBall(GameObject): #POWERUPS
    def __init__(self, picture, xPos, yPos, color):
        GameObject.__init__(self, picture)
        self.rect.x = xPos
        self.rect.y = yPos
        self.color = color

    def update(self):
        
        self.rect.y += 3 #powerup falls from the brick towards the player platform
        self.ball_collide()
        # Call the effect corresponding to the power-up's color
        if self.color == BLUE:
            self.blue()
        elif self.color == RED:
            self.red()
        elif self.color == ORANGE:
            self.orange()


    def ball_collide(self):        
        # Check for collision with the player paddle
        if self.rect.colliderect(Player.rect):
            r1.roomObjects.remove(self)
    
    def blue(self): #blue power up- increases the size of the player platform
        if self.rect.colliderect(Player.rect):
            Player.image=g.makeRectangle(250,17,BLACK) #changes the image of the platform
            Player.rect = Player.image.get_rect(center=Player.rect.center)
            pygame.time.set_timer(pygame.USEREVENT + 1, 5000) #set a timer to revert back after 5 seconds

    def red(self): #red power up- laser
        self.color=RED
        if self.rect.colliderect(Player.rect):
            laser = Laser(g.makeRectangle(5, 20, RED), Player.rect.centerx, Player.rect.centery) #calls the laser class
            r1.addObject(laser)
    
    def orange(self): #orange power up- slow down the ball
        self.color = ORANGE
        if self.rect.colliderect(Player.rect):
            ball_velocity = (ball.xspeed**2 + ball.yspeed**2)**0.5 #speed of the ball using x and y (pythagorean theorem)
            new_velocity = ball_velocity *0.5 #reducing it by 50%
            x_direction = ball.xspeed/ball_velocity
            y_direction = ball.yspeed/ball_velocity
            ball.xspeed = x_direction*new_velocity #define new velocity by multiplying the direction with the new speed
            ball.yspeed = y_direction*new_velocity
            pygame.time.set_timer(pygame.USEREVENT + 2, 5000) #set a timer to revert back after 5 seconds

#generate bricks
block_list = [] 
for i in range(9): #LIST to handle the bricks on the screen
    for j in range(4):
        color_list = [WHITE, ORANGE, CYAN, GREEN, BLUE, PURPLE, RED, YELLOW]
        color = random.choice(color_list)
        
        # Create the rectangle surface with size 100x50
        surface = g.makeRectangle(100, 50, color) #create each block with a width of 100 px, height of 50 px
        # Create the block with the colored surface at the specified position
        has_powerup = random.choice([True, False, False]) #lower chance for true
        block = Block(surface, 10 + 110 * i, 10 + 60 * j) #each block is created 10 pixels apart from each other sideways and 10 pixels apart from each other vertically
        if has_powerup==True: #generate powerup blocks
            block.has_pu = True
        else:
            block.has_pu= False
        
        # Append the block to the list
        block_list.append(block)

for block in block_list:
    r1.addObject(block) #add all blocks to the room

class Laser(GameObject):
    global score
    def __init__(self, picture, xPos, yPos):
        GameObject.__init__(self, picture)
        self.rect.x = xPos
        self.rect.y = yPos
        self.speed = 20  # Speed at which the laser moves upward

    def update(self):
        global score
        self.rect.y -= self.speed  # Move laser upward
        
        # Check if the laser goes off-screen
        if self.rect.bottom < 0:
            r1.roomObjects.remove(self)
        


        # Check for collision with blocks
        for block in block_list:
            if self.rect.colliderect(block.rect):
                r1.roomObjects.remove(block)  # Remove block on collision
                block_list.remove(block)
                score +=10
                score_text.setText(f"Score:{score}")
                break


                

#CREATING MAIN OBJECTS FOR THE GAME
ball = Ball(g.makeCircle(ball_radius, WHITE),WHITE, 400, 680)
r1.addObject(ball)

fixed_ypos = g.windowHeight -60 #for the player platform
Player = platform(g.makeRectangle(150, 17, BLACK), 400, fixed_ypos, BLACK)
r1.addObject(Player)        

g.start()

while g.running:
    
    time.sleep(0.05)
    #limit the game execution framerate
    dt = g.clock.tick(60)

    #check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            g.stop()
        if event.type == pygame.USEREVENT+1:
            Player.image=g.makeRectangle(150,17,BLACK)
            Player.rect = Player.image.get_rect(center=Player.rect.center) #reverts the player platform after a blue power up
        
        if event.type == pygame.USEREVENT+2:
            ball.xspeed = ball.new_x
            ball.yspeed = ball.new_y #reverts the player platform after an orange power up 
    #update the gamestate of all the objects
    
    g.currentRoom().updateObjects()
    
        


    #render the background to the window surface
    g.currentRoom().renderBackground(g)

    #render the object images to background
    g.currentRoom().renderObjects(g)

    #draw everything on the screen
    pygame.display.flip()
pygame.quit()



        

