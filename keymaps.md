Using modifier keys in terminal applications can be a nuisance thanks to the long legacy of
physical terminals. This file documents some of their idiosyncracies and the re-mappings I use to
work around them. Specifically, I remap problematic modified keys to Unicode code points from the
Unicode Private Use Area U+E000 to U+F8FF.

TODO: this is out of date, update

# CTRL mappings

## Traditional terminal CTRL mappings

Traditionally, a terminal maps <ctrl>+<key> in strange and inconvenient ways. A complete table is
available at https://sw.kovidgoyal.net/kitty/keyboard-protocol/#ctrl-mapping

Very vaguely, the <ctrl> key sets the two highest bits of the 7-bit ASCII code corresponding to the
key, and sets them to zero. Many keys correspond to two ASCII codes (e.g. a and A), in which case
you take the smaller ASCII code as long as it is at least 64. Otherwise, maybe you take the larger
ASCII code, except that the association of keys to pairs of ASCII codes is based on very old
keyboard layouts? The mappings for non-letter keys (e.g. numbers and symbols) are a mess.

In any case, the result is that in a terminal, the combination <ctrl>+<key> often yields something
that is indistinguishable from some other keypresses.

Here is a list of all the non-alphabetic keys on my keyboard, along with a symbolic representation
of what they emit in my terminal when modified with <CTRL>.

    ` -> `
    1 -> 1
    2 -> ^@
    3 -> ^[
    4 -> ^\
    5 -> ^]
    6 -> ^^
    7 -> ^_
    8 -> <delete>
    9 -> 9
    0 -> 0
    - -> -
    = -> =
    [ -> ^[ (i.e., <esc>)
    ] -> ^]
    \ -> ^\
    ; -> ;
    ' -> '
    , -> ,
    . -> .
    / -> ^_
    <space> -> ^@
    <backspace> -> <backspace>
    <enter> -> <enter>
    <tab> -> doesn't emit (but maybe does on other terminals)
    <esc> -> <esc>

In addition, some of the alphabetic keys emit control codes that are indistinguishable from other
keys on the keyboard:

    ^H -> <backspace>
    ^I -> <tab>
    ^J -> <enter> (technically \n)
    ^M -> <enter> (technically \r)

Note that on some terminals, ^S will stop all input and ^Q will restart it.

## CTRL remappings for a better terminal experience

We remap the following keys when modified by control:

    hijms`12345[7890;',.<tab><backspace><enter>

This includes everything that produces ambiguous or unreliable results. Note that we do NOT remap
<ctrl>+6, which does produce an unambiguous result.  We do however remap <ctrl>+[ which is usually
a useful way of producing <esc>. This is because we instead remap <caps> (and in fact <ctrl>) to
produce <esc> when tapped (and not used as a modifier) via `xcape`.

We continue to use <ctrl>+<space> for <ctrl>+2 (i.e. `^@`) and we continue to use <ctrl>+/ for
<ctrl>+7 (i.e. `^_`).

I remap (currently using kitty) the sequence of keys given above, when modified by <ctrl>, to
instead produce the 23 Unicode code points U+E000 through U+E016.

# Other modifier keys

The <alt> modifier key is also annoying in terminals. Traditionally it has emitted <esc> followed
by the modified key. Other modifier keys like <super> (i.e. Windows or Mac Command key) also cannot
reliably be used by terminal applications (e.g., they might not emit anything at all).

I find that <shift> works fine on its own (and is generally handled reliably in terminals), but I
find it awkward to use in combination with other modifer keys. So I reserve combined modifier
sequences involving <shift> (e.g. <ctrl>+<shift>+m) for the desktop environment or terminal
emulator itself, rather than trying to use them in terminal applications.

However, I remap <alt>, <super>, <ctrl>+<alt>, and <ctrl>+<super> to be more useful.  Since <alt>
and <super> are usually small keys that are close together on keyboards, and appear in inconsistent
orders (e.g., usually the Windows key is to the left of Alt, but the Mac Command key is to the
right of Alt), I do not use them as separate modifiers: instead, I ensure that they always map to
the same thing. Separately, <ctrl>+<alt> and <ctrl>+<super> do the same thing.

I order the keys as follows:

    abcdefghijklmnopqrstuvwxyz`1234567890-=[]\;',./<tab><backspace><enter><space>

These are mapped under <alt> or <super> to the 51 Unicode code points U+E100 through U+E133, and
they are mapped under <ctrl>+<alt> or <ctrl>+<super> to U+E200 through U+E233.

