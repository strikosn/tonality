#!/usr/bin/env python3

import tinysoundfont

synth = tinysoundfont.Synth()
sfid = synth.sfload('FluidR3_GM.sf2')
synth.start(buffer_size=0)

GLOBAL_BANK = 0
GLOBAL_PRESET = 68
KEY_OFFSET = -14
NOTE_ON_KEYMAP = {}
VELOCITY = 80

synth.pitchbend_range(chan=1, semitones=1)
synth.pitchbend(chan=1, value=5461)








import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class Tonality(Gtk.Window):
    def __init__(self):
        super().__init__(title="Tonality")
        self.set_default_size(500, 300)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(20)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.vbox.set_homogeneous(False)  # allows different sizes
        self.add(self.vbox)

        # Label to display pressed keys
        self.keyboard_r2_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
        self.keyboard_r2_hbox.set_homogeneous(True)  # both sides same width
        self.vbox.pack_start(self.keyboard_r2_hbox, False, False, 0)

        self.key_labels = {}

        for scancode in (66, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48):
            label = Gtk.Label()
            label.set_justify(Gtk.Justification.CENTER)
            label.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.95, 0.95, 0.98, 1))
            label.set_padding(20, 20)
            self.keyboard_r2_hbox.pack_start(label, False, False, 0)
            self.key_labels[scancode] = label

        # Label to display instruments
        self.label2 = Gtk.Label()
        self.label2.set_justify(Gtk.Justification.CENTER)
        self.label2.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.95, 0.95, 0.98, 1))
        self.label2.set_padding(20, 20)
        self.vbox.pack_start(self.label2, False, False, 0)

        # Label to display base note
        self.label3 = Gtk.Label()
        self.label3.set_justify(Gtk.Justification.CENTER)
        self.label3.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.95, 0.95, 0.98, 1))
        self.label3.set_padding(20, 20)
        self.vbox.pack_start(self.label3, False, False, 0)

        # Connect keyboard events
        self.connect("key-press-event", self.OnKeyPress)
        self.connect("key-release-event", self.OnKeyRelease)
        self.connect("destroy", Gtk.main_quit)

        # Make window grab focus when clicked
        self.set_focus_on_click(True)
        self.connect("button-press-event", lambda w, e: self.grab_focus())

        self.Reprogram(bank_diff=0, preset_diff=0)
        self.Transpose(diff=0)

    def OnKeyPress(self, widget, event):
        global NOTE_ON_KEYMAP

        #print(event)

        scancode = event.get_scancode()
        keyname = Gdk.keyval_name(event.keyval)

        def NoteOn(chan, key):
            if scancode not in NOTE_ON_KEYMAP:
                NOTE_ON_KEYMAP[scancode] = dict(chan=chan, key=key)
                synth.noteon(chan=chan, key=key, velocity=VELOCITY)

        if scancode == 24:  # ζω+ = si
            NoteOn(chan=0, key=KEY_OFFSET+59)
        if scancode == 27:  # βου+ = mi
            NoteOn(chan=0, key=KEY_OFFSET+64)
        if scancode == 31:  # ζω'+ = si'
            NoteOn(chan=0, key=KEY_OFFSET+71)
        if scancode == 34:  # βου'+ = mi'
            NoteOn(chan=0, key=KEY_OFFSET+76)

        if scancode == 66:  # κε
            NoteOn(chan=0, key=KEY_OFFSET+57)
        if scancode == 38:  # ζω
            NoteOn(chan=1, key=KEY_OFFSET+59)
        if scancode == 39:  # νη
            NoteOn(chan=0, key=KEY_OFFSET+60)
        if scancode == 40:  # πα
            NoteOn(chan=0, key=KEY_OFFSET+62)
        if scancode == 41:  # βου
            NoteOn(chan=1, key=KEY_OFFSET+64)
        if scancode == 42:  # γα
            NoteOn(chan=0, key=KEY_OFFSET+65)
        if scancode == 43:  # δη
            NoteOn(chan=0, key=KEY_OFFSET+67)
        if scancode == 44:  # κε
            NoteOn(chan=0, key=KEY_OFFSET+69)
        if scancode == 45:  # ζω'
            NoteOn(chan=1, key=KEY_OFFSET+71)
        if scancode == 46:  # νη'
            NoteOn(chan=0, key=KEY_OFFSET+72)
        if scancode == 47:  # πα'
            NoteOn(chan=0, key=KEY_OFFSET+74)
        if scancode == 48:  # βου'
            NoteOn(chan=1, key=KEY_OFFSET+76)

        if keyname == 'minus':
            self.Reprogram(bank_diff=0, preset_diff=-1)
        if keyname == 'equal':
            self.Reprogram(bank_diff=0, preset_diff=1)
        if keyname == 'underscore':
            self.Reprogram(bank_diff=-1, preset_diff=0)
        if keyname == 'plus':
            self.Reprogram(bank_diff=1, preset_diff=0)

        if keyname == 'Page_Up':
            self.Transpose(diff=1)
        if keyname == 'Page_Down':
            self.Transpose(diff=-1)

        if scancode in self.key_labels:
            self.key_labels[scancode].override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.45, 0.45, 0.48, 1))

        return False  # Allow further processing (e.g. typing in entry)

    def OnKeyRelease(self, widget, event):
        global NOTE_ON_KEYMAP

        #print(event)

        scancode = event.get_scancode()

        if scancode in NOTE_ON_KEYMAP:
            synth.noteoff(**NOTE_ON_KEYMAP[scancode])
            del NOTE_ON_KEYMAP[scancode]

        if scancode in self.key_labels:
            self.key_labels[scancode].override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.95, 0.95, 0.98, 1))

        return False

    def Reprogram(self, bank_diff, preset_diff):
        global GLOBAL_BANK, GLOBAL_PRESET
        new_bank = GLOBAL_BANK + bank_diff
        new_preset = GLOBAL_PRESET + preset_diff
        name = synth.sfpreset_name(sfid=sfid, bank=new_bank, preset=new_preset)
        if name is not None:
            GLOBAL_BANK = new_bank
            GLOBAL_PRESET = new_preset
            self.label2.set_markup(f'{name} (bank={GLOBAL_BANK}, preset={GLOBAL_PRESET})')
            synth.program_select(chan=0, sfid=sfid, bank=GLOBAL_BANK, preset=GLOBAL_PRESET)
            synth.program_select(chan=1, sfid=sfid, bank=GLOBAL_BANK, preset=GLOBAL_PRESET)
        else:
            print('Not valid program (bank=', GLOBAL_BANK, ', preset=', GLOBAL_PRESET, ')')

    def Transpose(self, diff):
        global KEY_OFFSET
        KEY_OFFSET += diff

        def midi_to_note(midi_number: int) -> str:
            """Convert a MIDI note number to note name with octave (e.g., 60 -> 'C4')."""
            notes = ['C', 'C#/D♭', 'D', 'D#/E♭', 'E', 'F', 'F#/G♭', 'G', 'G#/A♭', 'A', 'A#/B♭', 'B']
            octave = (midi_number // 12) + 4
            note_index = midi_number % 12
            return f"{notes[note_index]}{octave}"

        base_note = midi_to_note(KEY_OFFSET)
        self.label3.set_markup(f'Base note: {base_note}')


# Run the app
app = Tonality()
app.show_all()
app.grab_focus()  # Start with focus
Gtk.main()
