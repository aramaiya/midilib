class Midi:

    def __init__(self):
        self.midifile = None
        self.formattype = 0
        self.trackcount = 0
        self.timedivision = 0

    def load_from_file(self, file):

        with open(file, 'rb') as self.midifile:
            self._readheader()

    def _readheader(self):
        header_chunk_id = self.midifile.read(4).decode('utf-8')
        print("header chunk id: " + header_chunk_id)
        if header_chunk_id != 'MThd':
            print('not midi file')
            return

        header_chunk_size = int.from_bytes(self.midifile.read(4), byteorder='big')
        print("header chunk size: %d" % header_chunk_size)

        self.formattype = int.from_bytes(self.midifile.read(2), byteorder='big')
        print("format type: %d" % self.formattype)

        self.trackcount = int.from_bytes(self.midifile.read(2), byteorder='big')
        print("number of tracks: %d" % self.trackcount)

        self.timedivision = int.from_bytes(self.midifile.read(2), byteorder='big')
        print("time division: %d" % self.timedivision)


