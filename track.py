import bisect


class Track:

    #todo: use avl tree for fast insert. key: time, val: note

    def __init__(self):
        self.notes = []
        self.times = []

    def insert(self, note, time):
        index = bisect.bisect_left(self.times, time)
        self.notes.insert(index, note)
        self.times.insert(index, time)

    def append(self, note):
        lastnote = self.notes[-1]
        lasttime = self.times[-1]

        self.notes.append(note)
        self.times.append(lasttime + lastnote.duration)