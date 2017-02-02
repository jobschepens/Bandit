#Lukas Nagel - lnagel@mpib-berlin.mpg.de

# from psychopy import gui
# from psychopy import parallel
# import fnmatch
# import os
# from __future__ import division
import pygame
import time
import random
import datetime
import numpy as np
# import textwrap
# import os
import glob
from extras import *
# import os.path
from matplotlib import pyplot as plt

def exit_handler(): 
    raise Exception("exit()")
    get_ipython().ask_exit = exit_handler

def f(): 
    raise Exception("Found exit()")

class parameters():
    """An object containing parameters and values throughout the experiment. Basically unnecessary (could also use a dictionary), 
    but keeps things nicely organised, and you only have to pass one variable into functions"""
    def __init__(self,participant):
        # INIT SCREEN        
        self.participant = participant
        s = pygame.display.Info() # get current display info
        
        self.rect = [s.current_w,s.current_h] # set screen size        
        self.C = [self.rect[0]/2, self.rect[1]/2] # divide width and height in two
        self.screen = pygame.display.set_mode(self.rect,pygame.FULLSCREEN) # create screen

        # INIT CONDITIONS
        self.condition_order = "conditions-8-4-even.txt"
        if int(self.participant.itervalues().next())%2 > 0: # uneven
           self.condition_order = "conditions-4-8-uneven.txt"
        # self.condinfo = randomise(self.condition_order,s=1,rand=1,asstr=1) # randomize
        self.condinfo = randomise(self.condition_order,s=1,rand=0,asstr=0) # randomize
        self.totalBlocks = len(self.condinfo)
                
        # INIT GLOBAL PARAMS
        self.totalscore = 0
        self.instrwait = 0
        self.now = datetime.datetime.now()
        self.filename = 'logs/banditlog_' + str(self.participant['Participant ID']) + '_' + time.strftime("%Y-%b%d-%H.%M.%S") + '.txt'
        self.file = open(self.filename, 'w')
        # self.file.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t"
        self.file.write("\n")
#        self.file.write("%s\t" % time.strftime("%Y-%b%d-%H.%M.%S"))
        self.file.write("%s\t%s\t%s\t%s\t%s\t%s\t %s\t%s\t%s\t%s\t%s\t%s\t%s"
            %("id","gender","age","block_id","trial_number",
            "bandit_position","bandit_id","payoff","rt","block_score","total_score_overall",
            "timestamp","ms"))
        self.file.close()

class block():
    def __init__(self,p,condition,currentblock):       
        # TIME
        self.flipTime = 0.3 # flipping time in seconds # should be .3
        self.waitingtime = 0.2 # time from flipping to choice. # should be .3
        self.timeOut = 1.5
        #((.3 + .3 + .2)*100*10)/60 = 13 min (fastest)
        # ((.3 + .3 + .2 + 1)*100*10)/60 = 30 min (slowest)

        # INIT BLOCK
        self.currentblock = currentblock
        self.blockId = int(condition[0])
        self.nTrials = int(condition[1]) 
        self.nBandits = int(condition[2])
        self.pace = condition[3]
        self.vis = condition[4]
        self.ncols = int(condition[5])
        self.nrows = int(condition[6])
        self.dispEV = int(condition[7])
        self.dispTrialNo = int(condition[8])
        self.dispTotalScore = int(condition[9])
        self.dispGraph = True#int(condition[10])     
        self.realBlockId = self.blockId

        # RANDOMIZE
        # print (self.blockId) 
        if (((int(p.participant.itervalues().next())-1) % 4) < 2) == True: 
            self.realBlockId = (self.blockId)
        else:
            self.realBlockId = 10-(self.blockId)
            if (10-(self.blockId)) <= 0:
                self.realBlockId = (10-(self.blockId)) + 16
        # print (self.realBlockId)
        
        file = "conditions/trials/cond_" + str(self.realBlockId) + "_trials_" + str(self.nBandits) + ".csv"        
        # if self.blockId > 5:
        #    file = "conditions/trials/cond_"+str(self.blockId - 5)+"_trials_" + str(self.nBandits) + ".csv"        
        self.trials = randomise(file,s=0,rand=0, asstr = 1)
        if len(self.trials)!=self.nTrials:
            print "Mismatch in lengths of trials"
        # self.bandShuffle = random.sample(range(self.nBandits),self.nBandits)
        self.bandShuffle = range(self.nBandits)
        
        # INIT BLOCK        
        self.banSize = [100,200] # w, h       
        hsep = 50
        vsep = 50
        
        # x coors  w/h    - cols                             
        x_rects = [p.C[0] - (self.ncols/2.-col)*(self.banSize[0]+hsep) for col in range(self.ncols)]
        y_rects = [p.C[1] - (self.nrows/2.-row)*(self.banSize[1]+vsep) for row in range(self.nrows)]

        #               xcoor,          ycoor,        w size,          h size
        self.banRects = [[x_rects[col], y_rects[row], self.banSize[0], self.banSize[1]] for row in range(self.nrows) for col in range(self.ncols)] 
        
        keys = [[113,119,101,114,116,121,117,105], #first row numbers
                [97,115,100,102,103,104,106,107]] #second row qwertzuiop
        self.keyVals = [keys[row][col] for row in range(self.nrows) for col in range(self.ncols)]        

        self.banRects = [self.banRects[i] for i in self.bandShuffle]
        self.keyVals = [self.keyVals[i] for i in self.bandShuffle]        
        self.previous = None
        self.blockscore = 0
        self.score_history = []        
        self.bandits = [ElBandito(p,self,i) for i in range(self.nBandits)]          
        if self.nBandits == 16 or self.nBandits == 4:
            self.labels = ["Q","W","E","R","T","Z","U","I","O","A","S","D","F","G","H","J"]
        elif self.nBandits == 8:
            self.labels = ["Q","W","E","R","A","S","D","F"]                     
    
    def banddisplay(self,p,color,flip,dots):
        for bandito in self.bandits:
            bandito.display_box(p,self,color,dots)
        #pygame.display.update()
        for bandito in self.bandits:
            bandito.display_pay(p,self,flip)
    
    def plotupdate(self,p):
        pass
#        plt.figure(figsize=(5,1))
#        plt.plot(range(len(self.score_history)),self.score_history,"-oc",linewidth=5)
#        plt.plot([0,self.nTrials],[0,0],"--k")
#        plt.xlim(0,self.nTrials)
#        if self.score_history:
#            init_y_min = 0
#            init_y_max = 10
#            plt.ylim(min(init_y_min ,min(self.score_history)),max(init_y_max ,max(self.score_history)))
#            plt.yticks([min(init_y_min ,min(self.score_history)),max(init_y_max ,max(self.score_history))])
#        else:
#            plt.ylim(-100,100)
#            plt.yticks([-100,100])
#        plt.tick_params(labelbottom='off')
#        plt.savefig('stims/figure.png')
#        plt.close()
#        self.graph = pygame.image.load('stims/figure.png')

    
    def plotdisplay(self,p):
        tl = p.C[0]+120
        ty = p.C[1]-375
        
        width,height = 500,100
        pygame.draw.polygon(p.screen,(0,0,0),[[tl,ty],[tl,ty+height],[tl+width,ty+height],[tl+width,ty]],2)
        pygame.draw.line(p.screen,(0,0,0),[tl-10,ty],[tl,ty],2)
        pygame.draw.line(p.screen,(0,0,0),[tl-10,ty+height],[tl,ty+height],2)
        for i in range(5):
            length = 10
            pygame.draw.line(p.screen,(0,0,0),[tl+i*width/5.,ty],[tl+i*width/5.,ty+length])
            pygame.draw.line(p.screen,(0,0,0),[tl+i*width/5.,ty+height],[tl+i*width/5.,ty+height-length])
        
        init_ymin,init_ymax = 0,10
        if self.score_history:
            ymin = min(init_ymin ,min(self.score_history))
            ymax = max(init_ymax ,max(self.score_history))
            points = [[tl,int(ty+float(height/(ymax-ymin))*(ymax-0))]]
            for point,n in zip(self.score_history,np.arange(len(self.score_history))):
                x = int(tl+n*float(width/self.nTrials))
                y = int(ty+float(height/(ymax-ymin))*(ymax-point))
                points.append([x,y])
            for i in range(len(points)-1):
                pygame.draw.line(p.screen,(0,255,255),points[i],points[i+1],4)
            for x,y in points:
                pygame.draw.circle(p.screen,(0,255,255),[x,y],5)
                pygame.draw.circle(p.screen,(0,0,0),[x,y],5,1)

        else:
            ymin = init_ymin
            ymax = init_ymax
        
        if ymin < 0:
            for i in range(20):
                y = int(ty+float(height/(ymax-ymin))*(ymax-0))
                pygame.draw.line(p.screen,(0,0,0),[tl+width/20*i,y],[tl+width/20*i+width/40,y],1)
        
        center_text(str(int(ymax)),[tl-15,ty,0,0],25,p,colour=(10,10,10),left = 0,right=1)
        center_text(str(int(ymin)),[tl-15,ty+height,0,0],25,p,colour=(10,10,10),left = 0,right=1)

class ElBandito():
    def __init__(self,p,b,number):
        self.id = number    #Bandit ID
        self.rect = b.banRects[self.id]     #bandit screen locay
        self.payoffs = []   #Initialise payoffs seen
        self.EV = None        #Initialise expected value
        self.clicked = None   #Initialise whether payoff is to be displayed
        self.toFlip = None    #Should the bandit be flipped???
    
    def calcEV(self):
        self.EV = np.mean(self.payoffs)
        self.VAR = np.var(self.payoffs)
        self.NUM = len(self.payoffs)
    
    def display_box(self,p,b,color,dots):
        if color == None:
            color = (0,0,0)
            fill = 0
        else:
            fill = 1
        if self.clicked!= None:
            #      p, rect (xcoor,   ycoor (ycoor + hsize - val),    wsize,        hsize), text,                          textsize, pressed, colour = (242,144,32)):            
            button(p, self.rect, b.labels[b.bandShuffle[self.id]], 30, fill, color)
            if dots:
                #                , x,            y,            w size,       h size, size, 
                center_text(dots, [self.rect[0], self.rect[1], self.rect[2], 60],    30, p)
        else:
            #      p, rect,      text,                             textsize, pressed, colour = (242,144,32)):
            button(p, self.rect, b.labels[b.bandShuffle[self.id]], 30,       0,       (0,0,0))

    def display_pay(self,p,b,flip=0):         
        if flip==0:
            if self.clicked != None:
                # color = (4, 167, 176)
                color = (87, 30, 110)
                #           string,                     rect,                                           size, p
                center_text("Belohnung",                [self.rect[0], self.rect[1] + self.rect[3] - 200, self.rect[2], 60], 20, p, colour=color)         
                center_text(str(int(self.payoffs[-1])), [self.rect[0], self.rect[1] + self.rect[3] - 175, self.rect[2], 60], 40, p, colour=color)
            if b.dispEV == 1:
                if self.EV != None:
                    color = (59,93,105)
                    #           string,               rect (xcoors,  ycoors,                         w,            h),  size, p
                    center_text("Durchschnitt",       [self.rect[0], self.rect[1] + self.rect[3]-98, self.rect[2], 60], 20, p, colour=color)
                    center_text(str(round(self.EV,1)),[self.rect[0], self.rect[1] + self.rect[3]-80, self.rect[2], 60], 30, p, colour=color)
                    center_text("Ausloesungen",       [self.rect[0], self.rect[1] + self.rect[3]-60, self.rect[2], 60], 20, p, colour=color)
                    center_text(str(self.NUM),        [self.rect[0], self.rect[1] + self.rect[3]-42, self.rect[2], 60], 30, p, colour=color)

class trial():
    def __init__(self,p,b,trial):
        self.tNo = trial
        self.game_over = False
        self.payoffs = b.trials[trial]

### BEGIN GLOBAL FUNCTIONS
def bandit(p,b):
    for trialno in range(b.nTrials):
        t = trial(p,b,trialno)
        pause(p,b,t)
        if trialno == 0:
            pass
            b.plotupdate(p)
            screenupdate(p,b,t,choice=1)
        getresponse(p,b,t)
        get_payoff(p,b,t)
        flipping(p,b,t)
        log(p,b,t)

def get_payoff(p,b,t):
    t.payoff = t.payoffs[t.resp]
    
    aap = b.trials[len(b.bandits[t.resp].payoffs)] # search payoffs at the number of ausloesungen for this bandit
    t.payoff = aap[t.resp] # search correct payoff
    
    # print str(aap) + "len" + str(len(b.bandits[t.resp].payoffs)) + "choose" + str(t.resp) + "payoff" + str(aap[t.resp])
    # print t.payoffs # based on trial nr
    
    p.totalscore += t.payoff
    b.blockscore += t.payoff
    b.score_history.append(b.blockscore)
    b.bandits[t.resp].payoffs.append(t.payoff)
    for bandit in b.bandits:
        bandit.clicked = None
    b.bandits[t.resp].clicked=t.payoff
    b.bandits[t.resp].calcEV()

def pause(p,b,t):
    game_over = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type==pygame.KEYDOWN and event.key==27:
            pygame.quit()
        elif event.type==pygame.KEYDOWN and event.key == 32:
            center_text("Pause",[p.C[0],p.C[1],0,0],80,p,colour=(0,0,255),left = 0,right=0)
            pygame.display.update()
            pygame.event.clear()
            while game_over == False:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        t.game_over = True
                    if event.type==pygame.KEYDOWN and event.key==27:
                        pygame.quit()
                    elif event.type==pygame.KEYDOWN and event.key == 32:
                        game_over = True
            screenupdate(p,b,t)

def getresponse(p,b,t):
    t.t0 = time.time()
    pygame.event.clear()
    while t.game_over == False:
        if b.pace == "auto" and b.previous>=0:
            if time.time()-t.t0>= b.timeOut:
                t.game_over= True
                t.RT=b.timeOut
                t.resp = b.previous
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                t.game_over = True
            if event.type==pygame.KEYDOWN and event.key==27:
                pygame.quit()
            elif event.type==pygame.KEYDOWN:
                if event.key in b.keyVals:
                    t.ans = b.keyVals.index(event.key)+1
                    t.RT=time.time()-t.t0
                    t.resp = t.ans-1
                    for bandit in b.bandits:
                        bandit.toFlip = None
                    b.bandits[t.resp].toFlip=1
                    t.game_over= True
            elif event.type==pygame.MOUSEBUTTONDOWN:
                t.ans = collision(event.pos,b.banRects)
                if t.ans:
                    t.RT=time.time()-t.t0
                    t.resp = t.ans-1
                    t.game_over= True
    if b.pace == "auto" and b.previous>=0:
        time.sleep(b.timeOut-t.RT)
    b.previous = t.resp

def screenupdate(p,b,t,color = None,flip=0,choice=0,dots = 0):
    p.screen.fill([255,255,255])
    if b.dispGraph:
        b.plotdisplay(p)     
    center_text("Durchgang",[p.C[0]-200,p.C[1]-380,0,0],40,p,colour=(10,10,10),left = 0,right=0)
    center_text(str(b.currentblock+1)+"/"+str(p.totalBlocks),[p.C[0],p.C[1]-380,0,0],40,p,colour=(10,10,10),left = 0,right=0)    
    if b.dispTrialNo:
        center_text("Runde",[p.C[0]-200,p.C[1]-340,0,0],40,p,colour=(10,10,10),left = 0,right=0)
        center_text(str(int(t.tNo)+1),[p.C[0],p.C[1]-340,0,0],40,p,colour=(10,10,10),left = 0,right=0)        
    if b.dispTotalScore:
        center_text("Punkte",[p.C[0]-200,p.C[1]-300,0,0],40,p,colour=(10,10,10),left = 0,right=0)
        center_text(str(int(b.blockscore)),[p.C[0],p.C[1]-300,0,0],40,p,colour=(10,10,10),left = 0,right=0)
    if choice == 1:
        center_text(u"Ausw\xe4hlen",[p.C[0],p.rect[1]-100,0,0],60,p,colour=(10,10,10),left = 0,right=0)
    b.banddisplay(p,color,flip,dots) #display the bandits
    pygame.display.update()

def flipping(p,b,t):
    startTime = time.time()
    text = [".","..","..."]
    tt = 0
    while time.time()-startTime < b.flipTime:
        screenupdate(p,b,t,flip = 1,dots = text[tt])
        tt = [1,2,0][tt]
        time.sleep(b.flipTime/4.)
    if t.payoff > 0:
        cc = 1
    else: cc = 0
    colour = [[255,0,0],[0,255,0]]
    screenupdate(p,b,t,colour[cc],flip = 0)
    time.sleep(b.waitingtime)
    # time.sleep(b.waitingtime + (1*b.waitingtime)*np.random.poisson(2))
    b.plotupdate(p)
    screenupdate(p,b,t,colour[cc],flip = 0,choice=1)

def log(p,b,t):
    """Write to the output file"""
    p.file = open(p.filename, 'a')
    p.file.write("\n")
    now = datetime.datetime.now()
    for value in p.participant.values():
        p.file.write("%s\t" % value)                    # ID, gender, age
    p.file.write("%i\t" % b.blockId)                    # condition ID
    p.file.write("%i\t" % t.tNo)                        # trial number
    p.file.write("%i\t" % b.bandShuffle[t.resp])       # Position
    p.file.write("%i\t" % t.resp)                       # bandit ID
    p.file.write("%i\t" % t.payoff)                     # money lost/won
    p.file.write("%f\t" % t.RT)                         # reaction time
    p.file.write("%i\t" % b.blockscore)                 # total score in Block
    p.file.write("%i\t" % p.totalscore)                 # total score in Game
    p.file.write("%s\t" % time.strftime("%Y-%b%d-%H.%M.%S"))      # timestamp 
    p.file.write("%s\t" % now.microsecond)      # milliseconds
    p.file.close()

def instructions(p):
    #matches = []
    #path = 'C:\Users\schepens\Dropbox\shared\JobsBandit\instr\starting_instr' # Job Work
    #path = 'C:\Users\job\Dropbox\shared\JobsBandit\instr\starting_instr' # Job Home
    #for root, dirnames, filenames in os.walk(path):
    #    for filename in fnmatch.filter(filenames, '*.txt'):
    #        matches.append(os.path.join(root, filename))
    instr_no = 0
    files = glob("instr/starting_instr/*.txt")
    complete = 0
    while complete == 0:
        switch = instructStarting(files[instr_no],p)
        instr_no = max(instr_no+switch,0)
        if instr_no >= len(files):
            complete=1

def main(participant):
    """Main experiment function. Determines order of sections"""
    p=parameters(participant)
    instructions(p)
    for condition,number in zip(p.condinfo,range(p.totalBlocks)):
        b = block(p,condition,number)
        if b.pace == "auto":
            instructStarting("instr/renew_instr/instr_renew_1.txt", p)
        bandit(p,b)
#        b.blockscore = 50
        instruction("instr/instr_between.txt",p,r= str(int(b.blockscore)))
        # win.winHandle.activate() #re-activate window  ??
     
#    p.totalscore = 800    
    bad = .01
    maxe = 3
    opts = p.totalBlocks*.6*b.nTrials
    mins = opts*bad
    money = float(p.totalscore - mins)/((opts-mins)/maxe)        
    if money < 1:
        money = 1
#     print p.totalscore
#    print money
# 
#    bad = .01
#    maxe = 3
#    totalBlocks  = 16
#    nTrials = 100
#    opts = totalBlocks*.6*nTrials #16*60=960
#    mins = opts*bad # 200
#    totalscore = totalBlocks * .5 * nTrials - ( 10 * totalBlocks ) 
#    totalscore = totalBlocks * .3 * nTrials - ( 20 * totalBlocks ) 
#    money = (totalscore - mins)/((opts-mins)/maxe)  # 120  
#    if money < 1:
#        money = 1
#    print money
        
    instruction("instr/instr_end_1.txt",p,r= str(int(money)))
    instruction("instr/instr_end_1.txt",p,r= str(int(money)))
    instruction("instr/instr_end_1.txt",p,r= str(int(money)))

if __name__ == "__main__":
    pygame.init() #This is what gets executed when you hit "run".
    pygame.mixer.init()
    participant = get_info(['Participant ID','Age','Gender'],[0,0,['male','female']]) #Get participant info
    main(participant) #Run main experiment
    pygame.quit()