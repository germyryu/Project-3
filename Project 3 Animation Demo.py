#################################################################
# Hw11
# Your Name: Jeremy Ryu
# Your Andrew ID: jihoonr
# Your Section: N
# Collaborators: stavares
#################################################################

import random, math

#### OOP Classes ####

## Asteroid and its subclasses, ShrinkingAsteroid and SplittingAsteroid ##

class Asteroid(object):
    # Model
    def __init__(self, cx, cy, r, speed, direction):
        # An asteroid has a position, size, speed, and direction
        self.cx = cx
        self.cy = cy
        self.r = r
        self.speed = speed
        self.direction = direction

    # View
    def draw(self, canvas, color="purple"):
        canvas.create_oval(self.cx - self.r, self.cy - self.r,
                           self.cx + self.r, self.cy + self.r,
                           fill=color)
    
    # Controller
    def moveAsteroid(self):
        self.cx += self.speed * self.direction[0]
        self.cy += self.speed * self.direction[1]
    
    def collidesWithWall(self, width, height):
        # Check if the asteroid hits the wall or overlaps it at all
        return self.cx - self.r <= 0 or self.cx + self.r >= width or \
            self.cy - self.r <= 0 or self.cy + self.r >= height
    
    #this function checks makes sure the normal asteroid wraps around
    def reactToWallHit(self, screenWidth, screenHeight):
        if self.cx-self.r<0:
            self.cx=screenWidth-self.r
        elif self.cx+self.r>screenWidth:
            self.cx=self.r
        elif self.cy-self.r<0:
            self.cy=screenHeight-self.r
        elif self.cy+self.r>screenHeight:
            self.cy=self.r
    
    #this function stuns the normal asteroid when hit by a bullet
    def reactToBulletHit(self):
        self.speed=0

class ShrinkingAsteroid(Asteroid):
    # Model
    def __init__(self, cx, cy, r, speed, direction):
        # Shrinking Asteroids also track how fast they shrink
        super().__init__(cx, cy, r, speed, direction)
        self.shrinkAmount = 5
    
    # View
    def draw(self, canvas):
        super().draw(canvas, color="pink")
    
    # Controller
    #this function makes sure the shrinking asteroid bounces inside the screen
    def reactToWallHit(self, screenWidth, screenHeight):
        self.speed=-1*self.speed
    
    #this function makes sure the shrinking asteroid shrinks
    def reactToBulletHit(self):
        self.r-=self.shrinkAmount

class SplittingAsteroid(Asteroid):  
    # View
    def draw(self, canvas):
        super().draw(canvas, color="blue")
    
    # Controller
    #this function returns a list of the two asteroids that result from
    #splitting one asteroid
    def reactToBulletHit(self):
        asteroid1=SplittingAsteroid(self.cx-self.r,self.cy-self.r,self.r//2,\
        self.speed,self.direction)
        asteroid2=SplittingAsteroid(self.cx+self.r,self.cy+self.r,self.r//2,\
        self.speed,self.direction)
        return [asteroid1,asteroid2]
    

## Rocket class ##

class Rocket(object):
    # Model
    def __init__(self, cx, cy):
        # A rocket has a position and a current angle it faces
        self.cx = cx
        self.cy = cy
        self.angle = 90

    # View
    def draw(self, canvas):
        # Draws a cool-looking triangle-ish shape
        size = 30
        angle = math.radians(self.angle)
        angleChange = 2*math.pi/3
        numPoints = 3
        points = []
        for point in range(numPoints):
            points.append((self.cx + size*math.cos(angle + point*angleChange),
                           self.cy - size*math.sin(angle + point*angleChange)))
        points.insert(numPoints-1, (self.cx, self.cy))
        
        canvas.create_polygon(points, fill="green2")

    # Controller
    def rotate(self, numDegrees):
        self.angle += numDegrees

    def makeBullet(self):
        # Generates a bullet heading in the direction the ship is facing
        offset = 35
        x = self.cx + offset*math.cos(math.radians(self.angle)) 
        y = self.cy - offset*math.sin(math.radians(self.angle))
        speedLow, speedHigh = 20, 40

        return Bullet(x, y, self.angle, random.randint(speedLow, speedHigh))

## Bullet Class ##

class Bullet(object):
    # Model
    def __init__(self, cx, cy, angle, speed):
        # A bullet has a position, a size, a direction, and a speed
        self.cx = cx
        self.cy = cy
        self.r = 5
        self.angle = angle
        self.speed = speed
    
    # View
    def draw(self, canvas):
        canvas.create_oval(self.cx - self.r, self.cy - self.r, 
                           self.cx + self.r, self.cy + self.r,
                           fill="white", outline=None)

    # Controller
    def moveBullet(self):
        # Move according to the original trajectory
        self.cx += math.cos(math.radians(self.angle))*self.speed
        self.cy -= math.sin(math.radians(self.angle))*self.speed

    def collidesWithAsteroid(self, other):
        # Check if the bullet and asteroid overlap at all
        if(not isinstance(other, Asteroid)): # Other must be an Asteroid
            return False
        else:
            dist = ((other.cx - self.cx)**2 + (other.cy - self.cy)**2)**0.5
            return dist < self.r + other.r
    
    def isOffscreen(self, width, height):
        # Check if the bullet has moved fully offscreen
        return (self.cx + self.r <= 0 or self.cx - self.r >= width) or \
               (self.cy + self.r <= 0 or self.cy - self.r >= height)

#### Graphics Functions ####

from tkinter import *

def init(data):
    data.rocket = Rocket(data.width//2, data.height//2)
    data.bullet=[]
    data.asteroids=[]
    #used to keep track of time
    data.step=0
    data.score = 0
    # TODO: add code here

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    if event.keysym == "Right":
        data.rocket.rotate(-5)
    elif event.keysym == "Left":
        data.rocket.rotate(5)
    #append the instance of bullet to the bullet list
    elif event.keysym=="space":
        data.bullet.append(data.rocket.makeBullet())
    # TODO: add code here

def timerFired(data):
    data.step+=1
    # TODO: add code here
    #takes care of the movement of the bullets on and off the screen
    for missile in data.bullet:
        missile.moveBullet()
        if missile.isOffscreen(data.width,data.height):
            data.bullet.remove(missile)
    #initializes the parameters of the asteroids in a random manner
    data.r=random.randint(20,100)
    data.cx=random.randint(0+data.r,data.width-data.r)
    data.cy=random.randint(0+data.r,data.height-data.r)
    data.speed=random.randint(5,20)
    #list of 4 directions that are described in a conditional statement below
    data.direction=random.choice(["left","right","up","down"])
    if data.direction=="left":
        data.direction=[-1,0]
    elif data.direction=="right":
        data.direction=[1,0]
    elif data.direction=="up":
        data.direction=[0,-1]
    else:
        data.direction=[0,1]
    
    #this list takes care of randomizing the type of asteroid that is called
    #every 2 seconds
    randL=[Asteroid(data.cx,data.cy,data.r,data.speed,data.direction),\
    ShrinkingAsteroid(data.cx,data.cy,data.r,data.speed,data.direction),\
    SplittingAsteroid(data.cx,data.cy,data.r,data.speed,data.direction)]
    
    if data.step%20==0:
        data.asteroids.append(random.choice(randL))

    for rock in data.asteroids:
        rock.moveAsteroid()
        if rock.collidesWithWall(data.width,data.height):
            rock.reactToWallHit(data.width,data.height)
    #every 10 seconds, any asteroid that is stunned should be removed from the
    #asteroids list, hence the screen  
    if data.step%100==0:
        for rock in data.asteroids:
            if rock.speed==0:
                data.asteroids.remove(rock)
                data.score+=1
    
    #loop through the bullets and asteroids and display the given results when
    #a bullet hits an asteroid
    for rock in data.asteroids:
        for missile in data.bullet:
            if missile.collidesWithAsteroid(rock):
                data.bullet.remove(missile)
                rock.reactToBulletHit()
                #checks if radius is less than or equal to 15
                if isinstance(rock,ShrinkingAsteroid):
                    if rock.r<=15:
                        try:
                            data.asteroids.remove(rock)
                            data.score+=1
                        except:
                            pass
                #checks if it is possible to split the asteroid into more
                #asteroids
                if isinstance(rock,SplittingAsteroid):
                    try:
                        data.asteroids.remove(rock)
                        data.score+=1
                    except:
                        pass
                    for i in rock.reactToBulletHit():
                        if i.r>0:
                            data.asteroids.append(i)
                            
def redrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="gray3")
    data.rocket.draw(canvas)
    for missile in data.bullet:
        missile.draw(canvas)
    for rock in data.asteroids:
        rock.draw(canvas)
    # TODO: add code here
    canvas.create_text(data.width/2, data.height, anchor="s", fill="yellow",
                       font="Arial 24 bold", text="Score: " + str(data.score))

#################################################################
# use the run function as-is
#################################################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)