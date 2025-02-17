# Part2:
# 9. Create a generate trials file   # Done
# 10. Runtime variables              # Done
# 11. Read in a trials file          # Done
# 12. Write the data                 # Done 

import time
import sys
import os
import random
from psychopy import visual,event,core,gui


def make_incongruent(color, stimuli):
        other_color = stimuli.copy()
        other_color.remove(color)
        # print(other_color)
        incongruent_color = random.choice(other_color)
        return incongruent_color

def generate_trials(subj_code, seed,num_repetitions):
    '''
    Writes a file named {subj_code_}trials.csv, one line per trial. Creates a trials subdirectory if one does not exist
    subj_code: a string corresponding to a participant's unique subject code
    seed: an integer specifying the random seed
    num_repetitions: integer specifying total times that combinations of trial type (congruent vs. incongruent) 
    and orientation (upright vs. upside_down) should repeat 
    (total number of trials = 4 * num_repetitions)
    '''
    import os
    import random

    separator = ','

    stimuli = ['red', 'orange', 'yellow', 'green', 'blue']
    trial_types = ["incongruent","normal"]
    orientations = ["upright", "upside_down"]

    

    # create a trials folder if it doesn't already exist
    try:
        os.mkdir('trials')
    except FileExistsError:
        print('Trials directory exists; proceeding to open file')
    f= open(f"trials/{subj_code}_trials.csv","w")

    #write header
    # cols = "subj_code" "seed" "word to be shown" "word color" "trial_type incongruent or not" "word orientation upright or upside_down"
    header = separator.join(["subj_code","seed","word", 'color','trial_type','orientation'])
    f.write(header+'\n')
    
    random.seed(int(seed))


    # write code to loop through creating and adding trials to the file here
    cols_data = []
    for _ in range(int(num_repetitions)):
        for trial_type in trial_types:
            for ori in orientations:
                cur_stim = random.choice(stimuli)
                if trial_type == "incongruent":
                    cur_color = make_incongruent(cur_stim, stimuli)
                else:
                    cur_color = cur_stim

                cols_data.append([subj_code,seed,cur_stim,cur_color,trial_type, ori])

    random.shuffle(cols_data)
    for trial in cols_data:
        f.write(separator.join(map(str, trial)) + '\n')
    #close the file
    f.close()


from psychopy import gui

#To get a bunch of runtime variables
def get_runtime_vars(vars_to_get,order,exp_version="Stroop"):
    #Get run time variables, see http://www.psychopy.org/api/gui.html for explanation
    infoDlg = gui.DlgFromDict(dictionary=vars_to_get, title=exp_version, order=order)
    if infoDlg.OK:
        return vars_to_get
    else: 
        print('User Cancelled')


order =  ['subj_code','seed','num_reps']
runtime_vars = get_runtime_vars({'subj_code':'stroop_01','seed': 1, 'num_reps': 5}, order)

# get the function from python/mental_rotation/helper.py
def import_trials(trial_filename, col_names=None, separator=','):
    trial_file = open(trial_filename, 'r')
 
    if col_names is None:
        # Assume the first row contains the column names
        col_names = trial_file.readline().rstrip().split(separator)
    trials_list = []
    for cur_trial in trial_file:
        cur_trial = cur_trial.rstrip().split(separator)
        assert len(cur_trial) == len(col_names) # make sure the number of column names = number of columns
        trial_dict = dict(zip(col_names, cur_trial))
        trials_list.append(trial_dict)
    return trials_list

# def generate_trials(subj_code, seed,num_repetitions=25):
generate_trials(runtime_vars['subj_code'],runtime_vars['seed'],runtime_vars['num_reps'])

# get from python/mental_rotation/mental_rotation_complete.py
trial_path = os.path.join(os.getcwd(),'trials',runtime_vars['subj_code']+'_trials.csv')
trial_list = import_trials(trial_path)
print(trial_list)

# variables from stroop.py
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
# trial_types = ["incongruent","normal"]

try:
    os.mkdir('data')
except FileExistsError:
    print('data directory exists; proceeding to open file')
data_file= open(os.path.join(os.getcwd(),'data',runtime_vars['subj_code']+'_data.csv'),'w')
# cols = "subj_code" "seed" "word to be shown" "word color" "trial_type incongruent or not" "word orientation upright or upside_down"
# 
header = ','.join(["subj_code","seed","word", 'color','trial_type','orientation',
                   'trial_num', 'response', 'is_correct', 'rt'])
data_file.write(header+'\n')

trial_num = 1
for cur_trial in trial_list:
    response_list = []

    cur_stim = cur_trial['word']
    cur_color = cur_trial['color']
    cur_trial_type = cur_trial['trial_type']
    cur_ori = cur_trial['orientation']

    word_stim.setText(cur_stim)
    word_stim.setColor(cur_color)

    if cur_ori == 'upside_down':
        word_stim.setOri(180)
    else:
        word_stim.setOri(0)
    
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

    timer.reset(newT = 0.0) 
    key_pressed = event.waitKeys(keyList= response_keys, maxWait= 2)

    # print(timer.getTime() * 1000)
    # RTs.append(round(timer.getTime() * 1000))
    response_rt = round(timer.getTime() * 1000)

    if not key_pressed:
        is_correct = 0
        response_ans = 'NA'
        placeholder.draw()
        instruction.draw()
        too_slow_word.draw()
        win.flip()
        core.wait(1)
    # elif key_pressed[0] == 'q':
    #     break
    elif key_pressed[0] == cur_stim[0]:
        is_correct = 1
        response_ans = cur_stim[0]
        pass
    else:
        is_correct = 0
        response_ans = key_pressed[0]
        # show incorrect and 1s time delay if wrong
        placeholder.draw()
        instruction.draw()
        incorrect_word.draw()
        win.flip()
        core.wait(1)

    for i in cur_trial:
        response_list.append(cur_trial[i])
    # previous 6 columns responses not added yet

    print(response_list)
    response_list.extend([trial_num,response_ans,is_correct,response_rt])
    responses = map(str,response_list)
    print(response_list)
    line = ','.join([str(i) for i in response_list])
    data_file.write(line+'\n')

    trial_num += 1

data_file.close()