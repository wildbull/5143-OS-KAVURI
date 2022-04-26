from hashlib import new
from platform import release
from utils import IoQueue, Pcb,JobStateQueue,ReadyQueue,WaitQueue,RunningQueue,TerminatedQueue
from simulate import *
from config import *
import sys
from time import sleep
import threading
import textwrap as tr

########## PROMPT_APP ##################
from re import I
from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, Window , HSplit
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.output.color_depth import ColorDepth
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
############################################

######## Visualisatoin settings ############
fcfs_buffer = Buffer()  # Editable buffer.
sjf_buffer = Buffer()  # Editable buffer.
rr_buffer = Buffer()  # Editable buffer.
srt_buffer = Buffer()  # Editable buffer.
pb_buffer = Buffer()  # Editable buffer.
generic_buffer = Buffer()  # Editable buffer.

style = Style([
     ('left', 'bg:ansired'),
     ('top', 'fg:#00aaaa'),
     ('bottom', 'underline bold'),
     ])

#######
#repeatable_container = Hsplit([ 

#######

fcfs_window = Window(content=BufferControl(buffer=fcfs_buffer), style="class:top")
sjf_window = Window(content=BufferControl(buffer=sjf_buffer),style="class:top")
rr_window = Window(content=BufferControl(buffer=rr_buffer), style="class:top")
srt_window = Window(content=BufferControl(buffer=srt_buffer),style="class:top")
pb_window = Window(content=BufferControl(buffer=pb_buffer),style="class:top")
generic_window = Window(content=BufferControl(buffer=generic_buffer),style="class:top")

#############################################

NewQueue = JobStateQueue()

Pause = False

make_2digits = lambda x: '0'*(2-len(x)) + x
def make_n_digits(lst , max_len = NUM_CPUS):
    lst = [make_2digits(i) for i in lst]
    string =  ",".join(lst)
    length_needed = 3*max_len - 1
    if len(string) < length_needed:
        string += "*"*(length_needed-len(string))
    return string

def print_cpu(running, cpu_released, io_released):
    string =''' 
    |--RUNNING--| |---I.O---| |--READY--|
    |   %s   | |  %s  | |  %s  |           
    -------------------------------------
    '''%(make_n_digits(running), make_n_digits(cpu_released), make_n_digits(io_released))
    return tr.dedent(string)

def print_ques(scheduler_obj):
    return_str = ""
    return_str += str(scheduler_obj.newQueue)
    return_str += str(scheduler_obj.readyQueue) 
    return_str += str(scheduler_obj.waitQueue) 
    return_str += str(scheduler_obj.runningQueue)
    return_str += str(scheduler_obj.ioQueue)
    return_str += str(scheduler_obj.terminatedQueue)
    return return_str

def print_scheduler(scheduler_obj, results, released_jobs, io_releases):
    scheduler_obj.buffer.insert_text("FCFS \n")
    scheduler_obj.buffer.insert_text("time step = "+ str(scheduler_obj.time) + "\n")
    scheduler_obj.buffer.insert_text(results)
    running_pids = [str(i.pid) for i in scheduler_obj.runningQueue.q]
    #self.buffer.insert_text("Running ::  "+ str(running_pids)+ "\n")
    released_jobs = [str(i.pid) for i in released_jobs]
    #self.buffer.insert_text("Released jobs = "+ ",".join(released_jobs)+ "\n")
    io_releases = [str(i.pid) for i in io_releases]
    #self.buffer.insert_text("IO releases = "+ ",".join(io_releases) + "\n")
    scheduler_obj.buffer.insert_text(print_cpu(running_pids, released_jobs, io_releases))


class FCFS:
    def __init__(self, data, buffer):
        self.data = data
        self.time = 0
        self.newQueue = NewQueue 
        self.readyQueue = ReadyQueue ()
        self.waitQueue = WaitQueue ()
        self.runningQueue = RunningQueue ()
        self.ioQueue = IoQueue ()
        self.terminatedQueue = TerminatedQueue ()
        self.buffer = buffer

    def run_ts(self):
        #update time
        self.time += 1

        #fill QUEUES
        self.newQueue.extend([i for i in self.data if (i.arrivalTime == self.time)])
        self.readyQueue.incrementTime()
        self.readyQueue.extend(self.newQueue.q)
        self.newQueue.emptyq()

        released_jobs = self.runningQueue.incrementTime()
        #print("released jobs :: ", released_jobs)
        # declare a job completed if a job doesnt have any more cpuBursts left in released jobs
        completed_jobs = [i for i in released_jobs if not len(i.cpuBursts)]
        if len(self.readyQueue.q):
            while len(self.runningQueue.q) < NUM_CPUS:
                try:
                    if len(self.readyQueue.q):
                        self.runningQueue.add(self.readyQueue.remove())
                    else:
                        break
                except Exception as e:
                    print("############## EXCEPTION in FCFS run_ts cpu_burst ################")
                    print(e)
                    break
        
        self.waitQueue.incrementTime()
        io_releases = self.ioQueue.incrementTime()
        
        #print("io released jobs :: ", io_releases)
        
        #add jobs to io queue
        for i in released_jobs:
            if i not in completed_jobs:
                self.waitQueue.add(i)
        
        for i in io_releases:
            self.readyQueue.add(i)

        if len(self.waitQueue.q):
            while len(self.ioQueue.q) < NUM_IO_DEVICES:
                try:
                    if len(self.waitQueue.q):
                        self.ioQueue.add(self.waitQueue.remove())
                    else:
                        break
                except Exception as e:
                    print("############## EXCEPTION in FCFS run_ts io_burst ################")
                    print(e)
                    break

        for job in completed_jobs:
            self.terminatedQueue.add(completed_jobs)
        
        results = print_ques(self)
        '''
        #rint("time step = ",self.time , "\n")
        #print(results)
        self.buffer.insert_text("FCFS \n")
        self.buffer.insert_text("time step = "+ str(self.time) + "\n")
        self.buffer.insert_text(results)
        running_pids = [str(i.pid) for i in self.runningQueue.q]
        #self.buffer.insert_text("Running ::  "+ str(running_pids)+ "\n")
        released_jobs = [str(i.pid) for i in released_jobs]
        #self.buffer.insert_text("Released jobs = "+ ",".join(released_jobs)+ "\n")
        io_releases = [str(i.pid) for i in io_releases]
        #self.buffer.insert_text("IO releases = "+ ",".join(io_releases) + "\n")
        self.buffer.insert_text(print_cpu(running_pids, released_jobs, io_releases))
        '''
        print_scheduler(self, results, released_jobs, io_releases)
        return results



class SJF:
    def __init__(self, data, buffer):
        self.data = data
        self.time = 0
        self.newQueue = NewQueue 
        self.readyQueue = ReadyQueue ()
        self.waitQueue = WaitQueue ()
        self.runningQueue = RunningQueue ()
        self.ioQueue = IoQueue ()
        self.terminatedQueue = TerminatedQueue ()
        self.buffer = buffer
    
    def run_ts(self):
        #update time
        self.time += 1

        #fill QUEUES
        ############  
        self.newQueue.extend([i for i in self.data if (i.arrivalTime == self.time)])
        self.readyQueue.incrementTime()
        self.readyQueue.extend(self.newQueue.q)
        self.newQueue.emptyq()
        
        #sort entries of new_queue based on total cpu_burst_time
        self.readyQueue.sort("total_cpu_time")

        released_jobs = self.runningQueue.incrementTime()
        #print("released jobs :: ", released_jobs)
        # declare a job completed if a job doesnt have any more cpuBursts left in released jobs
        completed_jobs = [i for i in released_jobs if not len(i.cpuBursts)]
        if len(self.readyQueue.q):
            while len(self.runningQueue.q) < NUM_CPUS:
                try:
                    if len(self.readyQueue.q):
                        self.runningQueue.add(self.readyQueue.remove())
                    else:
                        break
                except Exception as e:
                    print("############## EXCEPTION in FCFS run_ts cpu_burst ################")
                    print(e)
                    break
 
        self.waitQueue.incrementTime()
        io_releases = self.ioQueue.incrementTime()
        
        #print("io released jobs :: ", io_releases)
        
        #add jobs to io queue
        for i in released_jobs:
            if i not in completed_jobs:
                self.waitQueue.add(i)
        
        for i in io_releases:
            self.readyQueue.add(i)

        if len(self.waitQueue.q):
            while len(self.ioQueue.q) < NUM_IO_DEVICES:
                try:
                    if len(self.waitQueue.q):
                        self.ioQueue.add(self.waitQueue.remove())
                    else:
                        break
                except Exception as e:
                    print("############## EXCEPTION in FCFS run_ts io_burst ################")
                    print(e)
                    break

        for job in completed_jobs:
            self.terminatedQueue.add(completed_jobs)
        
        results = print_ques(self)
        #print("time step = ",self.time , "\n")
        #print(results)
        self.buffer.insert_text("SJF \n")
        self.buffer.insert_text("time step = "+ str(self.time) + "\n")
        self.buffer.insert_text(results + "\n")
        released_jobs = [str(i) for i in released_jobs]
        self.buffer.insert_text("Released jobs = "+ ",".join(released_jobs)+ "\n")
        io_releases = [str(i) for i in io_releases]
        self.buffer.insert_text("IO releases = "+ ",".join(io_releases) + "\n")
        return results

class SRT:
    def __init__(self, data, buffer):
        self.data = data
        self.time = 0
        self.newQueue = NewQueue 
        self.readyQueue = ReadyQueue ()
        self.waitQueue = WaitQueue ()
        self.runningQueue = RunningQueue ()
        self.ioQueue = IoQueue ()
        self.terminatedQueue = TerminatedQueue ()
        self.buffer = buffer
    
    def run_ts(self):
        #update time
        self.time += 1

        #fill QUEUES
        ############  
        self.newQueue.extend([i for i in self.data if (i.arrivalTime == self.time)])
        self.readyQueue.incrementTime()
        self.readyQueue.extend(self.newQueue.q)
        self.newQueue.emptyq()
        
        #sort entries of new_queue based on total cpu_burst_time
        self.readyQueue.sort("cpu_time_left")

        released_jobs = self.runningQueue.incrementTime()
        #print("released jobs :: ", released_jobs)
        # declare a job completed if a job doesnt have any more cpuBursts left in released jobs
        completed_jobs = [i for i in released_jobs if not len(i.cpuBursts)]
        if len(self.readyQueue.q):
            while len(self.runningQueue.q) < NUM_CPUS:
                try:
                    if len(self.readyQueue.q):
                        self.runningQueue.add(self.readyQueue.remove())
                    else:
                        break
                except Exception as e:
                    print("############## EXCEPTION in FCFS run_ts cpu_burst ################")
                    print(e)
                    break

        self.waitQueue.incrementTime()
        io_releases = self.ioQueue.incrementTime()
        
        #print("io released jobs :: ", io_releases)
        
        #add jobs to io queue
        for i in released_jobs:
            if i not in completed_jobs:
                self.waitQueue.add(i)
        
        for i in io_releases:
            self.readyQueue.add(i)

        if len(self.waitQueue.q):
            while len(self.ioQueue.q) < NUM_IO_DEVICES:
                try:
                    if len(self.waitQueue.q):
                        self.ioQueue.add(self.waitQueue.remove())
                    else:
                        break
                except Exception as e:
                    print("############## EXCEPTION in FCFS run_ts io_burst ################")
                    print(e)
                    break

        for job in completed_jobs:
            self.terminatedQueue.add(completed_jobs)
        
        results = print_ques(self)
        #print("time step = ",self.time , "\n")
        #print(results)
        self.buffer.insert_text("SRT \n")
        self.buffer.insert_text("time step = "+ str(self.time) + "\n")
        self.buffer.insert_text(results + "\n")
        released_jobs = [str(i) for i in released_jobs]
        self.buffer.insert_text("Released jobs = "+ ",".join(released_jobs)+ "\n")
        io_releases = [str(i) for i in io_releases]
        self.buffer.insert_text("IO releases = "+ ",".join(io_releases) + "\n")
        return results




class RR:
    def __init__(self, data, buffer):
        self.data = data
        self.time = 0
        self.RR_quantum = 5
        self.newQueue = NewQueue 
        self.readyQueue = ReadyQueue ()
        self.waitQueue = WaitQueue ()
        self.runningQueue = RunningQueue ()
        self.ioQueue = IoQueue ()
        self.terminatedQueue = TerminatedQueue ()
        self.buffer = buffer
    
    def run_ts(self):
        #update time
        self.time += 1

        #fill QUEUES
        ############  
        self.newQueue.extend([i for i in self.data if (i.arrivalTime == self.time)])
        self.readyQueue.incrementTime()
        self.readyQueue.extend(self.newQueue.q)
        self.newQueue.emptyq()
        
        released_jobs = self.runningQueue.incrementTime()

        for job in self.runningQueue.q:
            if not job.currBurstCpuUsage<self.RR_quantum:
                self.runningQueue.q.remove(job)
                released_jobs.append(job)


        #print("released jobs :: ", released_jobs)
        # declare a job completed if a job doesnt have any more cpuBursts left in released jobs
        completed_jobs = [i for i in released_jobs if not len(i.cpuBursts)]
        if len(self.readyQueue.q):
            while len(self.runningQueue.q) < NUM_CPUS:
                try:
                    if len(self.readyQueue.q):
                        self.runningQueue.add(self.readyQueue.remove())
                    else:
                        break
                except Exception as e:
                    print("############## EXCEPTION in FCFS run_ts cpu_burst ################")
                    print(e)
                    break

        self.waitQueue.incrementTime()
        io_releases = self.ioQueue.incrementTime()
        
        #print("io released jobs :: ", io_releases)
        
        #add jobs to io queue
        for i in released_jobs:
            if i not in completed_jobs:
                self.waitQueue.add(i)
        
        for i in io_releases:
            self.readyQueue.add(i)

        if len(self.waitQueue.q):
            while len(self.ioQueue.q) < NUM_IO_DEVICES:
                try:
                    if len(self.waitQueue.q):
                        self.ioQueue.add(self.waitQueue.remove())
                    else:
                        break
                except Exception as e:
                    print("############## EXCEPTION in FCFS run_ts io_burst ################")
                    print(e)
                    break

        for job in completed_jobs:
            self.terminatedQueue.add(completed_jobs)
        
        results = print_ques(self)
        #print("time step = ",self.time , "\n")
        #print(results)
        self.buffer.insert_text("RR \n")
        self.buffer.insert_text("time step = "+ str(self.time) + "\n")
        self.buffer.insert_text(results + "\n")
        released_jobs = [str(i) for i in released_jobs]
        self.buffer.insert_text("Released jobs = "+ ",".join(released_jobs)+ "\n")
        io_releases = [str(i) for i in io_releases]
        self.buffer.insert_text("IO releases = "+ ",".join(io_releases) + "\n")
        return results


class PB:
    def __init__(self, data, buffer):
        self.data = data
        self.time = 0
        self.newQueue = NewQueue 
        self.readyQueue = ReadyQueue ()
        self.waitQueue = WaitQueue ()
        self.runningQueue = RunningQueue ()
        self.ioQueue = IoQueue ()
        self.terminatedQueue = TerminatedQueue ()
        self.buffer = buffer
    
    def run_ts(self):
        #update time
        self.time += 1

        #fill QUEUES
        ############  
        self.newQueue.extend([i for i in self.data if (i.arrivalTime == self.time)])
        self.readyQueue.incrementTime()
        self.readyQueue.extend(self.newQueue.q)
        self.newQueue.emptyq()
        
        #sort entries of new_queue based on total cpu_burst_time
        self.readyQueue.sort("priority")

        released_jobs = self.runningQueue.incrementTime()
        #print("released jobs :: ", released_jobs)
        # declare a job completed if a job doesnt have any more cpuBursts left in released jobs
        completed_jobs = [i for i in released_jobs if not len(i.cpuBursts)]
        if len(self.readyQueue.q):
            while len(self.runningQueue.q) < NUM_CPUS:
                try:
                    if len(self.readyQueue.q):
                        self.runningQueue.add(self.readyQueue.remove())
                    else:
                        break
                except Exception as e:
                    print("############## EXCEPTION in FCFS run_ts cpu_burst ################")
                    print(e)
                    break
 
        self.waitQueue.incrementTime()
        io_releases = self.ioQueue.incrementTime()
        
        #print("io released jobs :: ", io_releases)
        
        #add jobs to io queue
        for i in released_jobs:
            if i not in completed_jobs:
                self.waitQueue.add(i)
        
        for i in io_releases:
            self.readyQueue.add(i)

        if len(self.waitQueue.q):
            while len(self.ioQueue.q) < NUM_IO_DEVICES:
                try:
                    if len(self.waitQueue.q):
                        self.ioQueue.add(self.waitQueue.remove())
                    else:
                        break
                except Exception as e:
                    print("############## EXCEPTION in FCFS run_ts io_burst ################")
                    print(e)
                    break

        for job in completed_jobs:
            self.terminatedQueue.add(completed_jobs)
        
        results = print_ques(self)
        #print("time step = ",self.time , "\n")
        #print(results)
        self.buffer.insert_text("Priority Based \n")
        self.buffer.insert_text("time step = "+ str(self.time) + "\n")
        self.buffer.insert_text(results + "\n")
        released_jobs = [str(i) for i in released_jobs]
        self.buffer.insert_text("Released jobs = "+ ",".join(released_jobs)+ "\n")
        io_releases = [str(i) for i in io_releases]
        self.buffer.insert_text("IO releases = "+ ",".join(io_releases) + "\n")
        return results

class Simulator:
    def __init__(self, data):
        self.data = data
        self.schedulers = []
        self.global_time = 0        
        
        #create schedulers
        self.schedulers.append(FCFS(data, fcfs_buffer))
        self.schedulers.append(SJF(data,sjf_buffer))
        self.schedulers.append(SRT(data,srt_buffer))
        self.schedulers.append(RR(data,rr_buffer))
        self.schedulers.append(PB(data,pb_buffer))


    def run_time_step(self):
        #print("Global time step - " + str(self.global_time))
        results = []
        for scheduler in self.schedulers:
            results.append(scheduler.run_ts())
            #print(scheduler)
        return results
    
    def run_simulation(self):
        global Pause
        while True:
            if Pause:
                Pause = False
                return
            else:
                results = self.run_time_step()
                #print(results)
            sleep(2)

def update_results(results):
    #update labels and progressbars
    pass

#if __name__ == "__main__":

simulator = Simulator(load_data())
simulator_thread = threading.Thread(target = simulator.run_simulation)
#######################################

root_container = HSplit([
    VSplit([
        # One window that holds the BufferControl with the default buffer on
        # the left.
        fcfs_window,
        # A vertical line in the middle. We explicitly specify the width, to
        # make sure that the layout engine will not try to divide the whole
        # width by three for all these windows. The window will simply fill its
        # content by repeating this character.
        Window(width=1, char='|', style="class:left"),

        # Display the text 'Hello world' on the right.
        sjf_window,
    ]),
    
    Window(height=1, char='-', style="class:left"),

    VSplit([
        # One window that holds the BufferControl with the default buffer on
        # the left.
        srt_window,
        # A vertical line in the middle. We explicitly specify the width, to
        # make sure that the layout engine will not try to divide the whole
        # width by three for all these windows. The window will simply fill its
        # content by repeating this character.
        Window(width=1, char='|', style="class:left"),

        # Display the text 'Hello world' on the right.
        rr_window,
    ]), 
    
    Window(height=1, char='-', style="class:left"),
    
    VSplit([
        # One window that holds the BufferControl with the default buffer on
        # the left.
        pb_window,
        # A vertical line in the middle. We explicitly specify the width, to
        # make sure that the layout engine will not try to divide the whole
        # width by three for all these windows. The window will simply fill its
        # content by repeating this character.
        Window(width=1, char='|', style="class:left"),

        # Display the text 'Hello world' on the right.
        pb_window,
    ]), 
])
layout = Layout(root_container)


kb = KeyBindings()

help_str = ""


def run_time_step_dummy():
    #while True:
    fcfs_buffer.insert_text("next event triggered\n", overwrite = True)
    rr_buffer.insert_text("next event triggered and updated\n", overwrite = True)

help_str += """
    Pressing Ctrl-Q will exit the user interface.
"""

@kb.add('c-q')
def exit_(event):
    #Setting a return value means: quit the event loop that drives the user
    #interface and return this value from the `Application.run()` call.
    event.app.exit()


help_str += """
    Pressing Ctrl-p will pause simulatior run
"""
@kb.add('c-p')
def exit_(event):
    global Pause
    global simulator_thread 
    simulator_thread = threading.Thread(target = simulator.run_simulation)
    Pause = True


help_str += """
    Pressing Ctrl-s will run simulation 
"""
@kb.add('c-s')
def exit_(event):
    simulator_thread.start()

help_str += """
    Pressing Ctrl-n will run next time step in simulation
"""
@kb.add('c-n')
def exit_(event):
    #schedulers.Pause = True
    #run_time_step_dummy()
    simulator.run_time_step()

if len(sys.argv)> 1:
    print(help_str)
    sys.exit()

#test = threading.Thread(target = run_time_step_dummy )
#test.start()


#######################################



'''
for i in range(2000):
    results = simulator.run_time_step()
    print(results)
'''
app = Application(layout=layout, key_bindings=kb, full_screen=True, color_depth=ColorDepth.DEPTH_24_BIT, style=style)
app.run() # You won't be able to Exit this app
    

    

