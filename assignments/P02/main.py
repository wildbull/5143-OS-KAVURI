from rich import print
from config import *

class Pcb:
  def __init__(self,line):
    """
    Example Process: 40 76 P4 2 5 6 30 3 20 5 22 7 39 4
      arrivalTime = 40
      pid = 76
      Priority = p4
      cpuBursts = [2, 6, 3, 5, 7, 4]
      ioBursts =  [5,30,20,22,39]
    """
    '''
    data = line.strip().split()
    
    self.arrivalTime = data[0]    # Process arrival time
    self.pid = data[1]            # Process ID
    self.priority = data[2]
    self.CPUWaitTime = 0          # Time in ready queue
    self.IOWaitTime = 0           # Time in wait queue
    
    self.Terminated = 0           # Time process terminated 
    self.TurnAroundTime = 0       # Time from start to finish
    
    self.cpuBursts = []           # list of cpu bursts
    self.ioBursts = []            # list of IO bursts

    # load cpu bursts from the `data` list by slicing
    # past the first 2 values and then grabbing every other value
    for i in range(0,len(data[3:]),2):
      self.cpuBursts.append(int(data[3:][i]))

    # same as above, but starts at location 1 instead of zero so
    # it grabs IO bursts, and not cpu bursts
    for i in range(1,len(data[3:])-1,2):
      self.ioBursts.append(int(data[3:][i]))
    '''
    self.arrivalTime = line["arrivalTime"]    # Process arrival time
    self.pid = line["process_id"]            # Process ID
    self.priority = line["priority"]
    self.CPUWaitTime = 0          # Time in ready queue
    self.IOWaitTime = 0           # Time in wait queue
    
    self.Terminated = 0           # Time process terminated 
    self.TurnAroundTime = 0       # Time from start to finish
    
    self.cpuBursts = line["cpuBursts"]           # list of cpu bursts
    self.ioBursts = line["ioBursts"]            # list of IO bursts

   
    self.cpuUsage = 0
    self.totalCpuNeeded = sum(self.cpuBursts)
    self.currCpuBurst = self.cpuBursts[0]
    self.currIoBurst = self.ioBursts[0]
    self.currBurstIoUsage = 0
    self.currBurstCpuUsage = 0

  def rem_cpu_burst(self):
    if len(self.cpuBursts) > 1:
      self.cpuBursts = self.cpuBursts[1:]
      self.currCpuBurst = self.cpuBursts[0]
      self.currBurstCpuUsage = 0
    else:
      self.cpuBursts = []
      self.currCpuBurst = 0
      self.currBurstCpuUsage = 0

  def rem_io_burst(self):
    if len(self.ioBursts) > 1:
      self.ioBursts = self.ioBursts[1:]
      self.currIoBurst = self.ioBursts[0]
      self.currBurstIoUsage = 0
    else:
      self.ioBursts = []
      self.currIoBurst = 0
      self.currBurstIoUsage = 0   

  def __str__(self):
    """ Prints a "process" out in a readable format. Feel free to
        change the format to whatever you see fit.
    """
    s = f'At: {self.arrivalTime}, Pid: {self.pid}\n'
    s += f'CpuBursts: {self.cpuBursts} , \nIoBursts: {self.ioBursts}\n'
    s += f'CPUWaitTime: {self.CPUWaitTime} , IOWaitTime: {self.IOWaitTime}\n'
    return s

  def __repr__(self):
    return self.__str__()

# The 5 States needed to be represented: 
#   - newQueue
#   - readyQueue
#   - runningQueue
#   - waitQueue
#   - terminatedQueue

class JobStateQueue:
  """ Generic state queue. Should be extended to add specific functionality
      for whichever queue you are implementing (see below)
  """
  def __init__(self):
    self.q = []

  def add(self,pcb):
    self.q.append(pcb)

  def remove(self):
    temp = self.q[0]
    self.q = self.q[1:]
    return temp

  def print(self,max=None):
    if not max:
      max = len(self.q)
    #print(self.q[:max])
    return str(self.q[:max])

  def length(self):
    return len(self.q)

  def extend(self, lst):
    self.q.extend(lst)
  
  def emptyq(self):
    self.q = []
  
  def sort(self,criterian):
    if criterian == "total_cpu_time":
      self.q.sort(key = lambda x: x.totalCpuNeeded)
    elif criterian == "cpu_time_left":
      self.q.sort(key = lambda x: sum(x.cpuBursts))
    elif criterian == "priority":
      self.q.sort(key = lambda x: x.priority)
    else:
      print("unknown sort criterian :: ", criterian)
    
    return

  def __str__(self):
    s = f'{self.__class__.__name__} Items: {len(self.q)} \n'
    return s
    
class ReadyQueue(JobStateQueue):
  """ Holds processes ready to run on cpu
  """
  def __init__(self):
    super().__init__()

  def incrementTime(self):
    for p in self.q:
      p.CPUWaitTime += 1

class WaitQueue(JobStateQueue):
  """ Holds processes waiting for IO device
  """
  def __init__(self):
    super().__init__()

  def incrementTime(self):
    for p in self.q:
      p.IOWaitTime += 1
  
class IoQueue(JobStateQueue):
  """ Holds processes waiting for IO device
  """
  def __init__(self):
    super().__init__()
  
  def incrementTime(self):
    IO_burst_completed = []
    for p in self.q:
      p.IOWaitTime += 1
      p.currBurstIoUsage += 1
      #print("io burst details")
      #print(p.currBurstIoUsage, p.currIoBurst)
      if not p.currBurstIoUsage < p.currIoBurst:
        p.rem_io_burst()
        IO_burst_completed.append(p)
        self.q.remove(p)
    return(IO_burst_completed)

class TerminatedQueue(JobStateQueue):
  """ Holds processes waiting for IO device
  """
  def __init__(self):
    super().__init__()
 
class RunningQueue(JobStateQueue):
  """ Holds processes waiting for IO device
  """
  def __init__(self):
    super().__init__()

  def incrementTime(self):
    completed_processes = []
    for p in self.q:
      p.cpuUsage += 1
      p.currBurstCpuUsage += 1
      #print("cpu burst details")
      #print(p.currBurstCpuUsage, p.currCpuBurst)
      if not p.currBurstCpuUsage < p.currCpuBurst :
        #print("burst completed")
        p.rem_cpu_burst()
        completed_processes.append(p)
        self.q.remove(p)
    
    return completed_processes

  

if __name__=='__main__':
  NewQueue = JobStateQueue()
  with open('infile.dat') as f:
    lines = f.read().splitlines()
    for line in lines:
      NewQueue.add(Pcb(line))

  readyQueue = ReadyQueue()
  waitQueue = WaitQueue()  


  NewQueue.print(5)

  print(NewQueue.length())

  for i in range(5):
    pcb = NewQueue.remove()
    readyQueue.add(pcb)

  readyQueue.print(5)
  readyQueue.incrementTime()

  readyQueue.print(5)

  print(readyQueue)
