#!/usr/bin/env python3

import sys
import argparse
from dataclasses import dataclass, asdict

DESCRIPTION="""\
Produces configuration files for terminal emulators and applications in order to handle remapping
modified keypresses (control, alt, super, etc.) to unicode code points.

    kitty - produces a configuration file performing the remapping

    nvim - produces a configuration file performing the remapping in the reverse direction

The configuration file for the specified application is printed to STDOUT.

(We use arbitrary unicode code-points instead the "fixterms" quasi-standard, which has a number of
issues. At some point maybe more applications will use kitty's standard for encoding these keys and
we won't need to deal with this at all.)
"""

UNICODE_CODEPOINT = 0xe500

TEMPLATE_INSERTION_MARKER = "### REMAP TERMCODES ###\n"

ANSI_UNSHIFTED = r"abcdefghijklmnopqrstuvwxyz`1234567890-=[]\;',./"
ANSI_SHIFTED   = r'ABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+{}|:"<>?'
ANSI_SHIFT_MAP = dict(zip(ANSI_UNSHIFTED, ANSI_SHIFTED))

NONTEXT_KEYS = "tab,backspace,delete,escape,enter,space,left,right,up,down,home,end,page_up,page_down,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19,f20,f21,f22,f23,f24".split(",")

BASE_KEYS = "f13,f14,f15,f16,f17,f18,f19,f20,f21,f22,f23,f24".split(",") # These aren't recognized by Nvim, even without modifiers
SHIFT_KEYS = BASE_KEYS+("backspace,enter,space".split(",")) # Keys whose shifted versions are ambiguous
CTRL_KEYS = NONTEXT_KEYS+list("hijms`12345[7890;',.") # Unshifted keys whose ctrl versions are ambiguous

@dataclass
class Modifier:
    shift: bool = False
    alt: bool = False
    ctrl: bool = False
    super: bool = False

    def get_names(self):
        ordered = ('super', 'ctrl', 'alt', 'shift')
        return [x for x in ordered if self.__dict__[x]]

    def to_lua(self):
        modifier_abbr = {'super': 'D', 'ctrl': 'C', 'alt': 'A', 'shift': 'S'}
        table_entries = [f"{modifier_abbr[x]}=true" for x in self.get_names()]
        return "{" + ", ".join(table_entries) + "}"

def unicode_to_lua(unicode):
    """Produces an escaped decimal encoding of a unicode string."""
    decimal = [''] + [str(int(x)) for x in unicode.encode()]
    return '\\'.join(decimal)

def nvim_remap(key, modifier, unicode):
    r""" Return command to associate modified key press with unicode code in a lua table"""
    modifier = Modifier(**asdict(modifier)) # copy it
    if modifier.shift and (key in ANSI_SHIFT_MAP):
        key = ANSI_SHIFT_MAP[key]
        modifier.shift = False

    nvim_key_names = {"page_up": "PageUp", "page_down": "PageDown", "backspace": "BS",
            "delete": "Del", "escape": "Esc"}

    if len(key) > 1:
        key = nvim_key_names.get(key, key.capitalize())
        key = f"<{key}>"

    key = f" [==[{key}]==] "

    #if key==']':
    #    key = f"'{key}'"
    #else:
    #    key = f" [[{key}]] "

    return f"mod_map[{key}][get_modifier_bits({modifier.to_lua()})] = {unicode}"

def kitty_remap(key, modifier, unicode):
    r""" Return the kitty command that transforms a modified keypress into a unicode character

        - key: the base key that is pressed, as a string. E.g., 'a' or 'backspace'
        - modifier: a `Modifier` instance giving any modifiers pressed
        - unicode: the desired Unicode code point as an integer

        E.g. kitty_remap('a', Modifier(ctrl=true), 0xe000) returns

        "map ctrl+a send_text all \ue000"
    """
    # {:04x} means width 4, padded with zeros as needed, in lower-case hex

    keypress = '+'.join(modifier.get_names() + [key])
    return f"map {keypress} send_text all \\u{unicode:04x}"

def _remap_all(mapper):
    mappings = []

    # Base
    mappings.append((BASE_KEYS, Modifier()))

    # Shift
    mappings.append((SHIFT_KEYS, Modifier(shift=True)))

    # Control
    mappings.append((CTRL_KEYS, Modifier(ctrl=True)))

    # Control+Shift
    mappings.append((ANSI_UNSHIFTED, Modifier(ctrl=True, shift=True)))
    mappings.append((NONTEXT_KEYS, Modifier(ctrl=True, shift=True)))
    
    # Alt
    mappings.append((NONTEXT_KEYS, Modifier(alt=True)))

    # Alt+Shift
    mappings.append((NONTEXT_KEYS, Modifier(alt=True, shift=True)))

    # Super
    mappings.append((ANSI_UNSHIFTED, Modifier(super=True)))
    mappings.append((NONTEXT_KEYS, Modifier(super=True)))

    # Super+Shift
    mappings.append((ANSI_UNSHIFTED, Modifier(super=True, shift=True)))
    mappings.append((NONTEXT_KEYS, Modifier(super=True, shift=True)))

    unicode = UNICODE_CODEPOINT
    for keys, modifier in mappings:
        for key in keys:
            yield mapper(key, modifier, unicode)
            unicode += 1

def _main():
    parser = argparse.ArgumentParser(description=DESCRIPTION,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('application', choices=['kitty', 'nvim'])
    args = parser.parse_args()

    applications = {'kitty': kitty_remap,
                    'nvim': nvim_remap}
    mapper = applications[args.application]

    with open(f"{sys.path[0]}/templates/{args.application}", "r") as template:
        for line in template:
            if line == TEMPLATE_INSERTION_MARKER:
                for mapping in _remap_all(mapper):
                    print(mapping)
            else:
                print(line, end='')

if __name__ == "__main__":
    _main()
