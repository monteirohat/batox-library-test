"""Generates a test library of fake ROMs (a few bytes each, not real games),
with covers and two gamelist.xml files, to test BatoX's Library screen.
    python3 generate.py OUT_DIR"""
import os
import struct
import sys
import zlib

out = sys.argv[1]

# system -> (extension, cover color)
SYSTEMS = {
    "snes": (".sfc", (124, 77, 255)),
    "nes": (".nes", (229, 57, 53)),
    "gba": (".gba", (63, 81, 181)),
    "gb": (".gb", (139, 172, 15)),
    "gbc": (".gbc", (0, 150, 136)),
    "megadrive": (".md", (33, 33, 33)),
    "mastersystem": (".sms", (0, 120, 215)),
    "gamegear": (".gg", (255, 160, 0)),
    "n64": (".z64", (0, 145, 70)),
    "atari2600": (".a26", (121, 85, 72)),
    "pcengine": (".pce", (240, 98, 146)),
}
GENRES = ["Platform", "Puzzle", "Racing"]


def png(path, color, w=240, h=320):
    """A vertical gradient from color to black, in pure Python."""
    rows = bytearray()
    for y in range(h):
        k = 1 - 0.75 * y / h
        rows.append(0)
        rows.extend(bytes(int(c * k) for c in color) * w)

    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) \
        + chunk(b"IDAT", zlib.compress(bytes(rows), 9)) + chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(data)


for system, (ext, color) in SYSTEMS.items():
    d = os.path.join(out, system)
    os.makedirs(os.path.join(d, "images"), exist_ok=True)
    entries = []
    for i in (1, 2, 3):
        stem = f"BatoX Test Game {i} ({system})"
        content = f"BATOX FAKE ROM - not a game - {system} {i}\n".encode()
        with open(os.path.join(d, stem + ext), "wb") as f:
            f.write(content + bytes((i * 4096) - len(content)))
        if system == "nes" and i == 3:
            continue                                   # a game without a cover
        if system == "gb" and i == 2:
            png(os.path.join(d, "images", f"{stem}-thumb.jpg"), color)  # PNG bytes, the -thumb fallback
        else:
            png(os.path.join(d, "images", f"{stem}-image.png"), color)
        entries.append((stem, ext, i))
    if system in ("snes", "gba"):
        with open(os.path.join(d, "gamelist.xml"), "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0"?>\n<gameList>\n')
            for stem, e, i in entries:
                f.write(f"\t<game>\n\t\t<path>./{stem}{e}</path>\n\t\t<name>Test Adventure {i}</name>\n"
                        f"\t\t<desc>A fake {system} game to test BatoX's Library screen.</desc>\n"
                        f"\t\t<developer>BatoX</developer>\n\t\t<genre>{GENRES[i - 1]}</genre>\n"
                        f"\t\t<players>1-2</players>\n\t\t<releasedate>199{i}0101T000000</releasedate>\n\t</game>\n")
            f.write("</gameList>\n")

print("ok")
