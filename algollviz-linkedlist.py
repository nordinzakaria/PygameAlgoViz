
# importing pygame
import pygame
import math

# https://stackoverflow.com/questions/43527894/drawing-arrowheads-which-follow-the-direction-of-the-line-in-pygame vladimir
def draw_arrow(screen, colour, start, end, sz):
    pygame.draw.line(screen,colour,start,end,2)
    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
    pygame.draw.polygon(screen, (255, 0, 0), ((end[0]+sz*math.sin(math.radians(rotation)), end[1]+sz*math.cos(math.radians(rotation))), 
					      (end[0]+sz*math.sin(math.radians(rotation-120)), end[1]+sz*math.cos(math.radians(rotation-120))), 
					      (end[0]+sz*math.sin(math.radians(rotation+120)), end[1]+sz*math.cos(math.radians(rotation+120)))))	

class LNode:
	def __init__(self, data):
		self.next = None
		self.data = data

	def insert(self, val):
		tracker = self
		while (tracker.next is not None):
			tracker = tracker.next
			
		tracker.next = val

	# method to show the list of height
	def show(self):

		tracker = self
		x = 50
		y = 150
		width = 70
		height = 60
		spacing = 150
		while (tracker is not None):
			pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
			x += spacing
			tracker = tracker.next

		font = pygame.font.SysFont(None, 16)
		tracker = self
		x = 50
		y = 150
		width = 70
		height = 60
		spacing = 150
	
		while (tracker is not None):
			text = font.render(str(tracker.data), True, (0,0,255))
			win.blit(text, (x, y))			
			x += spacing
			tracker = tracker.next



		tracker = self
		x = 50 + width
		y = 150 

		index = 0
		while (tracker.next is not None):
			start = (x, y)
			end = (x + spacing/3, y) 
			draw_arrow(win, (255, 255, 255), start, end, 20)
			x += spacing
			index+=1
			print("at index" , index)
			tracker = tracker.next



class LinkedList:
	def __init__(self):
		self.head = None
		self.counter = 0

	def insert(self, val):
		if self.head is None:
			self.head = LNode(val)
			self.counter +=1
			return

		self.head.insert(LNode(val))
		self.counter +=1

	def reset(self):
		self.head = None


	def viz(self):
		if self.head is None:
			return

		self.head.show()		

	

pygame.init()

# setting window size
win = pygame.display.set_mode((1400, 800))

# setting title to the window
pygame.display.set_caption("Bubble sort")

# initial position
x = 40
y = 40

# width of each bar
width = 20

# height of each bar (data to be sorted)
height = [200, 50, 130, 90, 250, 61, 110, 88]

run = True

		
		
llist = LinkedList()
        

# infinite loop
while run:

	# execute flag to start sorting
	execute = False

	# time delay
	pygame.time.delay(10)

	# getting keys pressed
	keys = pygame.key.get_pressed()

	# iterating events
	for event in pygame.event.get():

		# if event is to quit
		if event.type == pygame.QUIT:

			# making run = false so break the while loop
			run = False

	# if space bar is pressed
	if keys[pygame.K_SPACE]:
		# make execute flag to true
		execute = True

	# checking if execute flag is false
	if execute == False:

		# fill the window with black color
		win.fill((0, 0, 0))

		# call the height method to show the list items
		llist.viz()

		# update the window
		pygame.display.update()

	# if execute flag is true
	else:

		# start sorting using bubble sort technique
		llist.reset()
		for i in range(len(height)):
			# fill the window with black color
			win.fill((0, 0, 0))

			llist.insert(height[i])
			llist.viz()

			# create a time delay
			pygame.time.delay(20)

			# update the display
			pygame.display.update()

# exiting the main window
pygame.quit()
