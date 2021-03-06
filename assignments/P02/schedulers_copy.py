from hashlib import new
from platform import release
from main import IoQueue, Pcb,JobStateQueue,ReadyQueue,WaitQueue,RunningQueue,TerminatedQueue
from simulate import *
from config import *
import time

NewQueue = JobStateQueue()

Pause = False

def print_ques(scheduler_obj):
    return_str = ""
    return_str += str(scheduler_obj.newQueue)
    return_str += str(scheduler_obj.readyQueue) 
    return_str += str(scheduler_obj.waitQueue) 
    return_str += str(scheduler_obj.runningQueue)
    return_str += str(scheduler_obj.ioQueue)
    return_str += str(scheduler_obj.terminatedQueue)
    return return_str

class FCFS:
    def __init__(self, data):
        self.data = data
        self.time = 0
        self.newQueue = NewQueue 
        self.readyQueue = ReadyQueue ()
        self.waitQueue = WaitQueue ()
        self.runningQueue = RunningQueue ()
        self.ioQueue = IoQueue ()
        self.terminatedQueue = TerminatedQueue ()

    def run_ts(self):
        #update time
        self.time += 1

        #fill QUEUES
        self.newQueue.extend([i for i in self.data if (i.arrivalTime == self.time)])
        self.readyQueue.incrementTime()
        self.readyQueue.extend(self.newQueue.q)
        self.newQueue.emptyq()

        released_jobs = self.runningQueue.incrementTime()
        print("released jobs :: ", released_jobs)
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
        
        print("io released jobs :: ", io_releases)
        
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
            self.terminatedQueue.append(completed_jobs)
        
        results = print_ques(self)
        print("time step = ",self.time , "\n")
        print(results)
        time.sleep(3)
        return results



class SJF:
    def __init__(self, data):
        self.data = data
        self.time = 0
    

class RR:
    def __init__(self, data):
        self.data = data
        self.time = 0

class PB:
    def __init__(self, data):
        self.data = data
        self.time = 0

class Simulator:
    def __init__(self, data):
        self.data = data
        self.schedulers = []
        self.global_time = 0        
        #create schedulers
        self.schedulers.append(FCFS(data))
        '''
        self.schedulers.append(SJF(data))
        self.schedulers.append(RR(data))
        self.schedulers.append(PB(data))
        '''


    def run_time_step(self):
        print("Global time step - " + str(self.global_time))
        results = []
        for scheduler in self.schedulers:
            results.append(scheduler.run_ts())
            #print(scheduler)
        return results
    
    def run_simulation(self):
        while True:
            if Pause:
                Pause = False
                return
            else:
                results = self.run_time_step()
                print(results)

def update_results(results):
    #update labels and progressbars
    pass
if __name__ == "__main__":
    simulator = Simulator(load_data())
    
    for i in range(20):
        results = simulator.run_time_step()
        print(results)

    

