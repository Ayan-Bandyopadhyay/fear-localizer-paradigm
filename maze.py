# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sys
import pygame
from pygame.locals import *
import random 
import math
from collections import deque

SIDE = 110

class User(pygame.sprite.Sprite):
    
    def __init__(self, walls):
        PURPLE = (128, 0, 128)
        WHITE = (255,255,255)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill(WHITE)
        pygame.draw.polygon(self.image, PURPLE, ((0, 50), (25, 0), (50, 50)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (5, 5)
        self.walls = walls
        
        
        
    def move(self, direction, speed):
        old_x = self.rect.topleft[0]
        old_y = self.rect.topleft[1]
        new_x = old_x
        new_y = old_y
        
        if direction == 'r':
            new_x += speed
        elif direction == 'l':
            new_x -= speed
        elif direction == 'u':
            new_y -= speed
        elif direction == 'd':
            new_y += speed
        
        self.rect.topleft = (new_x, new_y)
        
        if pygame.sprite.spritecollide(self, self.walls, False):
            self.rect.topleft = (old_x, old_y)

class Wall(pygame.sprite.Sprite):
    
    def __init__(self, x, y, width, height):
        BLACK = (0, 0, 0)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width,height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
class Predator(pygame.sprite.Sprite):
    def __init__(self, walls, user, user_grp, pos, width, height ):
        BLACK = (0, 0, 0)
        ORANGE = (255, 165, 0)
        GREEN = (0, 255, 0)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        pygame.draw.circle(self.image, ORANGE, (SIDE/2,SIDE/2), SIDE/2)
        pygame.draw.rect(self.image, GREEN, (0,0,SIDE,SIDE), 5)
        self.rect = self.image.get_rect()
        self.initial_pos = pos
        self.rect.topleft = pos
        self.walls = walls
        self.player = user
        self.player_grp = user_grp
        self.phase = "A"
        self.graph = Graph()
        self.move_counter = SIDE
        self.start_node = self.graph.nodes[4][4]
        self.at_node = False
        self.next_node = self.graph.nodes[4][4]
        self.visited = [[]]
        self.visited = [[{'visited': False, 'from' : Node( (-1, -1))}  
                        for i in xrange(9)] for i in xrange(9)]
                
    def clear_visited(self):
        for i in xrange(9):
            for j in xrange(9):
                self.visited[i][j]['visited'] = False
                self.visited[i][j]['from'] = Node( (-1, -1))
    
    def reset(self, walls, user, user_grp, pos, width, height ):
        BLACK = (0, 0, 0)
        ORANGE = (255, 165, 0)
        GREEN = (0, 255, 0)
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        pygame.draw.circle(self.image, ORANGE, (SIDE/2,SIDE/2), SIDE/2)
        pygame.draw.rect(self.image, GREEN, (0,0,SIDE,SIDE), 5)
        self.rect = self.image.get_rect()
        self.initial_pos = pos
        self.rect.topleft = pos
        self.walls = walls
        self.player = user
        self.player_grp = user_grp
        self.phase = "A"
        self.graph = Graph()
        self.move_counter = SIDE
        self.start_node = self.graph.nodes[4][4]
        self.at_node = False
        self.next_node = self.graph.nodes[4][4]
        
        for i in xrange(9):
            for j in xrange(9):
                self.visited[i][j]['visited'] = False
                self.visited[i][j]['from'] = Node( (-1, -1))
    def set_phase(self, string):
        self.phase = string
    def update_img(self):
        BLACK = (0, 0, 0)
        ORANGE = (255, 165, 0)
        GREEN = (0, 255, 0)
        if self.phase == "A":
            self.image.fill(BLACK)
            pygame.draw.circle(self.image, ORANGE, (SIDE/2,SIDE/2), SIDE/2)
            pygame.draw.rect(self.image, GREEN, (0,0,SIDE,SIDE), 5)
            self.rect.topleft = self.initial_pos
            return
        elif self.phase == "B":
            self.image.fill(BLACK)
            pygame.draw.circle(self.image, ORANGE, (SIDE/2,SIDE/2), SIDE/2)
            self.rect.topleft = self.initial_pos
        elif self.phase == "C":
            WHITE = (255, 255, 255)
            self.image.fill(WHITE)
            pygame.draw.circle(self.image, ORANGE, (SIDE/2,SIDE/2), SIDE/2)
            self.rect.topleft = (self.initial_pos[0],self.initial_pos[1]-SIDE)
    def find_next_node(self, start_node, dest_node):
        
        frontier = deque()
        frontier.append(start_node)
        self.visited[start_node.maze_row][start_node.maze_col]['visited'] = True
        
        
        if not frontier:
            print 'queue is empty'
        while frontier:
            current_node = frontier.popleft()
            if (current_node.maze_row == dest_node.maze_row
                and current_node.maze_col == dest_node.maze_col):
                    break
            for neighbor in self.graph.get_neighbors(current_node):
                if (not self.visited[neighbor.maze_row][neighbor.maze_col]['visited']):
                    frontier.append(neighbor)
                    self.visited[neighbor.maze_row][neighbor.maze_col]['visited'] = True
                    self.visited[neighbor.maze_row][neighbor.maze_col]['from']=current_node
        
        next_step = dest_node
        path = []

        while next_step.maze_coord != start_node.maze_coord:            
            path.append(next_step)
            next_step = self.visited[next_step.maze_row][next_step.maze_col]['from']

        last = path[-1]
        
        return  self.graph.nodes[ last.maze_row][ last.maze_col ]
    def move(self):
        old_x = self.rect.topleft[0]
        old_y = self.rect.topleft[1]
        new_x = old_x
        new_y = old_y
        dest_node = self.graph.get_node(self.player.rect.topleft)
        distance = math.sqrt( (self.rect.topleft[0]-self.player.rect.topleft[0])**2 + (self.rect.topleft[1]-self.player.rect.topleft[1])**2)

        if pygame.sprite.spritecollide(self, self.player_grp, False): 
            return True
        else:
            self.at_node = False            
            
            if (self.move_counter == SIDE):                    
                self.move_counter = 0
                self.at_node = True
            
            if self.at_node:
                self.current_node = self.next_node
                if pygame.sprite.spritecollide(self, self.player_grp, False): 
                    return True
                
                self.next_node = self.find_next_node(self.current_node, dest_node)
                self.clear_visited()

            speed = 5
            if (distance < SIDE*3):
                speed = 4
            if (self.move_counter >=SIDE-5):
                speed = SIDE - self.move_counter
            
            if self.next_node.topleft[0] > old_x:
                new_x = old_x + speed
            elif self.next_node.topleft[0] < old_x:
                new_x = old_x - speed
            elif self.next_node.topleft[1] > old_y:
                new_y = old_y + speed
            else:
                new_y = old_y - speed

            
        self.move_counter += speed
        self.rect.topleft = (new_x, new_y)
        self.at_node = False
        return False
        
        
        
class Graph(object):
    def __init__(self):

        self.maze = [[1,1,1,1,1,1,1,1,1],
                     [1,0,0,0,1,0,0,0,1],
                     [1,0,0,0,0,0,0,0,1],
                     [1,0,1,1,0,0,1,0,1],
                     [1,0,0,0,0,0,0,0,1],
                     [1,0,0,0,1,1,0,0,1],
                     [1,0,1,0,0,0,0,1,1],
                     [1,0,0,0,0,0,0,0,1],
                     [1,1,1,1,1,1,1,1,1]]
        
        self.nodes = self.generate_nodes()
        

    def generate_nodes(self):
        nodes = []
        
        def generate_node(tup, y_coord):
            if tup[1] == 0:
                return Node((5+ SIDE*(tup[0]-1), y_coord))
            else:
                return None
                
        for row_index, row in enumerate(self.maze):
            y = 5 + SIDE*(row_index-1)
            new_row = [generate_node(x, y) for x in enumerate(row)]
            nodes.append(new_row)
            
        return nodes
        
    def get_node(self, coords):
        y_coord = coords[1]
        x_coord = coords[0]  
        row_num = 1 + int( (y_coord -5)/SIDE)
        col_num = 1 + int( (x_coord -5)/SIDE)
        
        return self.nodes[row_num][col_num];
                
    def get_neighbors(self, node):
        

        neighbors = [self.nodes[node.maze_row +1][node.maze_col],
                     self.nodes[node.maze_row -1][node.maze_col],
                     self.nodes[node.maze_row][node.maze_col +1],
                     self.nodes[node.maze_row][node.maze_col -1]]
        neighbors = filter(lambda x: x is not None, neighbors)         
        
        return neighbors

class Node(object):
    def __init__(self, coords):
        self.topleft = coords
        self.maze_row = ((coords[1]-5)/SIDE ) +1
        self.maze_col = ((coords[0]-5)/SIDE ) +1 
        self.maze_coord = (self.maze_row,self.maze_col)
    def __str__(self):
        return "(%d,%d)" % (self.maze_row, self.maze_col)
        
class Game(object):
    def __init__(self):
        height = SIDE*7 + 10
        width = SIDE*7 + 10
        self.screen = pygame.display.set_mode((width, height))
        self.walls = self.create_walls()
        self.player = User(self.walls)
        self.player_grp = pygame.sprite.Group(self.player)
        RED = (255,0,0)
        self.red_square = pygame.Surface((SIDE,SIDE))
        self.red_square.fill(RED)
        self.clock = pygame.time.Clock()
        self.pred = Predator(self.walls, self.player, self.player_grp, 
                             (5+SIDE*3, 5+SIDE*4), SIDE, SIDE)
        self.pred_grp = pygame.sprite.Group(self.pred)
        self.file = open("coordinates.txt", "w")
    def create_walls(self):
        wall_coords = [[1,1,1,1,1,1,1,1,1],
                       [1,0,0,0,1,0,0,0,1],
                       [1,0,0,0,0,0,0,0,1],
                       [1,0,1,1,0,0,1,0,1],
                       [1,0,0,0,0,0,0,0,1],
                       [1,0,0,0,1,1,0,0,1],
                       [1,0,1,0,0,0,0,1,1],
                       [1,0,0,0,0,0,0,0,1],
                       [1,1,1,1,1,1,1,1,1]]
        walls = pygame.sprite.Group()
        y = 0
        for row in range(len(wall_coords)):
            
            if row == 0 or (row == len(wall_coords) - 1):
                for i in range(len(wall_coords[row])):
                    if wall_coords[row][i] == 1:
                        walls.add(Wall(SIDE*i, y, SIDE, 5))
                y += 5
            else:          
                for i in range(len(wall_coords[row])):
                    if wall_coords[row][i] == 1:
                        if i == 0:
                            walls.add(Wall(0, y, 5, SIDE))
                        elif i == (len(wall_coords[row]) -1):
                            walls.add(Wall(5 + SIDE*(i-1), y, 5, SIDE))
                        else:
                            walls.add(Wall(5 + SIDE*(i-1), y, SIDE, SIDE))
                y += SIDE
        return walls
        
    def render_screen(self):    
        WHITE = (255, 255, 255)
        self.screen.fill(WHITE)
        self.walls.draw(self.screen)
        self.player_grp.draw(self.screen)
        self.pred_grp.draw(self.screen)
    
    def refresh_screen(self, show_square, square_coords):
        WHITE = (255, 255, 255)
        self.screen.fill(WHITE)
        self.walls.draw(self.screen)
        if show_square:
            self.screen.blit(self.red_square, square_coords)
        self.player_grp.draw(self.screen)
        self.pred_grp.draw(self.screen)
        pygame.display.flip()
        
    def select_random_coords(self):
        # for a 7x7 square map
        maze = [[1,1,1,1,1,1,1,1,1],
                [1,0,0,0,1,0,0,0,1],
                [1,0,0,0,0,0,0,0,1],
                [1,0,1,1,0,0,1,0,1],
                [1,0,0,0,0,0,0,0,1],
                [1,0,0,0,1,1,0,0,1],
                [1,0,1,0,0,0,0,1,1],
                [1,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1]]
        
        rand_row = random.choice(range(1,8))
        
        pos_indices = [i for i, item in enumerate(maze[rand_row]) if item == 0]
        
        rand_col = random.choice(pos_indices)
        
        x_coord = 5 + (rand_col-1)*SIDE
        y_coord = 5 + (rand_row-1)*SIDE
        return (x_coord, y_coord)
        
    def phase_A(self, time):
        
        self.pred.set_phase("A")
        self.pred.update_img()
        flash_square = pygame.USEREVENT + 1
        show_square = False
        square_timer = 0
        phase_timer = 0
        position_timer = 0
        timer = time
        square_coords = (0,0)
        
        self.file.write(" \r\n Phase A: \r\n")
        self.render_screen()
        pygame.time.set_timer(flash_square, 5000)
        self.clock.tick(40) 
        while(phase_timer <= 30000):
            self.clock.tick(40) 
            phase_timer += self.clock.get_time()
            position_timer += 1
            if (position_timer % 20 == 0):
                output = "(%d, %d) Time: %d \r\n" %(self.player.rect[0], self.player.rect[1],(phase_timer+timer))
                self.file.write(output)
            pygame.event.pump()
            keys = pygame.key.get_pressed()
                    
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                if event.type == flash_square:
                    show_square = True
                    square_coords = self.select_random_coords()
                    
            if show_square:
                square_timer += self.clock.get_time()
                if square_timer >= 100:
                    show_square = False
                    square_timer = 0
                    
                    
            right = False;
            left = False;
            up = False;
            down = False;
            
            if (keys[K_RIGHT]):
                right = True
            if (keys[K_LEFT]):
                left = True  
            if (keys[K_UP]):
                up = True               
            if (keys[K_DOWN]):
                down = True
            if (keys[K_ESCAPE]):
                break
            
            if(right and up):
                self.player.move('r', 5/(math.sqrt(2)))
                self.player.move('u', 5/(math.sqrt(2)))
            elif(right and down):
                self.player.move('r', 5/(math.sqrt(2)))
                self.player.move('d', 5/(math.sqrt(2)))
            elif(left and up):
                self.player.move('l', 5/(math.sqrt(2)))
                self.player.move('u', 5/(math.sqrt(2)))
            elif(left and down):
                self.player.move('l', 5/(math.sqrt(2)))
                self.player.move('d', 5/(math.sqrt(2)))
            elif(right):
                self.player.move('r', 5)
            elif(left):
                self.player.move('l', 5)
            elif(up):
                self.player.move('u', 5)
            elif(down):
                self.player.move('d', 5)
                    
            
            
            self.refresh_screen(show_square, square_coords)
            
        return (timer + phase_timer)
        
    def phase_B(self, time):
        self.pred.set_phase("B")
        self.pred.update_img()
        show_square = False
        square_timer = 0
        phase_timer = 0
        flash_square = pygame.USEREVENT + 1
        timer = time
        square_coords = (0,0)
        wait_time =  1000 * (random.choice(range(2,25)))
        wait_counter = 0
        position_timer = 0
        done = False
        attack = False
        
        self.file.write(" \r\n Phase B: \r\n")
        self.render_screen()
        pygame.time.set_timer(flash_square, 5000)
        self.clock.tick(40) 
        while(phase_timer <= 30000):
            self.clock.tick(40) 
            phase_timer += self.clock.get_time()
            position_timer += 1
            if (position_timer % 20 == 0):
                output = "(%d, %d) Time: %d \r\n" %(self.player.rect[0], self.player.rect[1],(phase_timer+timer))
                self.file.write(output)
            if (wait_counter >= 0):
                wait_counter += self.clock.get_time()
                          
            pygame.event.pump()
            keys = pygame.key.get_pressed()
                    
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                if (event.type == flash_square and phase_timer < wait_time):
                    show_square = True
                    square_coords = self.select_random_coords()
                    
                    
            if show_square:
                square_timer += self.clock.get_time()
                if square_timer >= 100:
                    show_square = False
                    square_timer = 0
                    
                    
            right = False;
            left = False;
            up = False;
            down = False;
            
            if (keys[K_RIGHT]):
                right = True
            if (keys[K_LEFT]):
                left = True  
            if (keys[K_UP]):
                up = True               
            if (keys[K_DOWN]):
                down = True
            if (keys[K_ESCAPE]):
                break
            
            if(right and up):
                self.player.move('r', 5/(math.sqrt(2)))
                self.player.move('u', 5/(math.sqrt(2)))
            elif(right and down):
                self.player.move('r', 5/(math.sqrt(2)))
                self.player.move('d', 5/(math.sqrt(2)))
            elif(left and up):
                self.player.move('l', 5/(math.sqrt(2)))
                self.player.move('u', 5/(math.sqrt(2)))
            elif(left and down):
                self.player.move('l', 5/(math.sqrt(2)))
                self.player.move('d', 5/(math.sqrt(2)))
            elif(right):
                self.player.move('r', 5)
            elif(left):
                self.player.move('l', 5)
            elif(up):
                self.player.move('u', 5)
            elif(down):
                self.player.move('d', 5)
            
            if(wait_counter >= wait_time):
                wait_counter = -1
                self.pred.set_phase("C")
                self.pred.update_img()
                attack = True
                
            if (attack):
                done = self.pred.move()
                
            self.refresh_screen(show_square, square_coords)  
            if done:
                break
            
        self.pred.reset(self.walls, self.player, self.player_grp, 
                             (5+SIDE*3, 5+SIDE*4), SIDE, SIDE)
        return (phase_timer + timer)
        
    def phase_C(self, time):
        self.pred.set_phase("C")
        self.pred.update_img()
        self.player.rect.topleft = (5,5)
        show_square = False
        phase_timer = 0
        timer = time
        square_coords = (0,0)
        self.render_screen()
        self.clock.tick(40) 
        self.file.write(" \r\n Phase C: \r\n")
        done = False
        
        position_timer = 0
        while(phase_timer <= 30000):
            self.clock.tick(40) 
            phase_timer += self.clock.get_time()
            position_timer += 1
            if (position_timer % 20 == 0):
                output = "(%d, %d) Time: %d \r\n" %(self.player.rect[0], self.player.rect[1],(phase_timer+timer))
                self.file.write(output)
                
            pygame.event.pump()
            keys = pygame.key.get_pressed()
                    
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
            right = False;
            left = False;
            up = False;
            down = False;
            
            if (keys[K_RIGHT]):
                right = True
            if (keys[K_LEFT]):
                left = True  
            if (keys[K_UP]):
                up = True               
            if (keys[K_DOWN]):
                down = True
            if (keys[K_ESCAPE]):
                break
            
            if(right and up):
                self.player.move('r', 5/(math.sqrt(2)))
                self.player.move('u', 5/(math.sqrt(2)))
            elif(right and down):
                self.player.move('r', 5/(math.sqrt(2)))
                self.player.move('d', 5/(math.sqrt(2)))
            elif(left and up):
                self.player.move('l', 5/(math.sqrt(2)))
                self.player.move('u', 5/(math.sqrt(2)))
            elif(left and down):
                self.player.move('l', 5/(math.sqrt(2)))
                self.player.move('d', 5/(math.sqrt(2)))
            elif(right):
                self.player.move('r', 5)
            elif(left):
                self.player.move('l', 5)
            elif(up):
                self.player.move('u', 5)
            elif(down):
                 self.player.move('d', 5)
            
            done = self.pred.move()

            self.refresh_screen(show_square, square_coords) 
            if done:
                break
            
        self.pred.reset(self.walls, self.player, self.player_grp, 
                             (5+SIDE*3, 5+SIDE*4), SIDE, SIDE)
        return (phase_timer + timer)
        
    def wait_screen(self, msg):
        WHITE = (255, 255, 255)
        wait_clock = pygame.time.Clock()
        wait_timer = 0        
        
        wait_clock.tick(40)
        self.screen.fill(WHITE)
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render(msg, 1, (0,0,0))
        self.screen.blit(label, (100, 100))
        pygame.display.flip()
        while(wait_timer < 5000):
            wait_clock.tick(40)
            wait_timer += wait_clock.get_time()
            pygame.event.pump()       
            key_list = pygame.key.get_pressed()
            if (key_list[K_RETURN]):
                break
            if (key_list[K_ESCAPE]):
                pygame.quit()
                sys.exit()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
        
    def play(self):        
        pygame.init()
        time = 0

        phases = {'A':8, 'B':8, 'C':8}

        for i in xrange(24):
            for key in phases.keys():
                if phases[key] == 0:
                    del phases[key]
            phase = random.choice(phases.keys())
            phases[phase] -= 1
            
            if(phase == 'A'):
                self.wait_screen("Starting phase A")
                time = self.phase_A(time)
            elif(phase == 'B'):
                self.wait_screen("Starting phase B")
                time = self.phase_B(time)
            else:
                self.wait_screen("Starting phase C")
                time = self.phase_C(time)
            
        print "Total time:", time
        self.file.close()
        self.wait_screen("Game over")
        pygame.quit()
        sys.exit()
        
        
game1 = Game()
game1.play()
