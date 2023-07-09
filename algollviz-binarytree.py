
# importing pygame
import pygame
import math

# https://stackoverflow.com/questions/43527894/drawing-arrowheads-which-follow-the-direction-of-the-line-in-pygame vladimir
def draw_arrow(screen, colour, start, end, sz):
    pygame.draw.line(screen,colour,start,end,2)
    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
    pygame.draw.polygon(screen, (155, 255, 0), ((end[0]+sz*math.sin(math.radians(rotation)), end[1]+sz*math.cos(math.radians(rotation))), 
					      (end[0]+sz*math.sin(math.radians(rotation-120)), end[1]+sz*math.cos(math.radians(rotation-120))), 
					      (end[0]+sz*math.sin(math.radians(rotation+120)), end[1]+sz*math.cos(math.radians(rotation+120)))))	

NODE_WIDTH = 50
NODE_HEIGHT = 40
NODE_SPACING = 160

class BinaryNode:
	def __init__(self, data):
		self.left = None
		self.right = None		
		self.data = data

	def insert(self, val):
		if val.data < self.data:
			if self.left is None:
				self.left = val
			else:
				self.left.insert(val)
		else:
			if self.right is None:
				self.right = val
			else:
				self.right.insert(val)							


	# method to show the list of height
	def show(self, pos, node_spacingx, node_spacingy):
		x, y = pos[0], pos[1]
		# draw current
		pygame.draw.rect(win, (255, 0, 0), (x, y, NODE_WIDTH, NODE_HEIGHT))
		text = font.render(str(self.data), True, (0,0,255))
		win.blit(text, (x, y))			

		if self.left is not None:
			xleft = x + node_spacingx
			yleft = y - node_spacingy

			start = (x, y)
			end = (x + node_spacingx, y - node_spacingy) 
			draw_arrow(win, (255, 255, 255), start, end, 20)

			self.left.show((xleft, yleft), node_spacingx, node_spacingy-50)

		if self.right is not None:
			xright = x + node_spacingx
			yright = y + node_spacingy

			start = (x, y)
			end = (x + node_spacingx, y + node_spacingy) 
			draw_arrow(win, (255, 255, 255), start, end, 20)

			self.right.show((xright, yright), node_spacingx, node_spacingy-50)



class BinaryTree:
	def __init__(self):
		self.head = None
		self.counter = 0

	def insert(self, val):
		if self.head is None:
			self.head = BinaryNode(val)
			self.counter +=1
			return

		self.head.insert(BinaryNode(val))
		self.counter +=1

	def reset(self):
		self.head = None

	def viz(self):
		if self.head is None:
			return

		self.head.show((50, 300), NODE_SPACING, NODE_SPACING+30)		

	

pygame.init()

# setting window size
win = pygame.display.set_mode((1400, 800))

# setting title to the window
pygame.display.set_caption("Bubble sort")

font = pygame.font.SysFont(None, 36)


# initial position
x = 40
y = 40

# width of each bar
width = 20

# height of each bar (data to be sorted)
height = [100, 50, 130, 90, 250, 61, 110, 88]

run = True

		
		
btree = BinaryTree()
        

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
		btree.viz()

		# update the window
		pygame.display.update()

	# if execute flag is true
	else:

		# start sorting using bubble sort technique
		btree.reset()
		for i in range(len(height)):
			# fill the window with black color
			win.fill((0, 0, 0))

			btree.insert(height[i])
			btree.viz()

			# create a time delay
			pygame.time.delay(20)

			# update the display
			pygame.display.update()

# exiting the main window
pygame.quit()
