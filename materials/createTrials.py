#Lukas Nagel - lnagel@mpib-berlin.mpg.de

from psychopy import gui
from psychopy import parallel
#import fnmatch
#import os
import pygame
#import time
import random
#import datetime
import numpy as np
#import textwrap
#import os
import pygame
#import glob
from extras import *
#import os.path

def main():
#    ctrials("conditions/cond_1.csv",8,100,rando,"conditions/cond_1_param.csv")
#    ctrials("conditions/cond_2.csv",8,100,rando,"conditions/cond_2_param.csv")
#    ctrials("conditions/cond_3.csv",8,100,rando,"conditions/cond_3_param.csv")
#    ctrials("conditions/cond_4.csv",8,100,rando,"conditions/cond_4_param.csv")
#    ctrials("conditions/cond_5.csv",8,100,rando,"conditions/cond_5_param.csv")
#    ctrials("conditions/cond_6.csv",8,100,rando,"conditions/cond_6_param.csv")
#    ctrials("conditions/cond_7.csv",8,100,rando,"conditions/cond_7_param.csv")
#    ctrials("conditions/cond_8.csv",8,100,rando,"conditions/cond_8_param.csv")
#    ctrials("conditions/cond_9.csv",8,100,rando,"conditions/cond_9_param.csv")
#    ctrials("conditions/cond_10.csv",8,100,rando,"conditions/cond_10_param.csv")    
    
#    - 48484848 48484848 options per block for participants with even id's
#    - 84848484 84848484 options per block for participants with uneven id's

    ctrials("conditions/trials/cond_1_trials_4.csv","conditions/trials/cond_2_trials_4.csv",4,100,rando,"conditions/cond_1_param_4.csv")
    ctrials("conditions/trials/cond_2_trials_8.csv","conditions/trials/cond_3_trials_8.csv",8,100,rando,"conditions/cond_2_param_8.csv")
    ctrials("conditions/trials/cond_3_trials_4.csv","conditions/trials/cond_4_trials_4.csv",4,100,rando,"conditions/cond_3_param_4.csv")
    ctrials("conditions/trials/cond_4_trials_8.csv","conditions/trials/cond_5_trials_8.csv",8,100,rando,"conditions/cond_4_param_8.csv")
    ctrials("conditions/trials/cond_5_trials_4.csv","conditions/trials/cond_6_trials_4.csv",4,100,rando,"conditions/cond_5_param_4.csv")
    ctrials("conditions/trials/cond_6_trials_8.csv","conditions/trials/cond_7_trials_8.csv",8,100,rando,"conditions/cond_6_param_8.csv")
    ctrials("conditions/trials/cond_7_trials_4.csv","conditions/trials/cond_8_trials_4.csv",4,100,rando,"conditions/cond_7_param_4.csv")
    ctrials("conditions/trials/cond_8_trials_8.csv","conditions/trials/cond_9_trials_8.csv",8,100,rando,"conditions/cond_8_param_8.csv")

    ctrials("conditions/trials/cond_9_trials_4.csv","conditions/trials/cond_10_trials_4.csv",4,100,rando,"conditions/cond_9_param_4.csv")
    ctrials("conditions/trials/cond_10_trials_8.csv","conditions/trials/cond_11_trials_8.csv",8,100,rando,"conditions/cond_10_param_8.csv")    
    ctrials("conditions/trials/cond_11_trials_4.csv","conditions/trials/cond_12_trials_4.csv",4,100,rando,"conditions/cond_11_param_4.csv")
    ctrials("conditions/trials/cond_12_trials_8.csv","conditions/trials/cond_13_trials_8.csv",8,100,rando,"conditions/cond_12_param_8.csv")
    ctrials("conditions/trials/cond_13_trials_4.csv","conditions/trials/cond_14_trials_4.csv",4,100,rando,"conditions/cond_13_param_4.csv")
    ctrials("conditions/trials/cond_14_trials_8.csv","conditions/trials/cond_15_trials_8.csv",8,100,rando,"conditions/cond_14_param_8.csv")
    ctrials("conditions/trials/cond_15_trials_4.csv","conditions/trials/cond_16_trials_4.csv",4,100,rando,"conditions/cond_15_param_4.csv")
    ctrials("conditions/trials/cond_16_trials_8.csv","conditions/trials/cond_1_trials_8.csv",8,100,rando,"conditions/cond_16_param_8.csv")


def ctrials(filename1, filename2, bandits, trialNo, func, params):
    trials = np.zeros((trialNo,bandits))
    for trial in range(trialNo):
        trials = func(bandits,trial,trials,params)
    np.savetxt(filename1,trials,fmt='%i',delimiter="\t")
    np.savetxt(filename2,trials,fmt='%i',delimiter="\t")

def rando(bandits,trial,trials,params):
    blockinfo = randomise(params,s=1,rand=0) # (returns a list of the list of details for each bandit)
    payoffs = [None]*bandits
    for bandit in range(bandits):
        if random.random()<= float(blockinfo[bandit][3]): # gen random number and check if its smaller than Prob1
            trials[trial,bandit] = blockinfo[bandit][1] # if so, put Payoff1 in trial file
        else:
            trials[trial,bandit] = blockinfo[bandit][2]
    return trials


if __name__ == "__main__":
    main()