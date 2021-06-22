class Demand:
    def __init__(self , src, dest, bw):
        self.src = src
        self.dest = dest
        self.bw = bw
        self.path = [src, dest]

    def insert(self, position, node):
        self.path.insert(position, node)
    
    def replace(self, position, node):
        self.replace(position, node)
        
    def remove(self, position):
        self.path.pop(position)

    def reset(self):
        self.path = [self.src, self.dest]

 

