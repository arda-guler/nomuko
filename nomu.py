## MIDI CREATING THINGIE

from tkinter import *
from midiutil import MIDIFile

from music_elements import *

duration_to_length_factor = 300
y_offset_factor = 20

# this is a virtual "camera" to move the view around the grid
class camera():
    def __init__(self, pos=[200,300], zoom=0.5):
        self.pos = pos
        self.zoom = zoom

    def get_x(self):
        return self.pos[0]

    def get_y(self):
        return self.pos[1]

    def get_zoom(self):
        return self.zoom

    def move(self, movement):
        self.pos[0] += movement[0]
        self.pos[1] += movement[1]

    def zoom_in(self, factor):
        self.zoom *= 1/factor

    def zoom_out(self, factor):
        self.zoom *= factor

# convert camera coords to canvas coords
def camera2canvas(x, y, a_cam, canvas_size_x = 900, canvas_size_y = 500):
    
    canvas_x = (x - a_cam.get_x())/a_cam.get_zoom() + canvas_size_x/2
    canvas_y = (-y + a_cam.get_y())/a_cam.get_zoom() + canvas_size_y/2
    
    return canvas_x, canvas_y

# convert canvas coords to camera coords
def canvas2camera(x, y, a_cam, canvas_size_x = 900, canvas_size_y = 500):
    
    camera_x = (x - canvas_size_x/2)*a_cam.get_zoom() + a_cam.get_x()
    camera_y = -((y - canvas_size_y/2)*a_cam.get_zoom() - a_cam.get_y())
    
    return camera_x, camera_y

def duration2length(duration):
    global duration_to_length_factor
    return duration * duration_to_length_factor

def main():

    global duration_to_length_factor, y_offset_factor

    def canvas_y_to_midi_num(y):
        return int((y + 980)/y_offset_factor)

    def move_cam_up(event=None):
        main_cam.move([0, 30 * main_cam.get_zoom()])
    def move_cam_down(event=None):
        main_cam.move([0, -30 * main_cam.get_zoom()])
    def move_cam_right(event=None):
        main_cam.move([30 * main_cam.get_zoom(), 0])
    def move_cam_left(event=None):
        main_cam.move([-30 * main_cam.get_zoom(), 0])
    def zoom_cam_out(event=None):
        main_cam.zoom_out(2)
    def zoom_cam_in(event=None):
        main_cam.zoom_in(2)

    def create_note(x, y):
        new_note = Note(canvas_y_to_midi_num(y), float(duration_field.get("1.0","end-1c")), x/duration_to_length_factor)
        bar_found = False
        for bar in bars:
            if bar.get_start_time() + 1 >= new_note.get_start_time() >= bar.get_start_time():
                bar.add_note(new_note)
                bar_found = True
                break

        # no bar at the requested location - create some!
        if not bar_found:
            # find last bar
            last_bar = None
            for bar in bars:
                if not last_bar or bar.get_start_time() > last_bar.get_start_time():
                    last_bar = bar

            # if there are no bars at all, start with the very first
            if not last_bar:
                last_bar = Bar(0, int(measure_field.get("1.0","end-1c")))
                bars.append(last_bar)

            # keep creating bars until we reach the point where the note needs to be
            for i in range(int(new_note.get_start_time() - last_bar.get_start_time()) + 1):
                new_bar = Bar(last_bar.get_start_time() + 1, int(measure_field.get("1.0","end-1c")))
                bars.append(new_bar)
                last_bar = new_bar

            last_bar.add_note(new_note)

    def delete_note(x, y):
        closest_note = None
        
        for bar in bars:
            for note in bar.get_notes():
                if ((not closest_note) or
                    (((closest_note.get_start_time() - x/duration_to_length_factor)**2 + (closest_note.get_midi_num() - canvas_y_to_midi_num(y))**2) >
                    ((note.get_start_time() - x/duration_to_length_factor)**2 + (note.get_midi_num() - canvas_y_to_midi_num(y))**2))):
                    closest_note = note

        if closest_note:
            for bar in bars:
                if bar.get_start_time() + 1 >= closest_note.get_start_time() >= bar.get_start_time():
                    bar.delete_note(closest_note)
                    del closest_note
                    break

    def left_clicked_on_canvas(event):
        x, y = canvas2camera(event.x, event.y, main_cam)

        if click_op.get() == "cn":
            create_note(x, y)

        elif click_op.get() == "dn":
            delete_note(x, y)
        
    def right_clicked_on_canvas(event):
        pass
        
    ## init UI
    root = Tk()
    root.title("Nomu")
    root.geometry("1150x600")

    tk_canvas = Canvas(root, width=900, height=500, bg="white")
    tk_canvas.grid(row=1, column=1, rowspan=15, columnspan=5)

    click_op = StringVar(root, "cn")
    click_op_cp = Radiobutton(root, text="Create Note", value="cn", var = click_op)
    click_op_dp = Radiobutton(root, text="Delete Note", value="dn", var = click_op)

    click_op_label = Label(root, text="Mouse Click Operation")
    click_op_label.grid(row=0, column=6)

    click_op_cp.grid(row=1, column=6)
    click_op_dp.grid(row=2, column=6)

    duration_field_label = Label(root, text="Note Duration")
    duration_field_label.grid(row=16, column=1)
    duration_field = Text(root, height=1, width=10)
    duration_field.grid(row=17, column=1)

    measure_field_label = Label(root, text="Bar Measure")
    measure_field_label.grid(row=16, column=2)
    measure_field = Text(root, height=1, width=10)
    measure_field.grid(row=17, column=2)

    # init first bar
    bar0 = Bar(0)

    ## init variables
    bars = [bar0]
    main_cam = camera()

    note_creation_buffer = []

    # camera control bindings
    root.bind("<Up>", move_cam_up)
    root.bind("<Down>", move_cam_down)
    root.bind("<Left>", move_cam_left)
    root.bind("<Right>", move_cam_right)
    root.bind("<Control_L>", zoom_cam_out)
    root.bind("<Shift_L>", zoom_cam_in)

    # click bindings
    tk_canvas.bind('<Button-1>', left_clicked_on_canvas)
    tk_canvas.bind('<Button-3>', right_clicked_on_canvas)

    # MAIN LOOP
    while True:

        # draw notes
        for bar in bars:
            for note in bar.get_notes():
                rtx, rty = camera2canvas(duration2length(note.get_start_time()), -1000 + y_offset_factor * (note.get_midi_num() + 2), main_cam)
                rbx, rby = camera2canvas(duration2length(note.get_end_time()), -1000 + y_offset_factor * (note.get_midi_num() + 1), main_cam)
                tk_canvas.create_rectangle(rtx, rty, rbx, rby, fill="green")
        
        # draw grid
        # start by drawing vertical lines to show bars
        for bar in bars:
            ltx, lty = camera2canvas(duration2length(bar.get_start_time()), 250 * main_cam.get_zoom() + main_cam.get_y(), main_cam)
            lbx, lby = camera2canvas(duration2length(bar.get_start_time()), -250 * main_cam.get_zoom() + main_cam.get_y(), main_cam)
            tk_canvas.create_line(ltx, lty, lbx, lby, fill="black")
            tk_canvas.create_text(ltx + 15, lty + 15, text="Bar")

            # lets draw measures within bars
            x_offset = 0
            for i in range(bar.get_measure()):
                x_offset += duration_to_length_factor / bar.get_measure()
                ltx, lty = camera2canvas(duration2length(bar.get_start_time()) + x_offset, 250 * main_cam.get_zoom() + main_cam.get_y(), main_cam)
                lbx, lby = camera2canvas(duration2length(bar.get_start_time()) + x_offset, -250 * main_cam.get_zoom() + main_cam.get_y(), main_cam)
                tk_canvas.create_line(ltx, lty, lbx, lby, fill="gray")

        # now the horizontal lines for notes
        y_offset = 0
        for i in range(128):
            y_offset += y_offset_factor
            llx, lly = camera2canvas(0, -1000 + y_offset, main_cam)
            lrx, lry = camera2canvas(duration2length(bars[-1].get_start_time() + 1), -1000 + y_offset, main_cam)
            if lly >= 50:
                if i > 23 and i % 12 == 0:
                    tk_canvas.create_line(llx, lly, lrx, lry, fill="blue")
                else:
                    tk_canvas.create_line(llx, lly, lrx, lry, fill="black")
                if not i >= 127 and lly - 15 >= 50:
                    if llx > 10:
                        tk_canvas.create_text(llx - 15, lly - 7.5/main_cam.get_zoom(), text=note_names[i])
                    else:
                        tk_canvas.create_text(15, lly - 7.5/main_cam.get_zoom(), text=note_names[i])
        
        root.update()
        tk_canvas.delete("all")
        
    root.mainloop()

main()
