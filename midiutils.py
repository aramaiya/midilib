def code2note(num):

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


def note2code(note): #todo fix
    return
    raise ValueError("Invalid note")