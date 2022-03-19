from tracemalloc import start
import pygame
import math

class Environment:
    def __init__(self):
        
        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.TURQUISE = (64,224,208)
        self.ORANGE = (255,165,0)
        self.GREY = (150,150,150) 

        pygame.display.set_caption("Environment")

        self.screen = pygame.display.set_mode([500, 500])
        self.screen.fill(self.WHITE)

        self.trail_set = []
        self.car_x = 0
        self.car_y = 0
        self.robot_x = 0
        self.robot_y = 0

    def add_obstacle(self):
        self.center_obs = pygame.Rect(225, 200, 80, 80)
        pygame.draw.rect(self.screen, self.BLACK, self.center_obs)
        self.left_obs = pygame.Rect(10, 430, 120, 60)
        pygame.draw.rect(self.screen, self.BLACK, self.left_obs)
        self.right_obs = pygame.Rect(280, 430, 120, 60)
        pygame.draw.rect(self.screen, self.BLACK, self.right_obs)

    def update_environment(self):
        self.add_obstacle()
           
            

    def trail(self, pos):
        for i in range(0, len(self.trail_set)-1):
            pygame.draw.line(self.screen, self.RED, (self.trail_set[i][0], self.trail_set[i][1]),
                                                (self.trail_set[i+1][0], self.trail_set[i+1][1]))
        if self.trail_set.__sizeof__()>30000:
            self.trail_set.pop(0)
        self.trail_set.append(pos)

    
    def add_car(self, car_x=10, car_y=10):
        self.car_x += car_x
        self.car_y += car_y
        self.car = pygame.Rect(car_x, car_y, 80, 50)
        pygame.draw.rect(self.screen, self.ORANGE, self.car)
    
    def add_robot(self, robot_x=10, robot_y=10):
        # self.robot_x += robot_x
        # self.robot_y += robot_y
        self.robot = pygame.Rect(self.robot_x, self.robot_y, 50, 50)
        pygame.draw.rect(self.screen, self.ORANGE, self.robot)
    

class Robot:
    def __init__(self, robot_x=10, robot_y=10):
        self.w = 80
        self.x = robot_x
        self.y = robot_y
        self.theta = 0

        self.m2p = 3779.52 # meters to pixels
        self.vl = 0.01 * self.m2p
        self.vr = 0.01 * self.m2p
        self.minspeed = -0.02 * self.m2p
        self.maxspeed = 0.02 * self.m2p

        #graphics of robot
        robotImg = "robot.png"
        self.img = pygame.image.load(robotImg)
        self.rotated = self.img
        self.rect = self.rotated.get_rect(center=(self.x, self.y))    
    
    def draw(self, map):
        map.blit(self.rotated, self.rect)

    def move(self, event=None):
        if event is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.vl+=0.001*self.m2p
    
        self.x +=((self.vl+self.vr)/2) * math.cos(self.theta) * dt
        self.y +=((self.vl+self.vr)/2) * math.cos(self.theta) * dt
        #self.theta = 0
        self.theta += (self.vr - self.vl)/self.w * dt
        #reset theta
        if self.theta>2*math.pi or self.theta<-2*math.pi:
            self.theta = 0
        #set max speed
        self.vr = min(self.vr, self.maxspeed)
        self.vl = min(self.vl, self.maxspeed)
        #set min speed
        self.vr = max(self.vr, self.minspeed)
        self.vl = max(self.vl, self.minspeed)
        

        self.rotated = pygame.transform.rotozoom(self.img, math.degrees(self.theta), 1)
        self.rect = self.rotated.get_rect(center=(self.x,self.y))

    

## initialise pygame
pygame.init()


running = True

e = Environment()    

robot = Robot(50, 50)

dt = 0
lasttime = pygame.time.get_ticks()
#simulation loop
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running == False
        robot.move(event)
    #e.add_robot()
    dt = (pygame.time.get_ticks() - lasttime)/1000
    lasttime = pygame.time.get_ticks()
    
    pygame.display.update()
    
    e.screen.fill(e.WHITE)
    e.add_obstacle()
    
    robot.move()
    e.trail((robot.x, robot.y))
    robot.draw(e.screen)
    
    
    
#e.add_robot()
#e.update_environment()

#pygame.quit()