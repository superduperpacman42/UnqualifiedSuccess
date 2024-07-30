import pygame
import random
from Constants import *

class Person:

    def __init__(self, game, pos=[0,0], id=1, direction="B"):
        self.game = game
        id = random.randint(0, 1)
        if random.randint(0, 1) == 0:
            id += 6
        self.backImage = game.loadImage("Player"+str(id)+"B.png", 4)
        self.frontImage = game.loadImage("Player"+str(id)+"F.png", 4)
        self.rightImage = game.loadImage("Player"+str(id)+"R.png", 4)
        self.backSitImage = game.loadImage("Player"+str(id)+"BS.png", 1)
        self.rightSitImage = game.loadImage("Player"+str(id)+"RS.png", 1)
        self.pos = pos
        self.setDirection(direction)
        self.counter = 0
        self.moving = False
        self.right = True
        self.chat = None
        self.sitting = False
        self.score = 0
        self.checkedIn = False
        self.keywords = []
        self.interviewQuestion = 0.5
        self.freeze = False
        self.tempPos = [pos[0], pos[1]] # center of grid square
    
    def update(self, dt):
        # Move towards assigned coordinates
        for i in range(2):
            if self.tempPos[i] + dt*SPEED < self.pos[i]:
                self.tempPos[i] += dt*SPEED
            elif self.tempPos[i] - dt*SPEED > self.pos[i]:
                self.tempPos[i] -= dt*SPEED
            else:
                self.tempPos[i] = self.pos[i]
        if self.tempPos[0] != self.pos[0] or self.tempPos[1] != self.pos[1]:
            self.counter +=1.0/FRAME_DURATION
        # Draw sprite
        p0 = [self.tempPos[0]*GRID_SPACE+GRID_SPACE-5*SCALE, self.tempPos[1]*GRID_SPACE+GRID_SPACE-9*SCALE]
        if self.game.room2:
            p0 = [p0[0]+GRID_SPACE*2.5, p0[1]+GRID_SPACE*3.5]
        if self.game.fixed:
            p0[0] += -self.game.origin[0]-self.game.fixedOrigin[0]+GRID_X*GRID_SPACE/2
            p0[1] += -self.game.origin[1]-self.game.fixedOrigin[1]+GRID_Y*GRID_SPACE/2
        img = self.animation[int(self.counter)%4] # select frame
        if not self.right:
            img = pygame.transform.flip(img, 1, 0) # flip left/right
        self.game.screen.blit(img, p0)

    def move(self, dx, dy):
        if self.freeze:
            return
        if self.tempPos[0] != self.pos[0] or self.tempPos[1] != self.pos[1]:
            return
        g = self.game.grid[self.pos[1]+dy+1][self.pos[0]+dx+1]
        if g == "1" or g == "?": # wall
            if not self.sitting:
                self.turn(dx, dy)
        elif g == "*" : # desk
            self.moving = False
            self.turn(dx, dy)
            if not self.game.interviewStart:
                self.clearDialogue()
                self.checkedIn = True
                self.game.options += ["Continue"]
                self.game.playSound("Speech.wav")
                self.game.text += ["*Receptionist:","Welcome! Please take a *seat, we'll call you up for your interview shortly."]
                self.chat = "Desk"
        elif g == "^": # interview
            self.turn(dx, dy)
            if self.game.interviewStart:
                self.game.beginInterview()
                self.game.playSound("Door.wav")
        elif g == " ":
            self.moving = True
            self.right = True
            self.sitting = False
            if "wrong" in self.keywords and "quick-sort" in self.keywords and "bits" in self.keywords and \
                "Java" in self.keywords and not self.game.room2:
                self.game.interviewStart = True
                self.game.text = ["*Receptionist: it's time to begin your *interview. Please proceed to the interviewing room."]
                if not self.game.interviewStart:
                    self.game.playSound("Speech.wav")
            if dx > 0:
                self.pos[0] += 1
                self.animation = self.rightImage
            elif dx < 0:
                self.pos[0] -= 1
                self.animation = self.rightImage
                self.right = False
            elif dy > 0:
                self.pos[1] += 1
                self.animation = self.frontImage
            elif dy < 0:
                self.pos[1] -= 1
                self.animation = self.backImage
            self.checkPrompts()
        elif g == "%":
            self.setPos(self.pos[0]+dx, self.pos[1]+dy)
            self.sitting = True
            self.freeze = True
            self.clearDialogue()
            self.game.text += ["*VP:","Let's get started..."]
            self.game.playSound("Speech.wav")
            self.game.options += ["I'm ready."]
            self.setDirection("BS")
        else: # chair
            if g == "s" or g == "t":
                self.chat = g
                if g == "t":
                    self.clearDialogue()
                    self.game.text += [f"See why recruiters are looking for applicants that use {W['Java']}!"]
                    self.game.options += ["Done"]
                if g == "s":
                    self.clearDialogue()
                    self.game.text += [f"Breaking News: Researchers {W['factor']} a {W['polynomials']} using {W['recursion']}!"]
                    self.keywords += ["recursion"]
                    self.game.options += ["Done"]
            else:
                chair = self.game.getChair(g)
                if self.game.interviewStart:
                    self.turn(dx, dy)
                elif not chair.person:
                    self.moving = False
                    self.sitting = chair
                    self.checkPrompts()
                elif self.sitting:
                    chair.person.interact(option="Begin")
                    self.chat = chair.person
                else:
                    self.turn(dx, dy)

    def setDirection(self, direction):
        self.counter = 0
        self.right = True
        if direction == "F":
            self.animation = self.frontImage
        elif direction == "R":
            self.animation = self.rightImage
        elif direction == "RS":
            self.animation = self.rightSitImage
        elif direction == "L":
            self.animation = self.rightImage
            self.right = False
        elif direction == "LS":
            self.animation = self.rightSitImage
            self.right = False
        elif direction == "B":
            self.animation = self.backImage
        elif direction == "BS":
            self.animation = self.backSitImage

    def turn(self, dx, dy):
        self.counter = 0
        self.right = True
        if dy>0:
            self.animation = self.frontImage
        elif dx>0:
            self.animation = self.rightImage
        elif dy<0:
            self.animation = self.backImage
        elif dx<0:
            self.animation = self.rightImage
            self.right = False

    def checkPrompts(self):
        if self.sitting and not self.game.interviewStart:
            self.pos[0] = self.tempPos[0] = self.sitting.pos[0]-1
            self.pos[1] = self.tempPos[1] = self.sitting.pos[1]-1
            self.setDirection(self.sitting.direction)
            self.clearDialogue()
            for n in self.sitting.neighbors:
                if not n.person:
                    continue
                d = self.sitting.toChair(n)
                if n.person == "table": # reading material
                    s = "Read"
                elif self.checkedIn and (n.person.id == 6 or n.person.id == 7):
                    s = "Eavesdrop"
                else:
                    s = "Talk to *"+n.person.name
                if d[0] > 0:
                    self.game.text += ["@R"+s]
                elif d[0] < 0:
                    self.game.text += ["@L"+s]
                elif d[1] > 0:
                    self.game.text += ["@D"+s]
                else:
                    self.game.text += ["@U"+s]
        else:
            self.clearDialogue()
            if self.game.interviewStart and not self.game.room2:
                self.game.text = ["*Receptionist: it's time to begin your interview. Please proceed to the interviewing room."]
            up = self.game.grid[self.pos[1]+0][self.pos[0]+1]
            down = self.game.grid[self.pos[1]+2][self.pos[0]+1]
            left = self.game.grid[self.pos[1]+1][self.pos[0]+0]
            right = self.game.grid[self.pos[1]+1][self.pos[0]+2]
            if up == "*" and not self.game.interviewStart: # desk
                self.game.text += ["@UTalk to *Receptionist"]
            if up == "^": # interview
                if not self.game.interviewStart:
                    self.game.text += ["It's not yet your turn..."]
                else:
                    self.game.text = ["@UBegin interview"]
            if up == "?" and not self.game.interviewStart: # exit
                self.game.text += ["No admittance..."]
            if not self.game.interviewStart:
                if ord(up)-97>=0 and ord(up)-97<18 and not self.game.getChair(up).person:
                    self.game.text += ["@USit"]
                if ord(down)-97>=0 and ord(down)-97<18 and not self.game.getChair(down).person:
                    self.game.text += ["@DSit"]
                if ord(left)-97>=0 and ord(left)-97<18 and not self.game.getChair(left).person:
                    self.game.text += ["@LSit"]
                if ord(right)-97>=0 and ord(right)-97<18 and not self.game.getChair(right).person:
                    self.game.text += ["@RSit"]

    def setPos(self, x, y):
        self.pos[0] = self.tempPos[0] = x
        self.pos[1] = self.tempPos[1] = y

    def respond(self, option, index=0):
        if self.freeze:
            self.interview(option, index)
            return
        if option == "Done" or "(Done)" in option:
            self.clearDialogue()
            self.checkPrompts()
            self.game.playSound("Select.wav")
            if option == "Oh, good luck! (Done)":
                self.game.interviewCandidate(2)
            elif "leet" in self.keywords and "merge-sort" in self.keywords and "quick-sort" in self.keywords and "bits" in self.keywords:
                self.game.interviewCandidate(4)
        elif self.chat == "Desk":
            self.clearDialogue()
            self.game.text += ["*Receptionist:","Feel free to *talk with the other candidates as you wait."]
            self.game.playSound("Speech.wav")
            self.game.options += ["Done"]
        else:
            self.chat.interact(option, index)

    def clearDialogue(self):
        self.game.text = []
        self.game.options = []
        self.game.option = 0

    def inPosition(self):
        return self.tempPos[0] == self.pos[0] and self.tempPos[1] == self.pos[1]

    def vocab(self, words):
        for word in self.keywords:
            if word in words:
                self.game.options += [W[word].title()]
        if not len(self.game.options):
            self.game.options += ["Ummm..."]

    def jargon(self, exclude=[]):
        for word in self.keywords:
            if word in JARGON and not word in exclude:
                self.game.options += [W[word].title()]
        if not len(self.game.options):
            self.game.options += ["Ummm..."]

    def interview(self, option, index):
        self.clearDialogue()
        name = random.choice(["*CEO", "*VP", "*President"])
        self.interviewQuestion += 0.5
        self.game.text += [name]
        if self.interviewQuestion == 1:
            self.game.text += [f"So, what is your {W['language']} of choice?"]
            self.game.playSound("Speech.wav")
            self.jargon()
        elif self.interviewQuestion == 1.5:
            if option.lower() == W["Java"].lower():
                self.game.playSound("Select.wav")
                self.game.text += [f"Ah, perfect! We are looking to hire a {W['Java']} {W['developer']}."]
                self.game.playSound("Select.wav")
                self.score += 1
            elif option.lower() == W["Python"].lower():
                self.game.text += ["Hm, not quite what we were hoping for, but it'll do."]
                self.game.playSound("Wrong.wav")
            else:
                self.game.text += [f"Thats...not actually a {W['language']}? Are you even paying attention?"]
                self.game.playSound("Wrong.wav")
                self.score -= 1
        elif self.interviewQuestion == 2:
            self.game.playSound("Speech.wav")
            self.game.text += ["Ok, let's learn a little about you. What one word would you use to describe yourself?"]
            self.jargon()
        elif self.interviewQuestion == 2.5:
            if option.lower() == W["leet"].lower():
                self.game.text += [f"Wow, that's exactly the quality we look for the most in our employees!"]
                self.game.playSound("Select.wav")
                self.score += 1
            else:
                self.game.text += [f"That's...an interesting description to apply to a human? Moving on..."]
                self.game.playSound("Wrong.wav")
                self.score -= 1
        if self.interviewQuestion == 3:
            self.game.playSound("Speech.wav")
            self.game.text += [f"Now, let's get more technical. What's the {W['fastest']} way to {W['sort']} a {W['list']}?"]
            self.jargon()
        if self.interviewQuestion == 3.5:
            if option.lower() == W["quick-sort"].lower():
                self.game.text += [f"Spot on!"]
                self.game.playSound("Select.wav")
                self.score += 1
            elif option.lower() == W["merge-sort"].lower():
                self.game.text += [f"Hm, that's not quite the {W['fastest']} option, but I guess it gets the job done."]
                self.game.playSound("Wrong.wav")
            else:
                self.game.text += [f"That doesn't even make sense..."]
                self.game.playSound("Wrong.wav")
                self.score -= 1
        elif self.interviewQuestion == 4:
            self.game.playSound("Speech.wav")
            self.game.text += [f"Let's make this a bit harder. How many {W['bits']} are in a {W['byte']}?"]
            self.game.options += ['2','3','4','5','6','7','8']
        elif self.interviewQuestion == 4.5:
            if option == str(BITS_PER_BYTE):
                self.game.text += [f"Correct!"]
                self.game.playSound("Select.wav")
                self.score += 1
            else:
                self.game.text += [f"I'm afraid that's incorrect."]
                self.game.playSound("Wrong.wav")
                self.score -= 1
        elif self.interviewQuestion == 5:
            self.game.playSound("Speech.wav")
            self.game.text += [f"For which metric would {W['Python']} be a superior {W['language']} to {W['Java']}?"]
            self.vocab(["efficiency", "speed", "performance"])
        elif self.interviewQuestion == 5.5:
            if option.lower() == W["efficiency"].lower():
                self.game.playSound("Select.wav")
                self.game.text += [f"Exactly!"]
                self.score += 1
            elif option == "Ummm...":
                self.game.text += [f"This doesn't seem like your area of expertise..."]
                self.game.playSound("Wrong.wav")
                self.score -= 1
            else:
                self.game.text += [f"Actually, {W['Python']} is much worse in that regard."]
                self.game.playSound("Wrong.wav")
                self.score -= 1
        elif self.interviewQuestion == 6:
            self.game.playSound("Speech.wav")
            self.game.text += [f"All right, next question. How would you go about trying to {W['factor']} a {W['polynomials']}?"]
            self.jargon()
        elif self.interviewQuestion == 6.5:
            if option.lower() == W["recursion"].lower():
                self.game.text += [f"Good answer!"]
                self.game.playSound("Select.wav")
                self.score += 1
            else:
                self.game.text += [f"Um, I don't think that a {W['polynomials']} works like that..."]
                self.game.playSound("Wrong.wav")
                self.score -= 1
        elif self.interviewQuestion == 7:
            self.game.playSound("Speech.wav")
            self.game.text += [f"Well then, do you have any questions for us?"]
            self.game.options += ["Not at the moment."]
            if "cloud" in self.keywords:
                self.game.options += [f"How do you fund your {W['cloud']} operations?"]
        elif self.interviewQuestion == 7.5:
            if index == 0:
                self.game.playSound("Speech.wav")
                self.game.text += ["Very good."]
                self.interviewQuestion = 9.5
            else:
                self.game.playSound("Speech.wav")
                self.game.text += [f"Our {W['cloud']} operations!? Wait a minute, did someone tell you to ask about that?"]
                self.game.options += ["Um, I don't know what you're talking about...", "I met an undercover agent in the waiting room."]
        elif self.interviewQuestion == 8:
            if index == 0:
                self.game.playSound("Wrong.wav")
                self.game.text += ["Hm, well let's keep it that way."]
            else:
                self.game.text += ["Aha, thank your for that information! Your loyalty is greatly appreciated..."]
                self.game.playSound("Select.wav")
                self.score += 1
            self.interviewQuestion = 9.5
        elif self.interviewQuestion == 10:
            self.game.playSound("Speech.wav")
            self.game.text += ["Well then, that concludes our interview."]
        elif self.interviewQuestion == 10.5:
            self.game.playSound("Speech.wav")
            if self.score >= 3:
                self.game.text += ["Congratulations, we are delighted to offer you a job at our company!"]
                self.game.options += ["Accept the job!"]
            else:
                self.game.text += ["We are very sorry, but it seems you are underqualified for this position."]
                self.game.playSound("Speech.wav")
                self.game.options += ["Time to resume the job search..."]
        elif self.interviewQuestion == 11:
            self.game.shouldReset = True
            self.game.lost = self.score < 3
            if self.game.lost:
                self.game.playSound("Wrong.wav")
            else:
                self.game.playSound("Select.wav")
            return

        if not len(self.game.options):
            self.game.options += ["Continue"]
        print(self.score)
