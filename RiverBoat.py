import random
import math

#### OOP Classes ####

## Classes we need to create are:
## River, Boat, and Background ##

## River class ##
class River(object):
    # Model
    def __init__(self, cx, cy, length, width, speed, direction):
        # A river has a position, length, width, speed, and direction
        # Direction is defined as an angle from the positive x-axis
        self.cx = cx
        self.cy = cy
        self.length = length
        self.width = width
        self.speed = speed
        self.direction = direction
        self.angle = None

    def getAngle(self):
        # get an angle based off of the direction
        if self.direction == 'W':
            self.angle = math.pi
        elif self.direction == 'E':
            self.angle = 0
        elif self.direction == 'NE':
            self.angle = math.pi/6
        elif self.direction == 'NW':
            self.angle = 5*math.pi/6
        elif self.direction == 'SE':
            self.angle = -math.pi/6
        elif self.direction == 'SW':
            self.angle = -5*math.pi/6
        else:
        # no direction
            self.angle = None
        return self.angle 

    # View
    def draw(self, canvas, color="blue"):
        canvas.create_rectangle(self.cx - self.length/2, self.cy - self.width/2,
                           self.cx + self.length/2, self.cy + self.width/2,
                           fill=color)
        canvas.create_text(9*self.length//10, self.cy-self.width//3, text=self.direction)
 
## Boat class ##
class Boat(object):
    # Model
    def __init__(self, cx, cy, angle=90):
        # A boat has a position and a current angle it faces with respect to the river
        self.cx = cx
        self.cy = cy
        self.angle = angle
        self.speed = 10

    # View
    def draw(self, canvas):
        # Treat the boat as a triangle for now
        size = 10
        angle = math.radians(self.angle)
        angleChange = 2*math.pi/3
        numPoints = 3
        points = []
        for point in range(numPoints):
            points.append((self.cx + size*math.cos(angle + point*angleChange),
                           self.cy - size*math.sin(angle + point*angleChange)))
        points.insert(numPoints-1, (self.cx, self.cy))
        
        canvas.create_polygon(points, fill="brown4")

    # Controller
    # Rotate the boat so that the user can aim the boat in a certain direction
    def rotate(self, numDegrees):
        newAngle = self.angle + numDegrees
        if (newAngle < 180 and newAngle > 0):
            self.angle = newAngle
    
    # Move the boat along the river
    def move(self, dx, dy):
        self.cx += dx
        self.cy -= dy
        
        

## Background Class ##
##TODO: add more images for background
class Background(object):
    # Model
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
    
    # View
    def draw(self, canvas, data):
        canvas.create_rectangle(0, 0, data.width, data.height,
                           fill="green", outline=None)

    def drawGoal(self, canvas, data):
        return

#### Graphics Functions ####

from tkinter import *

def init(data):
    # initalize the rivers, this way multiple rivers can be used
    data.rivers = []
    for i in range(4):
        speed = random.randint(1,5)
        direction = random.choice(['W', 'E', 'NW', 'NE', 'SE', 'SW'])
        cx = data.width//2
        cy = data.height - 70 - 130 * i

        r = River(cx, cy, data.width, data.height//6, speed, direction)
        data.rivers.append(r)

    data.boat = Boat(data.width//2, data.height - 10)
    data.background = Background(0, 0)
    # used to keep track of time
    data.step=0
    data.startSeconds = 15
    # used to keep track of game state
    # 0: start, 1: channel, 2: game, 3: end
    data.state=1
    # current river
    data.curr=0

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    k = event.keysym

    if data.state == 1:
        if k == 's':
            data.state += 1
        elif k == 'Space':
            data.state += 1
        elif k == 'q':
            data.state -= 1

    if data.state == 2:
        if k == "Right":
            data.boat.rotate(-10)
        elif k == "Left":
            data.boat.rotate(10)

def timerFired(data):
    data.step+=1
    
    if data.state == 1:
        if data.step % 4 == 0:
            data.startSeconds -= 1
            if data.startSeconds == 0:
                data.state += 1

    
    if data.state == 2:
        # takes care of the movement of the boat on the screen
        # calculate dx and dy
        (dx, dy) = calculateBoatVelocity(data)
        data.boat.move(dx, dy)
    
    
    #checks if the boat comes in contact with the desired location
    #if data.boat.collision:
        ##TODO: IMPLEMENTATION NEEDED
            
def calculateBoatVelocity(data):
    # helper function to determine dx and dy
    boatAngle = data.boat.angle
    boatAngle = boatAngle * math.pi // 180
    r = data.rivers[data.curr]
    riverAngle = r.getAngle()
    dy = (data.boat.speed * math.sin(boatAngle)) + (r.speed * math.sin(riverAngle))
    dx = (data.boat.speed * math.cos(boatAngle)) + (r.speed * math.sin(riverAngle))
    if (data.boat.cx + dx < data.width and data.boat.cx - dx > 0):
        if (data.boat.cy - dy > 100):
            return (dx, dy)
    return (0, 0)

def redrawAll(canvas, data):
    if data.state == 1:
        warning = "Game begins in " + str(data.startSeconds) + " seconds"
        canvas.create_text(data.width//2, data.height//2, text=warning, fill='green',
                                font=("ComicSansMS" + " 50 " + " bold "))
        beginnow = "Press s or Space to begin now"
        canvas.create_text(data.width//2, data.height//2 + 50, text=beginnow,
                            fill='black', font=("ComicSansMS" + " 30 " + "bold"))
    
    if data.state == 2:
        # game screen
        canvas.create_rectangle(0, 0, data.width, data.height, fill="gray3")
        data.background.draw(canvas, data)
        for r in data.rivers:
            r.draw(canvas)
        data.boat.draw(canvas)
    

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
	data.timerDelay = 250 # milliseconds
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
