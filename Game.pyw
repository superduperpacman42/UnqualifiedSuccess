import pygame
from PIL import Image
import os, sys, math, random
from Person import Person
from Chair import Chair
from Candidate import Candidate
from Constants import *

exe = 0

class Game:

    def reset(self):
        ''' Resets the game from the beginning '''
        randomize()
        self.origin = [0,0]
        self.player = Person(self, [6, 11], id=1)
        self.text = []
        self.font = pygame.font.SysFont("arial", FONT_SIZE)
        self.fontBold = pygame.font.SysFont("arial_bold", FONT_SIZE+6)
        self.options = []
        self.option = 0
        self.frozen = False
        self.sounds = {}
        self.splash = True
        self.pauseTime = 0
        self.room2 = False
        self.shouldReset = False
        self.initCandidates()
        # self.secretary = Person(self, [6, 1], direction="F")
        self.initChairs()
        self.fixed = False
        self.interviewStart = False
        self.fixedOrigin = (0,0)
        self.grid = ["11?11111111^11",
                     "11  1    1  11",
                     "1   1    1   1",
                     "1a  111*11  r1",
                     "1b          q1",
                     "1            1",
                     "1            1",
                     "1            1",
                     "1c          p1",
                     "1d          o1",
                     "1e          n1",
                     "1f          m1",
                     "1sghi    jklt1",
                     "11111111111111"]
        self.grid2 = ["111111111",
                      "1 11111 1",
                      "1 11111 1",
                      "1   %   1",
                      "1       1",
                      "1       1",
                      "111111111"]
    
    def update(self, dt, keys):
        ''' Updates the game by a timestep and redraws graphics '''
        if dt>100: # timeout
            return
        if self.shouldReset:
            self.reset()
            return

        if self.frozen:
            if self.frozen.inPosition():
                if self.frozen.pos[1] == 0:
                    self.frozen.setPos(0, -5)
                    self.frozen.gone = True
                    self.frozen = None
                    self.playSound("Door.wav")
                    self.player.checkPrompts()
                elif self.frozen.pos[0] == 10:
                    self.frozen.pos[1] = 0
                    self.frozen.turn(0, -1)
                else:
                    self.frozen.pos[0] = 10
                    if self.frozen.pos[0] > 10:
                        self.frozen.turn(-1,0)
                    else:
                        self.frozen.turn(1,0)
                self.pauseTime = 200

        # Held button input
        if not self.player.sitting and not len(self.options) and self.player.moving and not self.frozen:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.player.move(0, -1)
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.move(1, 0)
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.move(-1, 0)
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.player.move(0, 1)
            else:
                if self.player.inPosition():
                    self.player.counter = 0

        # Graphics
        # self.origin[0]-=move[0]
        # self.origin[1]-=move[1]
        if self.splash:
            if pygame.time.get_ticks()%800 > 300:
                if self.lost:
                    self.screen.blit(self.splashScreenLose, (-15,-35))
                else:
                    self.screen.blit(self.splashScreen, (-15,-35))
            else:
                if self.lost:
                    self.screen.blit(self.splashScreenLose2, (-15,-35))
                else:
                    self.screen.blit(self.splashScreen2, (-15,-35))
        elif self.room2:
            self.screen.blit(self.background2, (0,0))
        else:
            self.screen.blit(self.background, (0,0))
        for i, text in enumerate(self.text):
            self.drawDialogue(text, i)

        # Draw text options
        line = 5
        for i, option in enumerate(self.options):
            line = self.drawOption(option, line, self.option==i) + 1.5
        if not self.splash:
            self.player.update(dt)

        # self.secretary.update(dt)
        if not self.room2 and not self.splash:
            for candidate in self.candidates:
                candidate.update(dt)
        if self.fixed:
            subscreen = (self.origin[0]+self.fixedOrigin[0]-WIDTH/2,
                         self.origin[1]+self.fixedOrigin[1]-HEIGHT/2,
                         WIDTH, HEIGHT)
            self.screen.blit(self.screen, (0,0), subscreen)
        if self.pauseTime > 0:
            pygame.time.wait(self.pauseTime)
            self.pauseTime = 0

    def keyPressed(self, key):
        ''' Respond to a key press event '''
        if self.splash:
            self.splash = False
            self.playSound("Door.wav")
            return
        if self.frozen:
            return
        if len(self.options):
            if key==pygame.K_UP or key==pygame.K_w:
                # if(len(self.options)==1):
                #     self.player.respond(self.options[self.option])
                # else:
                self.option -=1
                self.option %= len(self.options)
                self.playSound("Toggle.wav")
            if key==pygame.K_RIGHT or key==pygame.K_d or key==pygame.K_RETURN:
                self.player.respond(self.options[self.option], self.option)
            elif key==pygame.K_LEFT or key==pygame.K_a:
                # self.player.clearDialogue()
                # self.player.checkPrompts()
                pass
            elif key==pygame.K_DOWN or key==pygame.K_s:
                # if(len(self.options)==1):
                #     self.player.respond(self.options[self.option])
                # else:
                self.option +=1
                self.option %= len(self.options)
                self.playSound("Toggle.wav")
            return
        if key==pygame.K_UP or key==pygame.K_w:
            self.player.move(0, -1)
        if key==pygame.K_RIGHT or key==pygame.K_d:
            self.player.move(1, 0)
        elif key==pygame.K_LEFT or key==pygame.K_a:
            self.player.move(-1, 0)
        elif key==pygame.K_DOWN or key==pygame.K_s:
            self.player.move(0, 1)

    def initCandidates(self):
        self.candidates = []
        for i in range(9):
            self.candidates.append(Candidate(self, i))

    def getChair(self, letter):
        return self.chairs[ord(letter)-97]

    def initChairs(self):
        self.chairs = []
        self.chairs.append(Chair((1,3), None, None)) #a
        self.chairs.append(Chair((1,4), self.candidates[0], self.getChair('a')))

        self.chairs.append(Chair((1,8), None, None)) #c
        self.chairs.append(Chair((1,9), self.candidates[1], self.getChair('c')))
        self.chairs.append(Chair((1,10), None, self.getChair('d')))
        self.chairs.append(Chair((1,11), self.candidates[2], self.getChair('e')))

        self.chairs.append(Chair((2,12), self.candidates[3], None)) #g
        self.chairs.append(Chair((3,12), self.candidates[4], self.getChair('g')))
        self.chairs.append(Chair((4,12), None, self.getChair('h')))
        
        self.chairs.append(Chair((9,12), None, None)) #j
        self.chairs.append(Chair((10,12), None, self.getChair('j')))
        self.chairs.append(Chair((11,12), self.candidates[5], self.getChair('k')))
        
        self.chairs.append(Chair((12,11), None, None)) #m
        self.chairs.append(Chair((12,10), self.candidates[6], self.getChair('m')))
        self.chairs.append(Chair((12,9), self.candidates[7], self.getChair('n')))
        self.chairs.append(Chair((12,8), None, self.getChair('o')))

        self.chairs.append(Chair((12,4), None, None)) #q
        self.chairs.append(Chair((12,3), self.candidates[8], self.getChair('q')))
        

        self.chairs.append(Chair((12,12), "table", self.getChair('l')))
        self.getChair('m').addNeighbor(self.chairs[-1])

        self.chairs.append(Chair((1,12), "table", self.getChair('f')))
        self.getChair('g').addNeighbor(self.chairs[-1])


    def drawDialogue(self, chars, line):
        if(chars[0]=="@"):
            if(chars[1]=="U"):
                self.screen.blit(self.upArrow, (560+8,10+FONT_SIZE*line))
            elif(chars[1]=="D"):
                self.screen.blit(self.downArrow, (560+8,10+FONT_SIZE*line))
            if(chars[1]=="L"):
                self.screen.blit(self.leftArrow, (560+8,10+FONT_SIZE*line))
            elif(chars[1]=="R"):
                self.screen.blit(self.rightArrow, (560+8,10+FONT_SIZE*line))
            self.drawText(chars[2:], 20, line)
        else:
            self.drawText(chars, 0, line)

    def drawOption(self, chars, line, selected=False):
        if selected:
            self.screen.blit(self.rightArrow, (560+8,10+FONT_SIZE*line))
        return self.drawText(chars, 0, line, 20)

    def drawText(self, chars, x, line, x0=0):
        while(len(chars)):
            i = chars.find(" ")
            if i>=0:
                if chars[0] == "*":
                    self.caption = self.fontBold.render(chars[1:i+1], True, (0,0,0))
                    yoffset = 16
                else:
                    self.caption = self.font.render(chars[:i+1], True, (0,0,0))
                    yoffset = 10
                if x+self.caption.get_width()+x0 > 275:
                    x = 0
                    line += 1
                self.screen.blit(self.caption, (560+15+x+x0,yoffset+FONT_SIZE*line))
                x += self.caption.get_width()
                chars = chars[i+1:]
            else:
                if chars[0] == "*":
                    self.caption = self.fontBold.render(chars[1:], True, (0,0,0))
                    yoffset = 16
                else:
                    self.caption = self.font.render(chars, True, (0,0,0))
                    yoffset = 10
                if x+self.caption.get_width()+x0 > 275:
                    x = 0
                    line += 1
                self.screen.blit(self.caption, (560+15+x+x0,yoffset+FONT_SIZE*line))
                break
        return line

    def interviewCandidate(self, i=2):
        p = self.candidates[i]
        if p.gone:
            p = None
            return
        self.frozen = p
        self.player.clearDialogue()
        self.text = ["*Receptionist:", p.name+", they're ready for you."]
        for chair in self.chairs:
            if chair.person == p:
                chair.person = None
        if p.pos[1] >= 11:
            p.pos[1] = 10
            p.turn(0, -1)
        elif p.pos[0] > 10:
            p.pos[0] = 10
            p.turn(-1,0)
        else:
            p.pos[0] = 1
            p.turn(1,0)

    def beginInterview(self):
        self.room2 = True
        self.grid = self.grid2
        self.player.setPos(3,4)
        self.player.sitting = True
        self.player.clearDialogue()
        self.text += ["*CEO:","Thank you for joining us. Please, take a seat."]
        
################################################################################
    
    def __init__(self, name):
        ''' Initialize the game '''
        pygame.init()
        pygame.display.set_caption(name)
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.background = self.loadImage("Room.png")
        self.background2 = self.loadImage("InterviewRoom.png")
        self.splashScreen = self.loadImage("SplashScreen.png",scale=1.5)
        self.splashScreen2 = self.loadImage("SplashScreen1.png",scale=1.5)
        self.splashScreenLose = self.loadImage("SplashScreen2.png",scale=1.5)
        self.splashScreenLose2 = self.loadImage("SplashScreen3.png",scale=1.5)
        self.lost = False
        self.rightArrow = self.loadImage("Arrow.png")
        self.leftArrow = pygame.transform.flip(self.rightArrow, 1, 0) # flip left/right
        self.upArrow = self.loadImage("ArrowUp.png")
        self.downArrow = pygame.transform.flip(self.upArrow, 0, 1) # flip left/right
        self.playMusic("WaitingRoom.wav")

        self.reset()
        self.run()

    def run(self):
        ''' Iteratively call update '''
        clock = pygame.time.Clock()
        self.pause = False
        while not self.pause:
            for event in pygame.event.get():
                if event.type is pygame.KEYDOWN:
                    self.keyPressed(event.key)
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
            dt = clock.tick(TIME_STEP)
            self.update(dt, pygame.key.get_pressed())
            pygame.display.update()
    
    def loadImage(self, name, number=0, scale=1):
        ''' Loads an image or list of images '''
        if not hasattr(self, "images"):
            self.images = {}
        elif name in self.images:
            return self.images[name]
        if exe:
            path = os.path.join(os.path.dirname(sys.executable), 'images')
        else:
            path = os.path.join(os.path.dirname(__file__), 'images')
        if number==0:
            img = pygame.image.load(os.path.join(path, name))
            img = pygame.transform.scale(img, (int(SCALE*scale*img.get_width()),int(SCALE*scale*img.get_height())))
        else:
            img = []
            for i in range(number):
                key = name[:-4]+str(i)+name[-4:]
                img.append(pygame.image.load(os.path.join(path, key)))
                img[-1] = pygame.transform.scale(img[-1], (SCALE*img[-1].get_width(),SCALE*img[-1].get_height()))
        self.images[name] = img
        return img

    def playMusic(self, name):
        ''' Plays the given background track '''
        if exe:
            path = os.path.join(os.path.dirname(sys.executable), 'audio')
        else:
            path = os.path.join(os.path.dirname(__file__), 'audio')
        pygame.mixer.music.load(os.path.join(path, name))
        pygame.mixer.music.play(-1)
        
    def playSound(self, name):
        ''' Plays the given sound effect ''' 
        if name in self.sounds:
            self.sounds[name].play()
            return
        if exe:
            path = os.path.join(os.path.dirname(sys.executable), 'audio')
        else:
            path = os.path.join(os.path.dirname(__file__), 'audio')
        sound = pygame.mixer.Sound(os.path.join(path, name))
        self.sounds[name] = sound
        sound.play()

if __name__ == '__main__':
    game = Game("Unqualified Success")
