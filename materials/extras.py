#Lukas Nagel - lnagel@mpib-berlin.mpg.de

import pygame
import time
import random
import datetime
import numpy as np
from psychopy import gui
import textwrap
import os
from glob import *

def instruction(file,p,y_pos=200,width=60,size=35,r= ""):
    """Displays instructions from file"""
    p.screen.fill([225,225,225])
    TextDisplay(file,y_pos,width,size,p,xx="XXXX",xr = r )
    center_text(u'Eingebetaste dr\xfccken, um fortzufahren',[0,p.rect[1]-100,p.rect[0],100],40,p)
    pygame.display.flip()
    game_over = False
    time.sleep(0)
    while game_over == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type==pygame.KEYDOWN and event.key==27:
                pygame.quit()
            elif event.type==pygame.KEYDOWN and event.key==13:
                game_over = True
            elif event.type==pygame.KEYDOWN:
                print event.key

def instructStarting(file,p,y_pos=100,width=100,size=30,end=0):
    pic = file.replace(".txt",".png")
    showpic=0
    if os.path.isfile(pic):
        showpic = pygame.image.load(pic)
    p.screen.fill([225,225,225])
    TextDisplayStarting(file,y_pos,width,size,p,showpic,end)
    center_text(u'Eingebetaste dr\xfccken, um fortzufahren, Pfeiltasten dr\xfccken, um zur\xfcckzugehen',[0,p.rect[1]-100,p.rect[0],100],30,p)
    pygame.display.flip()
    game_over = False
    time.sleep(p.instrwait)
    pygame.event.clear()
    while game_over == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type==pygame.KEYDOWN and event.key==27:
                pygame.quit()
            elif event.type==pygame.KEYDOWN and event.key==13:
                game_over = True
                return 1
            elif event.type==pygame.KEYDOWN and event.key==276:
                game_over = True
                return -1
            elif event.type==pygame.KEYDOWN and event.key==275:
                game_over = True
                return 1
            elif event.type==pygame.KEYDOWN:
                print event.key

def TextDisplay(file,y_pos,width,size,p,xx=" ",xr=" ",yy=" ",yr=" "):
    """reads in a text file and displays it on the screen"""
    string = filter(None,[strin.replace("\n",'') for strin in open(file,'r').readlines()])
    string = [strin.decode('utf-8') for strin in string]
    string = [strin.replace(xx,xr).replace(yy,yr) for strin in string]
    wrappedstring=[]
    for stri in string:
        new=textwrap.wrap(stri,width)
        for st in new:
            wrappedstring.append(st)
        wrappedstring.append('')
    shift=0
    for strin in wrappedstring:        
        font = pygame.font.Font(None, size)
        text = font.render(strin,1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx= (p.rect[0]/2)
        textpos.centery = (y_pos+shift)
        p.screen.blit(text, textpos)
        shift+=size

def TextDisplayStarting(file,y_pos,width,size,p,show,end):
    if show:
        width = width/2
        impos = show.get_rect()
        impos.centerx= (3*p.rect[0]/4)
        impos.top = (y_pos)
        p.screen.blit(show, impos)
    """reads in a text file and displays it on the screen"""
    string = filter(None,[strang.replace("\n",'') for strang in open(file,'r').readlines()])
    if end:
        string = [s.replace("XXXX",str(int(p.grandtotal))) for s in string]
    wrappedstring=[]
    for strin in string:
        new=textwrap.wrap(strin,width)
        for st in new:
            wrappedstring.append(st)
        wrappedstring.append('')
    shift=0
    for strin in wrappedstring:        
        font = pygame.font.Font(pygame.font.match_font('arial'), size)
        text = font.render(strin.decode('utf-8'),1, (10, 10, 10))
        textpos = text.get_rect()
        if show:
            textpos.centerx= (p.rect[0]/4)
        else:
            textpos.centerx= (p.rect[0]/2)
        textpos.centery = (y_pos+shift)
        p.screen.blit(text, textpos)
        shift+=size+10
        
def center_text(string,rect,size,p,colour=(10,10,10),left = 0,right=0):
    """Displays on line of text, centered within a rect"""
    font = pygame.font.Font(None, size)
    text = font.render(string,1, colour)
    textpos = text.get_rect()
    textpos.centerx = rect[0]+rect[2]/2
    if left == 1:
        textpos.left = rect[0]
    if right == 1:
        textpos.right = rect[0]
    textpos.centery = rect[1]+rect[3]/2
    p.screen.blit(text, textpos)

def collision(position,rectlist):
    """This determines whether a point (position) lies within one of the given rectangles (rectlist). returns the 
    rect over which the action was performed +1 """
    x,n =0,0
    for i in range(len(rectlist)):
        if pygame.Rect(rectlist[i]).collidepoint(position):
            x = i+1
    return x

def button(p,rect,text,textsize,pressed, colour = (242,144,32)):
    """Displays a 'button' at a certain location and size (rect), with text, textsize, and whether or not the button is filled in (pressed)"""
    fill = (1 - pressed) * 5
    pygame.draw.rect(p.screen,colour,rect,fill)
    color = (59,93,105)
    center_text("Spielautomat",       [rect[0], rect[1] + rect[3]-138, rect[2], 60], 20, p, colour=color)    
    center_text(text,          [rect[0], rect[1] + rect[3]-120, rect[2], 60], 30,p, colour = color)


def get_info(keys,vals):
    """Opens GUI for input of participant info"""
    info = {keys[i]:vals[i] for i in range(len(keys))}
    infoSet =False
    while infoSet == False:
        if info['Participant ID']<1:
            infoDlg = gui.DlgFromDict(dictionary=info, title='Bandit',
            order=keys,)#this attribute can't be changed by the user
            if infoDlg.OK: #this will be True (user hit OK) or False (cancelled)
                pass
            else: 
                print 'User Cancelled'
                quits
        else:
            infoSet = True
    return info

def randomise(file,s=0,e=0,rand = 1,asstr=0):
    """Randomises the trials in a file, or doesn't"""
    with open(file,'r') as f:
        listy= [x.strip().split('\t') for x in f]
    if e>0:
        listy = [listy[i] for i in range(e)]
    if s>0:
        listy = [listy[i] for i in np.arange(s,len(listy),1)]
    if rand ==1:
        randorder = random.sample(listy, len(listy))
        if asstr == 1:
            randorder = [randorder[i] for i in range(len(randorder))]
        else:
            randorder = [map(float, randorder[i]) for i in range(len(randorder))]
        return randorder
    elif s == 0:
        listy = [map(float, listy[i]) for i in range(len(listy))]        
        return listy
    else:
        return listy