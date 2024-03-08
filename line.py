class Line:
    def __init__(self,start,stop,begin,end):
        self.start = start
        self.stop = stop
        self.begin = begin
        self.end = end
        self.slope = (end - begin)
        