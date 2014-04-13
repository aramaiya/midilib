from midiutils import code2note
from note import Note
from track import Track


class MidiReader:

    def __init__(self, midi):
        self.midi = midi
        self.midifile = None

    def read(self, filename):

        with open(filename, 'rb') as self.midifile:
            self._readheader()
            for _ in range(self.midi.metadata['track count']):
                self._readtrack()

    def _readheader(self):
        header_chunkid = self.midifile.read(4).decode('utf-8')
        self.midi.metadata["header chunk id"] = header_chunkid

        if header_chunkid != 'MThd':
            print('not midi file')
            return

        header_chunksize = int.from_bytes(self.midifile.read(4), byteorder='big')
        self.midi.metadata["header chunk size"] = header_chunksize

        formattype = int.from_bytes(self.midifile.read(2), byteorder='big')
        self.midi.metadata["format type"] = formattype

        trackcount = int.from_bytes(self.midifile.read(2), byteorder='big')
        self.midi.metadata["track count"] = trackcount

        timedivision = int.from_bytes(self.midifile.read(2), byteorder='big')
        self.midi.metadata["time division"] = timedivision

    def _readtrack(self):
        track = Track()

        track_chunkid = self.midifile.read(4).decode('utf-8')
        print("track chunk id: %s" % track_chunkid)

        track_chunksize = int.from_bytes(self.midifile.read(4), byteorder='big')
        print("track chunk size: %d" % track_chunksize)

        #todo: can track chunk size = 0?

        bytecount = 1
        open_notes = {}

        time = 0

        while bytecount <= track_chunksize:
            delta_time = 0
            byteval = int.from_bytes(self.midifile.read(1), byteorder='big')

            bytecount += 1

            while (byteval & 128) != 0:
                delta_time = (delta_time << 7) + (byteval - 128)
                byteval = int.from_bytes(self.midifile.read(1), byteorder='big')

                bytecount += 1

            delta_time = (delta_time << 7) + byteval

            event_type = int.from_bytes(self.midifile.read(1), byteorder='big')
            bytecount += 1

            time += delta_time

            if event_type == 255:
                meta_event_command = int.from_bytes(self.midifile.read(1), byteorder='big')

                meta_event_length = int.from_bytes(self.midifile.read(1), byteorder='big')

                event_params = self.midifile.read(meta_event_length)

                bytecount += meta_event_length + 1 + 1

            elif 192 <= event_type <= 223:
                data_1 = int.from_bytes(self.midifile.read(1), byteorder='big')
                print("data1: %d" % data_1)
                bytecount += 1

            else:
                data_1 = int.from_bytes(self.midifile.read(1), byteorder='big')
                data_2 = int.from_bytes(self.midifile.read(1), byteorder='big')
                if 144 <= event_type <= 160:

                    note = Note(code2note(data_1), 0, data_2)

                    if note.note not in open_notes:
                        track.insert(note, time)
                        open_notes[note.note] = {'note': note, 'time': time}

                elif 128 <= event_type <= 143:

                    if code2note(data_1) in open_notes:
                        popped = open_notes.pop(code2note(data_1))
                        note = popped['note']
                        note.duration = time - popped['time']

                else:
                    pass

                bytecount += 2
        for key in open_notes:
            popped = open_notes[key]
            note = popped["note"]
            note.duration = time - popped["time"]
        self.midi.tracks.append(track)


class MidiWriter:

    def __init__(self, midi):
        self.midi = midi

    def write(self, filename):

        with open(filename, 'wb') as fi:
            fi.write(b'Mthd')
            fi.write((self.midi.metadata["header chunk size"]).to_bytes(4, byteorder='big'))
            fi.write((self.midi.metadata["format type"]).to_bytes(2, byteorder='big'))
            fi.write((self.midi.metadata["track count"]).to_bytes(2, byteorder='big'))
            fi.write((self.midi.metadata["time division"]).to_bytes(2, byteorder='big'))

            for _ in range(self.midi.metadata["track count"]):
                fi.write(b'MTrk')
