import globals

class Maddy_History:
    def __init__(self):
        self.history_path = globals.history_path #"/home/prithvi/.maddy_history"
        with open(self.history_path, "r") as fd:
            self.HISTORY = fd.readlines()
            self.HISTORY = [ i.strip() for i in self.HISTORY if i]
        #self.HISTORY = ["ls -lrt", "history", "whoami", "hostname", "ps -eaf" , "du -skh", "scp -r "]
        self.MAX_HISTORY_LEN = 30
        self.curr_index = len(self.HISTORY) -1
    
    def __del__ (self):
        with open(self.history_path, "w") as fd:
            fd.write("\n".join(self.HISTORY))

    def update_curr_index(self):
        self.curr_index = len(self.HISTORY) - 1

    def add(self,cmd):
        if cmd:
            self.HISTORY.append(cmd)
            self.update_curr_index()
            #print("added command to history :: ")
            #print(cmd)
            #print(self.HISTORY)

    def rev_search(self,cmd):
        self.curr_index , matching_command = [ (idx,s) for idx, s in enumerate(HISTORY[:-1]) if s.startswith(cmd)][0]
        return matching_command

    def prev_cmd(self, curr_command):
        prev_cmd = self.HISTORY[self.curr_index]
        if self.curr_index > 0:
            self.curr_index -= 1
        return prev_cmd

    def next_cmd(self):
        next_cmd = self.HISTORY[self.curr_index]
        if (self.curr_index < self.MAX_HISTORY_LEN-1) and (self.curr_index < len(self.HISTORY)-1):
            self.curr_index += 1
        return next_cmd


