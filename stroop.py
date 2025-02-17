import time
import sys
import os
import random
from psychopy import visual,event,core,gui

# Tasks:
# Part1:
# 1. Fixation Cross               # Done
# 2. AutoDraw                     # Done
# 3. Wait for a response          # Done
# 4. Reaction Times               # Done
# 5. Feedback                     # Done
# 6. Timeout                      # Done
# 7. Add incongruent trials       # Done
# 8. checkpoint                   # Done? It should be done.


def make_incongruent(color, stimuli):
    other_color = stimuli.copy()
    other_color.remove(color)
    # print(other_color)
    incongruent_color = random.choice(other_color)
    return incongruent_color

stimuli = ['red', 'orange', 'yellow', 'green', 'blue']

win = visual.Window([800,600],color="gray", units='pix',checkTiming=False)
placeholder = visual.Rect(win,width=180,height=80, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[0,0])
word_stim = visual.TextStim(win,text="", height=40, color="black",pos=[0,0])
instruction = visual.TextStim(win,text="Press the first letter of the ink color", height=20, color="black",pos=[0,-200])

fixation = visual.TextStim(win, text = "+", color = "black", height= 15)
response_keys = ['r', 'o', 'y', 'g', 'b', 'q']
RTs = []
key_pressed = False
timer = core.Clock()
incorrect_word = visual.TextStim(win, text = "Incorrect", color = "black", pos = [0,0], height= 40)
too_slow_word  = visual.TextStim(win, text = "Too slow", color = "black", pos = [0,0], height= 40)
trial_types = ["incongruent","normal"]

response_list = []
while True:
    # incongruent part
    # cur_stim = random.choice(stimuli)
    # word_stim.setText(cur_stim)
    # cur_color = make_incongruent(cur_stim, stimuli)
    # word_stim.setColor(cur_color)
    
    # random trial type
    cur_stim = random.choice(stimuli)
    word_stim.setText(cur_stim)
    trial_type = random.choice(trial_types)
    if trial_type == "incongruent":
        cur_color = make_incongruent(cur_stim, stimuli)
    else:
        cur_color = cur_stim

    word_stim.setColor(cur_color)

    placeholder.draw()
    instruction.draw()
    fixation.draw()
    win.flip()
    core.wait(.5)

    placeholder.draw()
    instruction.draw()
    win.flip()
    core.wait(.5)

    placeholder.draw()
    instruction.draw()
    word_stim.draw()
    win.flip()
    # core.wait(1.0)

    timer.reset(newT = 0.0) 
    key_pressed = event.waitKeys(keyList= response_keys, maxWait= 2)
    # print(key_pressed)
    # print(key_pressed[0])

    # print(timer.getTime() * 1000)
    RTs.append(round(timer.getTime() * 1000))

    if not key_pressed:
        placeholder.draw()
        instruction.draw()
        too_slow_word.draw()
        response = 'NA'
        win.flip()
        core.wait(1)
    elif key_pressed[0] == 'q':
        break
    elif key_pressed[0] == cur_stim[0]:
        response = cur_stim[0]
        pass
    else:
        # show incorrect and 1s time delay if wrong
        response = cur_stim[0]
        placeholder.draw()
        instruction.draw()
        incorrect_word.draw()
        win.flip()
        core.wait(1)
    
    response_list.append(response)

print(response_list)
print(RTs)