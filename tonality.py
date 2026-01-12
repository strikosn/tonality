#!/usr/bin/env python3

import collections
import gi
import tinysoundfont

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

synth = tinysoundfont.Synth()
sfid = synth.sfload('FluidR3_GM.sf2')
synth.start(buffer_size=0)

GLOBAL_BANK = 0
GLOBAL_PRESET = 68
KEY_OFFSET = -14
NOTE_ON_KEYMAP = {}
VELOCITY = 80

synth.pitchbend_range(chan=1, semitones=1)
synth.pitchbend(chan=1, value=5461)  # -2/72

synth.pitchbend_range(chan=2, semitones=1)
synth.pitchbend(chan=2, value=2731)  # -4/72


KeyboardKey = collections.namedtuple('KeyboardKey', [
    'scan_code', 'key_row', 'midi_channel', 'relative_midi_key',
])


KEYBOARD_B = [
    KeyboardKey(scan_code=66, key_row=2, midi_channel=2, relative_midi_key=57),  # Caps Lock
    KeyboardKey(scan_code=38, key_row=2, midi_channel=1, relative_midi_key=59),  # A
    KeyboardKey(scan_code=39, key_row=2, midi_channel=0, relative_midi_key=60),  # S
    KeyboardKey(scan_code=40, key_row=2, midi_channel=2, relative_midi_key=62),  # D
    KeyboardKey(scan_code=41, key_row=2, midi_channel=1, relative_midi_key=64),  # F
    KeyboardKey(scan_code=42, key_row=2, midi_channel=0, relative_midi_key=65),  # G
    KeyboardKey(scan_code=43, key_row=2, midi_channel=0, relative_midi_key=67),  # H
    KeyboardKey(scan_code=44, key_row=2, midi_channel=2, relative_midi_key=69),  # J
    KeyboardKey(scan_code=45, key_row=2, midi_channel=1, relative_midi_key=71),  # K
    KeyboardKey(scan_code=46, key_row=2, midi_channel=0, relative_midi_key=72),  # L
    KeyboardKey(scan_code=47, key_row=2, midi_channel=2, relative_midi_key=74),  # ; / :
    KeyboardKey(scan_code=48, key_row=2, midi_channel=1, relative_midi_key=76),  # ' / "
]

KEYBOARD_PLD = [
    KeyboardKey(scan_code=24, key_row=1, midi_channel=0, relative_midi_key=59),  # Q
    KeyboardKey(scan_code=27, key_row=1, midi_channel=0, relative_midi_key=64),  # R
    KeyboardKey(scan_code=31, key_row=1, midi_channel=0, relative_midi_key=71),  # I
    KeyboardKey(scan_code=34, key_row=1, midi_channel=0, relative_midi_key=76),  # ]

    KeyboardKey(scan_code=66, key_row=2, midi_channel=0, relative_midi_key=57),  # Caps Lock
    KeyboardKey(scan_code=38, key_row=2, midi_channel=1, relative_midi_key=59),  # A
    KeyboardKey(scan_code=39, key_row=2, midi_channel=0, relative_midi_key=60),  # S
    KeyboardKey(scan_code=40, key_row=2, midi_channel=0, relative_midi_key=62),  # D
    KeyboardKey(scan_code=41, key_row=2, midi_channel=1, relative_midi_key=64),  # F
    KeyboardKey(scan_code=42, key_row=2, midi_channel=0, relative_midi_key=65),  # G
    KeyboardKey(scan_code=43, key_row=2, midi_channel=0, relative_midi_key=67),  # H
    KeyboardKey(scan_code=44, key_row=2, midi_channel=0, relative_midi_key=69),  # J
    KeyboardKey(scan_code=45, key_row=2, midi_channel=1, relative_midi_key=71),  # K
    KeyboardKey(scan_code=46, key_row=2, midi_channel=0, relative_midi_key=72),  # L
    KeyboardKey(scan_code=47, key_row=2, midi_channel=0, relative_midi_key=74),  # ; / :
    KeyboardKey(scan_code=48, key_row=2, midi_channel=1, relative_midi_key=76),  # ' / "
]


KEYBOARD = KEYBOARD_PLD


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
        self.keyboard_r1_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
        self.keyboard_r1_hbox.set_homogeneous(True)  # both sides same width
        self.vbox.pack_start(self.keyboard_r1_hbox, False, False, 0)
        self.keyboard_r2_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
        self.keyboard_r2_hbox.set_homogeneous(True)  # both sides same width
        self.vbox.pack_start(self.keyboard_r2_hbox, False, False, 0)

        self.key_labels = {}

        for keyboard_key in KEYBOARD:
            if keyboard_key.key_row == 1:
                this_keyboard_hbox = self.keyboard_r1_hbox
            if keyboard_key.key_row == 2:
                this_keyboard_hbox = self.keyboard_r2_hbox

            label = Gtk.Label()
            label.set_justify(Gtk.Justification.LEFT)
            label.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.95, 0.95, 0.98, 1))
            label.set_padding(20, 20)
            this_keyboard_hbox.pack_start(label, False, False, 0)
            self.key_labels[keyboard_key.scan_code] = label

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

        for keyboard_key in KEYBOARD:
            if keyboard_key.scan_code == scancode:
                this_keyboard_key = keyboard_key
                break
        else:
            this_keyboard_key = None

        if this_keyboard_key is not None and scancode not in NOTE_ON_KEYMAP:
            chan = this_keyboard_key.midi_channel
            key = KEY_OFFSET + this_keyboard_key.relative_midi_key
            NOTE_ON_KEYMAP[scancode] = dict(chan=chan, key=key)
            synth.noteon(chan=chan, key=key, velocity=VELOCITY)

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
            synth.program_select(chan=2, sfid=sfid, bank=GLOBAL_BANK, preset=GLOBAL_PRESET)
        else:
            print('Not valid program (bank=', GLOBAL_BANK, ', preset=', GLOBAL_PRESET, ')')

    def Transpose(self, diff):
        global KEY_OFFSET
        KEY_OFFSET += diff

        def midi_to_note(midi_number: int) -> str:
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
