import os
from time import time
from recorder import Recorder
from datetime import datetime
from pathlib import Path
import shutil

q_bank = {
    1:"What are you doing ?",
    2:"What is the big problem you are solving ?",
    3:"Why is it a hair on fire problem ?",
    4:"Why have other people not solved this problem yet ?",
    5:"What is your solution ?",
    6:"How is this solution defensible from likes of ABB/Schneider?",
    7:"Why would ABB/Schneider not take your customers away",
    8:"Why will DCs trust you over big companies ?",
    9:"What differentiates your solution from other solutions",
    10:"What is the market size ?",
    11:"How much of this market can you capture ?",
    12:"How will you make money ?",
    13:"Why would someone with 100million$ funding not be able to beat you in next 2 years ?",
    14:"What is the status of your POC ?",
    15:"How will you spend the money we give in IC ?",
    16:"Why you two ?",
    17:"Why did you guys chose to solve this problem ?",
    18:"How does your traction look like now ?",
    19:"How do you plan to reach 10/1000 customers ?",
    20:"What are customers saying about your product right now ?",
    21:"What has changed ? Why do you want to solve this problem now ?",
}

q_dg = {
    "introduction":[1],
    "problem":[2,3,4,17],
    "solution":[5,6,7,8,9,14],
    "defensibility":[13],
    "market":[10,11],
    "business_plan":[12],
    "traction":[18,19,20],
    "funding":[15],
    "misc":[21, 16],
}

def setup_dir(sections):
    now = datetime.now()
    start_time = now.strftime("%d%H%M%S")
    odir = start_time
    os.mkdir(odir)
    for section in sections:
        os.mkdir(Path(odir)/section)

    return odir


def string_to_filename(s):
    bad_chars = ["/","?"," ",","]
    s = s.lower()
    s = s.strip()
    for c in bad_chars:
        s = s.replace(c, "_")
    s = s.replace("__", "_")
    return s

def pitch(bank, dependency):
    odir = setup_dir(dependency)
    section_title = "--------{title}---------"
    question = "Q.{n}: {q}"
    
    total_time = 0
    pitch_start = time()
    q_times = {}
    for section in dependency:
        for q_index in dependency[section]:
            q = bank[q_index]
            print(question.format(n=q_index,q=q))
            q_start = time()
            
            q_fname = string_to_filename(q)
            rec_path = f"{odir}/{section}/{q_fname}.wav"
            rec = Recorder(rec_path)
            
            rec.start()

            next = input()   

            rec.stop()
            rec.join()

            q_end = time()
            q_time = int(q_end - q_start)
            # print (f"Duration:{q_time}s TotalTime:{total_time}s")
            total_time += q_time
            q_times[q_index] = q_time
    
    wall_time = int(time() - pitch_start)
    
    print ("++++++++++++PITCH Finished++++++{wall_time} secs+++++++")
    
    for section in dependency:
        total_time = sum(q_times[q] for q in dependency[section])
        num_questions = len(dependency[section])
        print (f"---------{section}---duration {total_time} seconds --- #{num_questions} questions ----")
   
    for q_index in sorted(q_times, reverse=True):
        print (f"{q_times[q_index]} secs: {bank[q_index]}")
    
    shutil.copytree(odir, "latest")


def pitch2(bank, dependency):
    odir = setup_dir(dependency)
    section_title = "--------{title}---------"
    question = "Q.{n}: {q}"
    
    total_time = 0
    pitch_start = time()
    q_times = {}
    next = 1
    q_done = set()
    
    while next != 0:
            q_index = next
            q_done.add(q_index)
            q = bank[q_index]
            print(question.format(n=q_index,q=q))
            q_start = time()
            
            q_fname = string_to_filename(q)
            rec_path = f"{odir}/{q_fname}.wav"
            rec = Recorder(rec_path)
            
            rec.start()
            
            while next in q_done:
                print (set(bank) - set(q_done))
                inp = input("Next question:")
                try:
                    inp = int(inp)
                except:
                    pass 
                if inp in q_done:                
                    print(f"repeated q {q_done}")
                elif inp not in bank:
                    print("invalid q no.")
                else:
                    next = inp 
                
            rec.stop()
            rec.join()

            q_end = time()
            q_time = int(q_end - q_start)
            # print (f"Duration:{q_time}s TotalTime:{total_time}s")
            total_time += q_time
            q_times[q_index] = q_time


    wall_time = int(time() - pitch_start)
    
    print ("++++++++++++PITCH Finished++++++{wall_time} secs+++++++")
    
    for section in dependency:
        total_time = sum(q_times[q] for q in dependency[section])
        num_questions = len(dependency[section])
        print (f"---------{section}---duration {total_time} seconds --- #{num_questions} questions ----")
   
    for q_index in sorted(q_times, reverse=True):
        print (f"{q_times[q_index]} secs: {bank[q_index]}")
    
    shutil.copytree(odir, "latest")
    

if __name__ == "__main__":
    pitch(q_bank, q_dg)
