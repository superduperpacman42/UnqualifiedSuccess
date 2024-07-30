from Person import Person
import pygame
import random
from Constants import *


class Candidate(Person):
    def __init__(self, game, id=1):
        self.id = id
        self.name = NAMES[self.id]
        id = random.randint(2, 3)
        if self.name in FEMALE:
            id += 2
        self.game = game
        self.backImage = game.loadImage("Player"+str(id)+"B.png", 4)
        self.frontImage = game.loadImage("Player"+str(id)+"F.png", 4)
        self.rightImage = game.loadImage("Player"+str(id)+"R.png", 4)
        self.backSitImage = game.loadImage("Player"+str(id)+"BS.png", 1)
        self.rightSitImage = game.loadImage("Player"+str(id)+"RS.png", 1)
        self.counter = 0
        self.right = True
        self.sitting = False
        self.pos=[0,0]
        self.gone = False
        self.permanentState = 0
        self.tempPos=[0,0]
        self.selections = []
        self.state = 0

    def interact(self, option=None, index=0):
        self.game.playSound("Speech.wav")
        g = self.game
        p = self.game.player
        self.clearDialogue()
        g.text += ["*"+self.name+":"]
        if not p.checkedIn:
            g.text += ["Make sure to check in at the front desk!"]
            g.options += ["Done"]
            return
        if option=="Begin":
            self.state = 0
            self.selections = []
        else:
            self.selections.append(index)
            self.state += 1
        if self.id == -1:
            if self.state == 0:
                g.text += ["How's it going?"]
                g.options += ["Great!","Good.","Pretty bad..."]
            elif self.state == 1:
                if option == "Great!":
                    g.text += ["Nice, glad to hear it!"]
                elif option == "Good.":
                    g.text += ["That's good."]
                elif option == "Pretty bad...":
                    g.text += ["Oof."]

# Insecure ###############################################################################################
        if self.id == 0:
            if self.state == 0:
                g.text += ["I hate interviews, they make me so nervous..."]
                g.options += ["You've got this!","Yeah, I've heard these interviewers are really harsh."]
            elif self.state == 1:
                if index == 0:
                    g.text += ["I don't know...I always forget everything under pressure."]
                    g.options += ["I can help you review if you'd like..."]
                elif index == 1:
                    g.text += ["Oh no, that's awful news! Why did you have to tell me that!? AAAAHHHHHHHH!!!"]
            elif self.state == 2:
                g.text += ["Oh, thank you! That would be really helpful. Ok, ask me a question."]
                if "sort" in p.keywords:
                    g.options += ["What's the "+W["fastest"]+" way to "+W["sort"]+" a "+W["list"]+"?"]
                if "datatype" in p.keywords:
                    g.options += [f"Which {W['datatype']} is the {W['biggest']}?"]
                if not len(g.options):
                    g.options += ["Ummm..."]
            elif self.state == 3:
                if option == "Ummm...":
                    g.text += ["Well this is useless. I'm going to fail this interview, I can already tell!"]
                elif option == "What's the "+W["fastest"]+" way to "+W["sort"]+" a "+W["list"]+"?":
                    g.text += ["Um...I think it would be "+W["quick-sort"] + " right?"]
                    p.keywords += ["quick-sort"]
                    g.options += ["Yep, nice job!", "I think that's incorrect..."]
                elif option == f"Which {W['datatype']} is the {W['biggest']}?":
                    g.text += [f"I think it was either {W['float']} or {W['integer']}, right?"]
                    p.keywords += [f"float", "integer"]
                    g.options += [f"Yep, it's {W['float']}.", f"Yep, it's {W['integer']}."]
            elif self.state == 4:
                if option[:3] == "Yep":
                    g.text += ["Well, if you say so... Thanks for your help!"]
                elif index == 0:
                    g.text += ["Awesome, I feel a lot better now!"]
                elif index == 1:
                    g.text += ["Really? I could have sworn that was it... I just know I'm going to fail this interview!"]

# Pompous ###############################################################################################
            
        if self.id == 4:
            if self.state == 0:
                g.text += ["You might as well go home now, I've got this interview in the bag."]
                g.options += ["Wow, you must be really qualified for this job!", "Nah, I think you're just overconfident."]
            elif self.state == 1:
                if index == 0:
                    g.text += ["Yeah, I'm as "+W["leet"]+ " as it gets! They'll all be begging me to take the job."]
                    p.keywords += ["leet", "smart", "innovative"]
                    g.options += ["Wow, that sounds like a really useful trait to have. (Done)"]
                elif index == 1:
                    g.text += ["Oh yeah? Watch this. Ask me the "+W["fastest"]+" way to "+W["sort"]+" a "+W["list"]+"."]
                    p.keywords += ["sort"]
                    g.options += ["Ok, what's the..."]
            elif self.state == 2:
                g.text += ["It's "+W["merge-sort"]+"! See, I'm just so prepared."]
                p.keywords += ["merge-sort"]
                g.options += ["Wow, I stand corrected. (Done)"]

# Hurried ###############################################################################################
            
        if self.id == 2:
            if self.state == 0:
                g.text += ["Sorry, but I don't have time to talk now. They're going to call my name any minute!"]
                g.options += ["Oh, good luck! (Done)"]

# Judgemental ###########################################################################################
            
        if self.id == 3:
            if self.state == 0:
                g.text += [f"Finally, I thought *{g.candidates[4].name} would never leave."]
                g.options += [f"Why don't you like *{g.candidates[4].name}?", f"Yeah, *{g.candidates[4].name} was really arrogant."]
            if self.state == 1:
                if index == 0:
                    if g.candidates[4].name in MALE:
                        g.text += ["He was just so arrogant, despite not having a clue what he was talking about."]
                    else:
                        g.text += ["She was just so arrogant, despite not having a clue what she was talking about."]
                    g.options += ["Oh, really?"]
                else:
                    if g.candidates[4].name in MALE:
                        g.text += [f"Tell me about it! Did he mention how {W['leet']} he was to you too? Such a liar..."]
                    else:
                        g.text += [f"Tell me about it! Did she mention how {W['leet']} she was to you too? Such a liar..."]
            if self.state == 2:
                if g.candidates[4].name in MALE:
                    g.text += ["Yeah, he couldn't "+W["sort"]+" a "+W["list"]+" if it fell on him."]
                else:
                    g.text += ["Yeah, she couldn't "+W["sort"]+" a "+W["list"]+" if it fell on her."]
                p.keywords += ["wrong"]

# Studious ###############################################################################################
            
        if self.id == 5:
            if self.state == 0:
                g.text += ["Please leave me alone, I'm busy studying for this interview."]
                g.options += ["Sorry, I'll move. (Done)"]
                if not "byte" in p.keywords:
                    g.options += ["No worries, I'll be quiet."]
            elif self.state == 1:
                g.text += [f"Hey, do you remember which {W['datatype']} is the {W['biggest']}?"]
                p.keywords += ["datatype"]
                self.jargon(["datatype"])
            elif self.state == 2:
                if option == W['integer'].title():
                    g.text += ["Hm, I don't think that's right..."]
                elif option == W['float'].title():
                    g.text += [f"Oh yeah, of course because a {W['byte']} contains {BITS_PER_BYTE} {W['bits']}!"]
                    p.keywords += ["bits","byte"]
                else:
                    g.text += ["You have no idea what you're talking about, do you?"]

# Arguers ###############################################################################################
            
        if self.id == 6:
            if self.state%2:
                g.text[0] = "*"+NAMES[self.id+1]+":"
            g.options += ["Continue listening", "Leave (Done)"]
            if self.state == 0:
                g.text += [f"{W['Python']} is just so much better than {W['Java']}!"]
                p.keywords += ["Python", "Java"]
            elif self.state == 1:
                g.text += [f"You're crazy! {W['Java']} has such better {W['speed']}!"]
                p.keywords += ["speed"]
            elif self.state == 2:
                g.text += [f"Sure, but you're ignoring {W['efficiency']}. There's a reason it's so much more popular!"]
                p.keywords += ["efficiency"]
                g.options = []

        if self.id == 7:
            if self.state%2:
                g.text[0] = "*"+NAMES[self.id-11]+":"
            g.options += ["Continue listening", "Leave (Done)"]
            if self.state == 0:
                g.text += [f"{W['Java']} is just so much better than {W['Python']}!"]
                p.keywords += ["Python", "Java"]
            elif self.state == 1:
                g.text += [f"You're crazy! {W['Python']} has such better {W['efficiency']}!"]
                p.keywords += ["efficiency"]
            elif self.state == 2:
                g.text += [f"Sure, but you're ignoring {W['performance']}. There's a reason people are switching over!"]
                p.keywords += ["performance"]
                g.options = []

# Suspicious ###############################################################################################
            
        if self.id == 1:
            if self.state == 0:
                if "compiler" in p.keywords:
                    g.text += ["I'm not telling you nothing."]
                else:
                    g.text += ["Hey there, good luck with the interview!"]
                    g.options += ["Thanks, you too! (Done)"]
                    if "sort" in p.keywords:
                        g.options += ["Quick question: what's the "+W["fastest"]+" way to "+W["sort"]+" a "+W["list"]+"?"]
                    if "datatype" in p.keywords:
                        g.options += [f"Hey, do you remember which {W['datatype']} is the {W['biggest']}?"]
            elif self.state == 1:
                g.text += [f"Hmm. Let me ask you something first. What's your favorite {W['compiler']}?"]
                p.keywords += ["compiler"]
                self.game.options += ["Ummm..."]
                self.jargon(["datatype"])
            elif self.state == 2:
                if option == "Ummm...":
                    g.text += ["I knew it, you know nothing about this job, do you?"]
                else:
                    g.text += [f"That's not a {W['compiler']}! I knew it, you know nothing about this job, do you?"]
                g.options += ["Uh, what do you mean...?"]
            elif self.state == 3:
                g.text += [f"Any real {W['developer']} would have a favorite {W['compiler']}! You're a fake!"]
                g.options += ["Oh, well, um...Look at the time! Gotta go, bye. (Done)"]

# Secretive ###############################################################################################
            
        if self.id == 8:
            if self.state == 0:
                if "cloud" in p.keywords:
                    g.text += ["Shhhhh..."]
                elif self.permanentState == 1:
                    g.text += ["Are you ready to keep a secret?"]
                    g.options += ["You have my word of honor.", "Nope."]
                    self.state = 3
                elif self.permanentState == 2:
                    g.text += ["Have you reconsidered my request?"]
                    g.options += ["I am willing.", "The answer is still no."]
                    self.state = 6
                else:
                    g.text += ["Oh, hey."]
                    g.options += ["How's it going?", "Are you also interviewing for the job?"]
            elif self.state == 1:
                if index == 0:
                    g.text += ["Good. How about you?"]
                    g.options += ["Good.", "Not bad.", "Could be worse."]
                else:
                    g.text += ["Yep."]
                    g.options += ["Cool. (Done)"]
                    if "sort" in p.keywords:
                        g.options += ["Quick question: what's the "+W["fastest"]+" way to "+W["sort"]+" a "+W["list"]+"?"]
                    if "datatype" in p.keywords:
                        g.options += [f"Hey, do you remember which {W['datatype']} is the {W['biggest']}?"]
                    if "compiler" in p.keywords:
                        g.options += [f"By the way, what's your favorite {W['compiler']}?"]
            elif self.state == 2:
                if option in ["Good.", "Not bad.", "Could be worse."]:
                    g.text += ["Well, glad to hear it."]
                elif option[:3] == "Hey":
                    g.text += ["Hm...not off the top of my head, sorry."]
                    g.options += ["Ok, no problem. (Done)"]
                elif option[:3] == "Qui":
                    g.text += ["Uh...sorry, I seem to have forgotten."]
                    g.options += ["Ok, no problem. (Done)"]
                elif option[:3] == "By ":
                    g.text += ["Um...I don't have one."]
                    g.options += ["Ok, no problem. (Done)", f"Wait a minute, every real {W['developer']} has a favorite {W['compiler']}!"]
            elif self.state == 3:
                g.text += ["Shoot! Um, ok, can you keep a secret for me?"]
                g.options += ["You have my word of honor.", "Nope."]
                self.permanentState = 1
            elif self.state == 4:
                if index == 0:
                    g.text += ["I'm not actually an applicant, I am an undercover agent!"]
                    g.options += ["Whoa! Why are you here?"]
                else:
                    g.text += ["Well then, I have nothing more to say."]
            elif self.state == 5:
                g.text += [f"The company may be embezzling money through their {W['cloud']} operations."]
                g.options = ["Yikes!", "That's terrible!"]
            elif self.state == 6:
                g.text += ["Say, could you do me a favor?"]
                g.options += ["Of course.", "No, I'd rather stay out of this."]
                self.permanentState = 2
            elif self.state == 7:
                if index == 0:
                    g.text += [f"During your interview, ask them how they fund their {W['cloud']} operations."]
                    g.options += ["I will do my best."]
                    p.keywords += ["cloud"]
                else:
                    g.text += ["I understand. This is my duty, not yours."]
            elif self.state == 8:
                g.text += ["Thank you for your cooperation."]


##########################################################################################################
        if not len(g.options):
            g.options += ["Done"]
        p.keywords = list(set(p.keywords))

    def jargon(self, exclude=[]):
        for word in self.game.player.keywords:
            if word in JARGON and not word in exclude:
                self.game.options += [W[word].title()]
        if not len(self.game.options):
            self.game.options += ["Ummm..."]