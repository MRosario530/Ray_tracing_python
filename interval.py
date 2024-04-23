
class Interval:

    def __init__(self, min, max):
        self.min = min
        self.max = max

    def contains(self, x):
        return (self.min <= x) and (x <= self.max)
    
    def surrounds(self, x):
        return (self.min < x) and (x < self.max)
    
    def clamp(self, x):
        if (x < self.min):
            return self.min
        if (x > self.max):
            return self.max
        return x