# BatoX library test

Fake ROMs (a few kilobytes of text and zeros each, not real games) and generated covers, to test
the Library screen of [BatoX](https://github.com/monteirohat/batox): 11 systems, 3 games each.

What it covers:

- covers named `<ROM name>-image.png`, plus one `-thumb.jpg` (`gb`, game 2) and one game without a
  cover (`nes`, game 3);
- `gamelist.xml` details for `snes` and `gba` (their games are called "Test Adventure");
- a system the console may not have (`pcengine`, `atari2600`...), listed but not downloadable.

## Use it

In BatoX, open **Library** and set the address to:

```
https://raw.githubusercontent.com/<user>/<repo>/main/library.json
```

## Change it

```bash
python3 generate.py .                                    # writes the ROMs, covers and gamelists again
python3 ../BatoX/scripts/make-library.py . --name "BatoX test library"   # writes library.json
```

`library.json` holds each file's size and SHA-256, so run `make-library.py` after any change, or
BatoX refuses the downloads.
