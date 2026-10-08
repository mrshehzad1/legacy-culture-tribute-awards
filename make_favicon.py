"""One-off: downscale logo.png (646x386 RGBA) to favicon.png (64x64).

Areas where the emblem art is transparent get the brand gold fill so the
favicon stays visible on dark and light browser chrome alike.
"""
import zlib, struct, math, sys

SRC, DST = "logo.png", "favicon.png"
TARGET = 64
BG = (198, 162, 100, 255)          # --gold #C6A264

# ---------- read & decode ----------
with open(SRC, "rb") as fh:
    data = fh.read()
pos, idat = 8, b""
while pos < len(data):
    ln = struct.unpack(">I", data[pos:pos+4])[0]
    typ = data[pos+4:pos+8]
    chunk = data[pos+8:pos+8+ln]
    if typ == b"IHDR":
        w, h, bd, ct = struct.unpack(">IIBB", chunk[:10])
    elif typ == b"IDAT":
        idat += chunk
    pos += 12 + ln
raw = zlib.decompress(idat)
bpp, stride = 4, w * 4
rows, prev, p = [], bytearray(stride), 0
for y in range(h):
    ft = raw[p]; p += 1
    line = bytearray(raw[p:p+stride]); p += stride
    for x in range(stride):
        a = line[x-bpp] if x >= bpp else 0
        b = prev[x]
        c = prev[x-bpp] if x >= bpp else 0
        if ft == 1:
            line[x] = (line[x] + a) & 255
        elif ft == 2:
            line[x] = (line[x] + b) & 255
        elif ft == 3:
            line[x] = (line[x] + (a + b) // 2) & 255
        elif ft == 4:
            pa, pb, pc = abs(b-c), abs(a-c), abs(a+b-2*c)
            pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
            line[x] = (line[x] + pr) & 255
    rows.append(bytes(line))
    prev = line

def px(x, y):
    off = x * 4                                # rows[y] is already row y
    return rows[y][off], rows[y][off+1], rows[y][off+2], rows[y][off+3]

# ---------- box-downsample to 64x64 (bg under transparent, alpha preserved) -------
out = bytearray()
for oy in range(TARGET):
    for ox in range(TARGET):
        x0 = int(ox * w / TARGET); x1 = max(x0 + 1, int((ox + 1) * w / TARGET))
        y0 = int(oy * h / TARGET); y1 = max(y0 + 1, int((oy + 1) * h / TARGET))
        r = g = b = a = 0; n = 0
        for y in range(y0, y1):
            for x in range(x0, x1):
                pr, pg, pb, pa = px(x, y)
                r += pr; g += pg; b += pb; a += pa; n += 1
        r, g, b, a = r // n, g // n, b // n, a // n
        # blend art over gold where the source is translucent/transparent
        alpha = a / 255.0
        orr = int(r * alpha + BG[0] * (1 - alpha))
        ogg = int(g * alpha + BG[1] * (1 - alpha))
        obb = int(b * alpha + BG[2] * (1 - alpha))
        out += bytes((orr, ogg, obb, 255))

# ---------- write PNG ----------
def chunk(tag, payload):
    c = zlib.crc32(tag + payload) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + tag + payload + struct.pack(">I", c)

raw_out = b""
for y in range(TARGET):
    raw_out += b"\x00" + bytes(out[y * TARGET * 4:(y + 1) * TARGET * 4])
png = (b"\x89PNG\r\n\x1a\n"
       + chunk(b"IHDR", struct.pack(">IIBBBBB", TARGET, TARGET, 8, 6, 0, 0, 0))
       + chunk(b"IDAT", zlib.compress(raw_out, 9))
       + chunk(b"IEND", b""))
with open(DST, "wb") as fh:
    fh.write(png)
print("wrote", DST, len(png), "bytes")
