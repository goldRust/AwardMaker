

class Award:
    def __init__(self, first, last, event, place):
        self.first = first
        self.last = last
        self.event = event
        self.place = place

    def get_name(self):
        return self.first + ' ' + self.last
