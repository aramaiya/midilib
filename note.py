from midiutils import note2code


class Note:

    def __init__(self, note, duration, velocity):
        note2code(note)  # will throw exception if invalid
        self.note = note
        self.duration = duration
        self.velocity = velocity