
# importing pygame
import pygame
import networkx as nx
import math
import numpy as np

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

def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):

    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.  
    Licensed under Creative Commons Attribution-Share Alike 
    
    If the graph is a tree this will return the positions to plot this in a 
    hierarchical layout.
    
    G: the graph (must be a tree)
    
    root: the root node of current branch 
    - if the tree is directed and this is not given, 
      the root will be found and used
    - if the tree is directed and this is given, then 
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given, 
      then a random choice will be used.
    
    width: horizontal space allocated for this branch - avoids overlap with other branches
    
    vert_gap: gap between levels of hierarchy
    
    vert_loc: vertical location of root
    
    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''
    
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos

            
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

class BinaryNode:
	def __init__(self, data):
		self.left = None
		self.right = None		
		self.data = data
		self.name = None

	def getValStr(self):
		return str(self.data)

	def getEdges(self, edges):
		if self.left is not None:
			edges.append((self.name, self.left.name))
		if self.right is not None:
			edges.append((self.name, self.right.name))

		if self.left is not None:
			self.left.getEdges(edges)
		if self.right is not None:
			self.right.getEdges(edges)

	def arrange(self):
		G = nx.DiGraph()
		edges = []
		self.getEdges(edges)
		if len(edges) == 0:
			return [{0: (50, 50)}]

		G.add_edges_from([edge for edge in edges])
		pos =  hierarchy_pos(G) 
		return pos

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

	def __setName__(self, index):
		self.name = index
		if self.left is not None:
			index = self.left.__setName__(index + 1)
		if self.right is not None:
			index = self.right.__setName__(index + 1)

		return index

	def setName(self):
		self.__setName__(0)

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

	def showx(self, nodepos):
		pos = nodepos[self.name]
		x, y = pos[0], pos[1]
		# draw current
		pygame.draw.rect(win, (255, 0, 0), (x, y, NODE_WIDTH, NODE_HEIGHT))
		text = font.render(str(self.data), True, (0,0,255))
		win.blit(text, (x, y))			

		if self.left is not None:
			end = nodepos[self.left.name]
			end = end + np.asarray((0, NODE_HEIGHT))
			start = np.asarray((x, y))
			draw_arrow(win, (255, 255, 255), start, end, 20)

			self.left.showx(nodepos)

		if self.right is not None:
			end = nodepos[self.right.name]
			end = end + np.asarray((0, NODE_HEIGHT))

			start = np.asarray((x, y))
			draw_arrow(win, (255, 255, 255), start, end, 20)

			self.right.showx(nodepos)


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

	def vizx(self, pos):
		if self.head is None:
			return
		self.head.showx(pos)

	def arrange(self):
		pos = self.head.arrange()
		spos = {}
		for p in pos.items():
			loc = list(p[1])
			loc[0] = loc[0] / 2 + 0.5
			loc[0] *= (win_width - NODE_WIDTH)
			loc[1] = loc[1] / 2 + 0.5
			loc[1] *= (win_height - NODE_HEIGHT)
			spos[p[0]] = np.asarray(loc)

		print('pos = ', spos)
		return spos

	def setName(self):
		self.head.setName()


pygame.init()

# setting window size
win_width = 1400
win_height = 800
win = pygame.display.set_mode((win_width, win_height))

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
for i in range(len(height)):
	btree.insert(height[i])
btree.setName()
btree_pos = btree.arrange()
btree.reset()

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
		btree.vizx(btree_pos)

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
			btree.setName()
			btree.vizx(btree_pos)

			# create a time delay
			pygame.time.delay(1000)

			# update the display
			pygame.display.update()


		pygame.display.update()			
	


# exiting the main window
pygame.quit()
