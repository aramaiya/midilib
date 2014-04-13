from midiio import MidiReader, MidiWriter
from note import Note


class Midi:

    def __init__(self, file):
        self.midifile = None
        self.formattype = 0
        self.trackcount = 0
        self.timedivision = 0
        self.metadata = {}

        self.tracks = []

        if file is not None:
            MidiReader(self).read(file)

    def __str__(self):
        return str(self.metadata)

    def save(self, filename):
        MidiWriter(self).write(filename)


if __name__ == "__main__":
    midi = Midi('/users/amit/downloads/c-major-scale.mid')
    note = Note('C# 5', 10, 0)
    midi.tracks[1].append(note)
    midi.tracks[1].append(note)
    midi.tracks[1].insert(note, 10)
    print(list(zip([(note.note, note.duration, note.velocity) for note in midi.tracks[1].notes], midi.tracks[1].times)))
    print(midi)
    midi.save('/users/amit/downloads/c-major.mid')
