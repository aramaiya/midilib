class Midi:

    def __init__(self, file):
        self.midifile = None
        self.formattype = 0
        self.trackcount = 0
        self.timedivision = 0
        self.metadata = {}

        with open(file, 'rb') as self.midifile:
            self._readheader()
            for _ in range(self.trackcount):
                self._readtrack()

    def _readheader(self):
        header_chunkid = self.midifile.read(4).decode('utf-8')
        self.metadata["header chunk id"] = header_chunkid

        if header_chunkid != 'MThd':
            print('not midi file')
            return

        header_chunksize = int.from_bytes(self.midifile.read(4), byteorder='big')
        self.metadata["header chunk size"] = header_chunksize

        self.formattype = int.from_bytes(self.midifile.read(2), byteorder='big')
        self.metadata["format type"] = self.formattype

        self.trackcount = int.from_bytes(self.midifile.read(2), byteorder='big')
        self.metadata["track count"] = self.trackcount

        self.timedivision = int.from_bytes(self.midifile.read(2), byteorder='big')
        self.metadata["time division"] = self.timedivision

    def _readtrack(self):
        track_chunkid = self.midifile.read(4).decode('utf-8')
        print("track chunk id: %s" % track_chunkid)

        track_chunksize = int.from_bytes(self.midifile.read(4), byteorder='big')
        print("track chunk size: %d" % track_chunksize)

        #todo: can track chunk size = 0?

        bytecount = 1

        while bytecount <= track_chunksize:
            delta_time = 0
            byteval = int.from_bytes(self.midifile.read(1), byteorder='big')

            bytecount += 1

            while (byteval & 128) != 0:
                delta_time = (delta_time << 7) + (byteval - 128)
                byteval = int.from_bytes(self.midifile.read(1), byteorder='big')

                bytecount += 1

            delta_time = (delta_time << 7) + byteval

            print("delta time: %d" % delta_time)

            event_type = int.from_bytes(self.midifile.read(1), byteorder='big')
            bytecount += 1
            print("event type: %s" % hex(event_type))

            if event_type == 255:
                meta_event_command = int.from_bytes(self.midifile.read(1), byteorder='big')

                #print("event command: %s" % hex(meta_event_command))
                meta_event_length = int.from_bytes(self.midifile.read(1), byteorder='big')

                event_params = self.midifile.read(meta_event_length)
                #print("event params: %s" % str(list(event_params)))
                bytecount += meta_event_length + 1 + 1

            elif 192 <= event_type <= 223:
                data_1 = int.from_bytes(self.midifile.read(1), byteorder='big')
                #print("data1: %d" % data_1)
                bytecount += 1

            else:
                data_1 = int.from_bytes(self.midifile.read(1), byteorder='big')
                data_2 = int.from_bytes(self.midifile.read(1), byteorder='big')
                print("data1: %s" % note(data_1))
                print("data2: %d" % data_2)
                bytecount += 2

    def __str__(self):
        return str(self.metadata)


def note(num):

    if num < 0 or num > 127:
        raise ValueError("Involid note code")

    notes = {
        0: 'C',
        1: 'C#',
        2: 'D',
        3: 'D#',
        4: 'E',
        5: 'F',
        6: 'F#',
        7: 'G',
        8: 'G#',
        9: 'A',
        10: 'A#',
        11: 'B'
    }

    return notes[num % 12] + ' ' + str(int(num / 12))

print(Midi('/users/amit/downloads/a-major-scale.mid'))

