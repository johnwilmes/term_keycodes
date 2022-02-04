# term_keycodes
Script to produce configuration files for terminal emulators and applications in order to handle
remapping modified keypresses (control, alt, super, etc.) to unicode code points.

(We use arbitrary unicode code-points instead the "fixterms" quasi-standard, which has a number of
issues. At some point maybe more applications will use kitty's standard for encoding these keys and
we won't need to deal with this at all.)

## Supported Applications

- kitty - produces a configuration file performing the remapping
- nvim - produces a lua script that defines a function performing the remapping in the reverse direction

