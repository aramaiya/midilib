class Midi:

    def __init__(self):
        self.midifile = None
        self.formattype = 0
        self.trackcount = 0
        self.timedivision = 0

    def load_from_file(self, file):
        with open(file, 'rb') as self.midifile:
            self._readheader()
            self._readtrack()
            #self._readtrack()

    def _readheader(self):
        header_chunkid = self.midifile.read(4).decode('utf-8')
        print("header chunk id: %s" % header_chunkid)

        if header_chunkid != 'MThd':
            print('not midi file')
            return

        header_chunksize = int.from_bytes(self.midifile.read(4), byteorder='big')
        print("header chunk size: %d" % header_chunksize)

        self.formattype = int.from_bytes(self.midifile.read(2), byteorder='big')
        print("format type: %d" % self.formattype)

        self.trackcount = int.from_bytes(self.midifile.read(2), byteorder='big')
        print("number of tracks: %d" % self.trackcount)

        self.timedivision = int.from_bytes(self.midifile.read(2), byteorder='big')
        print("time division: %d" % self.timedivision)

    def _readtrack(self):
        track_chunkid = self.midifile.read(4).decode('utf-8')
        print("track chunk id: %s" % track_chunkid)

        track_chunksize = int.from_bytes(self.midifile.read(4), byteorder='big')
        print("track chunk size: %d" % track_chunksize)

        #todo: can track chunk size = 0?

        delta_time = 0

        byteval = int.from_bytes(self.midifile.read(1), byteorder='big')

        while (byteval & 128) != 0:
            delta_time = (delta_time << 7) + (byteval - 128)
            byteval = int.from_bytes(self.midifile.read(1), byteorder='big')

        delta_time = (delta_time << 7) + byteval

        print("delta time: %s" % delta_time)


class Track:

    def __init__(self):
        self.deltatime = 0



Midi().load_from_file('/users/amit/downloads/c-major-scale.mid')