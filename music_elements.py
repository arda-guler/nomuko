class Note():
    def __init__(self, midi_num, duration, start_time):
        self.midi_num = midi_num
        self.duration = duration
        self.start_time = start_time

    def get_midi_num(self):
        return self.midi_num

    def get_duration(self):
        return self.duration

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.start_time + self.duration

class Bar():
    def __init__(self, start_time, measure = 4, notes = []):
        self.start_time = start_time
        self.measure = measure
        self.notes = notes

    def get_start_time(self):
        return self.start_time

    def get_measure(self):
        return self.measure

    def get_notes(self):
        return self.notes

    def add_note(self, note):
        self.notes.append(note)

    def delete_note(self, note):
        self.notes.remove(note)
        del note

class Piece():
    def __init__(self, bpm = 120, bars = []):
        self.bpm = bpm
        self.bars = bars

# first 21 midi notes are below A0
note_names = ["", "", "", "", "", "", "", "", "", "", "",
              "", "", "", "", "", "", "", "", "", "",
              "A0", "A#0", "B0",
              "C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1", "G#1", "A1", "A#1", "B1",
              "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2", "A2", "A#2", "B2",
              "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3",
              "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4",
              "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5",
              "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6", "B6",
              "C7", "C#7", "D7", "D#7", "E7", "F7", "F#7", "G7", "G#7", "A7", "A#7", "B7",
              "C8", "C#8", "D8", "D#8", "E8", "F8", "F#8", "G8", "G#8", "A8", "A#8", "B8",
              "C9", "C#9", "D9", "D#9", "E9", "F9", "F#9", "G9"]
