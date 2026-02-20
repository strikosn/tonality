#!/usr/bin/env python3

import collections
import gi
import mido
import tinysoundfont

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

synth = tinysoundfont.Synth()
sfid = synth.sfload('/usr/share/sounds/sf2/FluidR3_GM.sf2')

midi_port = mido.open_output()

GLOBAL_BANK = 0
GLOBAL_PRESET = 68
KEY_OFFSET = -14
NOTE_ON_KEYMAP = {}
VELOCITY = 80

midi_port.send(mido.Message('pitchwheel', channel=0, pitch=int(+8192 * 0 / 6)))
midi_port.send(mido.Message('pitchwheel', channel=1, pitch=int(-8192 * 1 / 6)))
midi_port.send(mido.Message('pitchwheel', channel=2, pitch=int(-8192 * 2 / 6)))
midi_port.send(mido.Message('pitchwheel', channel=3, pitch=int(+8192 * 1 / 6)))


KeyboardKeyLayout = collections.namedtuple('KeyboardKeyLayout', [
    'scan_code', 'key_row',
])

KeyboardKeyMapping = collections.namedtuple('KeyboardKeyMapping', [
    'scan_code', 'midi_channel', 'relative_midi_key',
])

NoteOn = collections.namedtuple('NoteOn', [
    'midi_channel', 'key',
])


KEYBOARD_LAYOUT = [
    KeyboardKeyLayout(scan_code=24, key_row=1),  # Q
    KeyboardKeyLayout(scan_code=27, key_row=1),  # R
    KeyboardKeyLayout(scan_code=31, key_row=1),  # I
    KeyboardKeyLayout(scan_code=34, key_row=1),  # ]

    KeyboardKeyLayout(scan_code=66, key_row=2),  # Caps Lock
    KeyboardKeyLayout(scan_code=38, key_row=2),  # A
    KeyboardKeyLayout(scan_code=39, key_row=2),  # S
    KeyboardKeyLayout(scan_code=40, key_row=2),  # D
    KeyboardKeyLayout(scan_code=41, key_row=2),  # F
    KeyboardKeyLayout(scan_code=42, key_row=2),  # G
    KeyboardKeyLayout(scan_code=43, key_row=2),  # H
    KeyboardKeyLayout(scan_code=44, key_row=2),  # J
    KeyboardKeyLayout(scan_code=45, key_row=2),  # K
    KeyboardKeyLayout(scan_code=46, key_row=2),  # L
    KeyboardKeyLayout(scan_code=47, key_row=2),  # ; / :
    KeyboardKeyLayout(scan_code=48, key_row=2),  # ' / "
]

KEYBOARD_DIATONIKI = [
    KeyboardKeyMapping(scan_code=24, midi_channel=0, relative_midi_key=59),  # Q
    KeyboardKeyMapping(scan_code=27, midi_channel=0, relative_midi_key=64),  # R
    KeyboardKeyMapping(scan_code=31, midi_channel=0, relative_midi_key=71),  # I
    KeyboardKeyMapping(scan_code=34, midi_channel=0, relative_midi_key=76),  # ]

    KeyboardKeyMapping(scan_code=66, midi_channel=0, relative_midi_key=57),  # Caps Lock
    KeyboardKeyMapping(scan_code=38, midi_channel=1, relative_midi_key=59),  # A
    KeyboardKeyMapping(scan_code=39, midi_channel=0, relative_midi_key=60),  # S
    KeyboardKeyMapping(scan_code=40, midi_channel=0, relative_midi_key=62),  # D
    KeyboardKeyMapping(scan_code=41, midi_channel=1, relative_midi_key=64),  # F
    KeyboardKeyMapping(scan_code=42, midi_channel=0, relative_midi_key=65),  # G
    KeyboardKeyMapping(scan_code=43, midi_channel=0, relative_midi_key=67),  # H
    KeyboardKeyMapping(scan_code=44, midi_channel=0, relative_midi_key=69),  # J
    KeyboardKeyMapping(scan_code=45, midi_channel=1, relative_midi_key=71),  # K
    KeyboardKeyMapping(scan_code=46, midi_channel=0, relative_midi_key=72),  # L
    KeyboardKeyMapping(scan_code=47, midi_channel=0, relative_midi_key=74),  # ; / :
    KeyboardKeyMapping(scan_code=48, midi_channel=1, relative_midi_key=76),  # ' / "
]

KEYBOARD_B = [
    KeyboardKeyMapping(scan_code=66, midi_channel=2, relative_midi_key=57),  # Caps Lock
    KeyboardKeyMapping(scan_code=38, midi_channel=1, relative_midi_key=59),  # A
    KeyboardKeyMapping(scan_code=39, midi_channel=0, relative_midi_key=60),  # S
    KeyboardKeyMapping(scan_code=40, midi_channel=2, relative_midi_key=62),  # D
    KeyboardKeyMapping(scan_code=41, midi_channel=1, relative_midi_key=64),  # F
    KeyboardKeyMapping(scan_code=42, midi_channel=0, relative_midi_key=65),  # G
    KeyboardKeyMapping(scan_code=43, midi_channel=0, relative_midi_key=67),  # H
    KeyboardKeyMapping(scan_code=44, midi_channel=2, relative_midi_key=69),  # J
    KeyboardKeyMapping(scan_code=45, midi_channel=1, relative_midi_key=71),  # K
    KeyboardKeyMapping(scan_code=46, midi_channel=0, relative_midi_key=72),  # L
    KeyboardKeyMapping(scan_code=47, midi_channel=2, relative_midi_key=74),  # ; / :
    KeyboardKeyMapping(scan_code=48, midi_channel=1, relative_midi_key=76),  # ' / "
]

KEYBOARD_PLAGIOS_B = [
    KeyboardKeyMapping(scan_code=66, midi_channel=0, relative_midi_key=56),  # Caps Lock
    KeyboardKeyMapping(scan_code=38, midi_channel=0, relative_midi_key=58),  # A  XXX
    KeyboardKeyMapping(scan_code=39, midi_channel=0, relative_midi_key=60),  # S
    KeyboardKeyMapping(scan_code=40, midi_channel=0, relative_midi_key=61),  # D
    KeyboardKeyMapping(scan_code=41, midi_channel=3, relative_midi_key=64),  # F
    KeyboardKeyMapping(scan_code=42, midi_channel=0, relative_midi_key=65),  # G
    KeyboardKeyMapping(scan_code=43, midi_channel=0, relative_midi_key=67),  # H
    KeyboardKeyMapping(scan_code=44, midi_channel=0, relative_midi_key=68),  # J
    KeyboardKeyMapping(scan_code=45, midi_channel=3, relative_midi_key=71),  # K
    KeyboardKeyMapping(scan_code=46, midi_channel=0, relative_midi_key=72),  # L
    KeyboardKeyMapping(scan_code=47, midi_channel=0, relative_midi_key=73),  # ; / :
    KeyboardKeyMapping(scan_code=48, midi_channel=3, relative_midi_key=76),  # ' / "
]

KEYBOARD_MAPPING = KEYBOARD_DIATONIKI


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

        for keyboard_key in KEYBOARD_LAYOUT:
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

        # Label to display keyboard mapping
        self.label4 = Gtk.Label()
        self.label4.set_justify(Gtk.Justification.CENTER)
        self.label4.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.95, 0.95, 0.98, 1))
        self.label4.set_padding(20, 20)
        self.vbox.pack_start(self.label4, False, False, 0)

        # Connect keyboard events
        self.connect("key-press-event", self.OnKeyPress)
        self.connect("key-release-event", self.OnKeyRelease)
        self.connect("destroy", Gtk.main_quit)

        # Make window grab focus when clicked
        self.set_focus_on_click(True)
        self.connect("button-press-event", lambda w, e: self.grab_focus())

        self.Reprogram(preset_diff=0)
        self.Transpose(diff=0)
        self.ChangeMapping(mapping='Διατονική')

    def OnKeyPress(self, widget, event):
        global NOTE_ON_KEYMAP

        scancode = event.get_scancode()
        keyname = Gdk.keyval_name(event.keyval)
        keyval_with_modifier = Gtk.accelerator_get_label(event.keyval, event.state & Gtk.accelerator_get_default_mod_mask())

        #print(scancode, keyname, keyval_with_modifier)

        for keyboard_key in KEYBOARD_MAPPING:
            if keyboard_key.scan_code == scancode:
                this_keyboard_key = keyboard_key
                break
        else:
            this_keyboard_key = None

        if this_keyboard_key is not None and scancode not in NOTE_ON_KEYMAP:
            chan = this_keyboard_key.midi_channel
            key = KEY_OFFSET + this_keyboard_key.relative_midi_key
            NOTE_ON_KEYMAP[scancode] = NoteOn(midi_channel=chan, key=key)
            midi_port.send(mido.Message('note_on', channel=chan, note=key, velocity=VELOCITY))

        if keyname == 'minus':
            self.Reprogram(preset_diff=-1)
        if keyname == 'equal':
            self.Reprogram(preset_diff=1)

        if keyname == 'Page_Up':
            self.Transpose(diff=1)
        if keyname == 'Page_Down':
            self.Transpose(diff=-1)

        if keyval_with_modifier == 'F1':
            self.ChangeMapping(mapping='Διατονική')
        elif keyval_with_modifier == 'F2':
            self.ChangeMapping(mapping='Ήχος Β')
        elif keyval_with_modifier == 'F3':
            self.ChangeMapping(mapping='Ήχος Πλάγιος Β')

        if scancode in self.key_labels:
            self.key_labels[scancode].override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.45, 0.45, 0.48, 1))

        return False  # Allow further processing (e.g. typing in entry)

    def OnKeyRelease(self, widget, event):
        global NOTE_ON_KEYMAP

        scancode = event.get_scancode()

        if scancode in NOTE_ON_KEYMAP:
            midi_channel, key = NOTE_ON_KEYMAP[scancode]
            del NOTE_ON_KEYMAP[scancode]
            midi_port.send(mido.Message('note_off', channel=midi_channel, note=key, velocity=VELOCITY))

        if scancode in self.key_labels:
            self.key_labels[scancode].override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.95, 0.95, 0.98, 1))

        return False

    def Reprogram(self, preset_diff):
        global GLOBAL_PRESET
        new_preset = GLOBAL_PRESET + preset_diff
        name = synth.sfpreset_name(sfid=sfid, bank=GLOBAL_BANK, preset=new_preset)
        if name is not None:
            GLOBAL_PRESET = new_preset
            self.label2.set_markup(f'{name} (bank={GLOBAL_BANK}, preset={GLOBAL_PRESET})')
            midi_port.send(mido.Message('control_change', channel=0, control=0, value=GLOBAL_BANK))
            midi_port.send(mido.Message('control_change', channel=0, control=32, value=GLOBAL_BANK))
            midi_port.send(mido.Message('program_change', channel=0, program=GLOBAL_PRESET))
            midi_port.send(mido.Message('control_change', channel=1, control=0, value=GLOBAL_BANK))
            midi_port.send(mido.Message('control_change', channel=1, control=32, value=GLOBAL_BANK))
            midi_port.send(mido.Message('program_change', channel=1, program=GLOBAL_PRESET))
            midi_port.send(mido.Message('control_change', channel=2, control=0, value=GLOBAL_BANK))
            midi_port.send(mido.Message('control_change', channel=2, control=32, value=GLOBAL_BANK))
            midi_port.send(mido.Message('program_change', channel=2, program=GLOBAL_PRESET))
            midi_port.send(mido.Message('control_change', channel=3, control=0, value=GLOBAL_BANK))
            midi_port.send(mido.Message('control_change', channel=3, control=32, value=GLOBAL_BANK))
            midi_port.send(mido.Message('program_change', channel=3, program=GLOBAL_PRESET))
        else:
            print('Not valid program (bank=', GLOBAL_BANK, ', preset=', new_preset, ')')

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

    def ChangeMapping(self, mapping):
        global KEYBOARD_MAPPING

        if mapping == 'Διατονική':
            KEYBOARD_MAPPING = KEYBOARD_DIATONIKI
        elif mapping == 'Ήχος Β':
            KEYBOARD_MAPPING = KEYBOARD_B
        elif mapping == 'Ήχος Πλάγιος Β':
            KEYBOARD_MAPPING = KEYBOARD_PLAGIOS_B
        else:
            return

        self.label4.set_markup(f'Keyboard mapping: {mapping}')


# Run the app
app = Tonality()
app.show_all()
app.grab_focus()  # Start with focus
Gtk.main()
