#!/usr/bin/env python

import struct


encrypted_text = "YMINNNUDZEHFQRITARBZRNVOLJGNVKOLSLREMOSEDFTTPQMMFLOZXMRUNPFFZFZVYAVGLGCEICKOAYGKUKAXWBBMTEMFSJLAUDDDWYCOSKVRILACTPDWYXHOYTCJFCFEPOOYHHPVYIKZMILDEYTEDIHDAPHJVIXNKHKZHYOQRBSPVYXETIXKSOVAYQZTNLEVEAAPZPGIWXGTAZMRVGZHGANOFEPOOYINDOSCRUDYJEJAENQNLNJJOHZSAREFCUAPZTCBFHZBMSGQJQJAKCKYEDFAYQRVBJWTZJXHUUKMOYPWVZGKQAFFAPXBLDFLGUJQFABGXFWQWSVWRDWYLQQZSZMLETTQYOQRBSPVYXETIXKVGLJKMKMIAAAEHFQRIORUVHHXQNMTKMJDFKNUEWPSCCIEHILSSOLQQNAZSSOLQQQJDXNLADACPPRVYXVCUYKFLOPFCHFPGWHGWEUKSSUSBRBBCACFICOOKZEVMSTTPXMZCVHNMSLCUAAUQROCTEJMXXAOHLQTTPZAXTRDNKLPYDZHCFXYVZGZFXBBEYOQRBSPVYXETIXKVGLJKMAZMOSCDWYCOOKRANDMIWUNIFQZVWFSMSGYHCRIHAVMPPQZHGXZRRMACTERBQFVDUGUHUOKBQSINYOQRBSPVYXETIXKVGLJKMYVMXMSFREZYBVZGCIEHILSUSGORBMWDTOXZBFBIOSCZSZABMBDCKHXDVZJFCOSCFEPOOYHUPBPXNNKSDABDQNMBBPXNNKSDABDQNMBBPXNNKSDABDQNMBBPXNNKSDABDQCCLPVYXETIXKVGLJKMKMIOETYOQRBSPVYXETIXKVGLJKMAZMOSCDWYCOOKRANDMIWUNIFQZVWFSMSGYHCRIHAVMPPQZHGXZRRMACTERBQFVDUGUHUOKBQSINYOQRBSPVYXETIXKVGLJKMYVMXMSFREZYBVZGCIEHILSUSGORBMWDTOXZBFBIOSCZSZABMBDCKHXDVZJFCOSCFEPOOYHUPBPXNNKSDABDQNMBBPXNNKSDABDQZQHJAIFEPOOYYST"

with open('key.png', 'r') as f:
    keypng = f.read()


def to_hex(s):
    return" ".join("{:02x}".format(ord(c)) for c in s)

print("Total file size:" + str(len(keypng)))

# file signature is the first 8 bytes, ignore them
key = keypng
curr_idx = 0
header = key[curr_idx:curr_idx + 8]
print("First we have header: (0-8b)" + str(header))
curr_idx += 8

START_IHDR = "IHDR"
END_CHUNK = "IEND"
IDAT_PIECE = "IDAT"
bKGD_PIECE = "bKGD"


# Process IHDR first
# print(key[curr_idx:])
# print(curr_idx)
IHDR_idx = key[curr_idx:].find(START_IHDR)
print("IHDR_idx: " + str(IHDR_idx))
useless_b = key[curr_idx:curr_idx + IHDR_idx]
print("We got {} useless bytes: {} ({}-{})".format(len(useless_b),
                                                   to_hex(useless_b), curr_idx, curr_idx + IHDR_idx))

print("useless_b as int:" + str(struct.unpack("!I", useless_b)))


start_IHDR_chunk = curr_idx + IHDR_idx
curr_idx += IHDR_idx + 4
width = key[curr_idx:curr_idx + 4]
curr_idx += 4
height = key[curr_idx:curr_idx + 4]
curr_idx += 4
bitdepth = key[curr_idx:curr_idx + 1]
curr_idx += 1
colortype = key[curr_idx:curr_idx + 1]
curr_idx += 1
compressionmethod = key[curr_idx:curr_idx + 1]
curr_idx += 1
filtermethod = key[curr_idx:curr_idx + 1]
curr_idx += 1
interlacemethod = key[curr_idx:curr_idx + 1]
curr_idx += 1
end_IHDR_chunk = curr_idx
print("IHDR chunk ({}-{}):".format(start_IHDR_chunk, end_IHDR_chunk))
titles = ["width ", "height ", "bitdepth ", "colortype ",
          "compressionmethod ", "filtermethod ", "interlacemethod"]
for idx, i in enumerate([width, height, bitdepth, colortype, compressionmethod, filtermethod, interlacemethod]):
    if idx == 0 or idx == 1:
        num = struct.unpack(">I", i)[0]
    else:
        num = struct.unpack(">B", i)[0]
    print("   " + titles[idx] + ": " + str(num))

chunks = []
finished = False

print("curr_idx is: " + str(curr_idx))

print("key partially looks like: " + str(key[curr_idx:curr_idx + 40]))

print("\n\n\n\n\n\n\n")
curr_idx = 8

IDAT_chunk_data = None
# Then go for the chunks
while not finished:
    if curr_idx >= len(key):
        break
    # chunk looks like
    # length (4byte), chunk type (4 byte), chunk data, crc (4byte)
    len_b = key[curr_idx:curr_idx + 4]
    curr_idx += 4
    print("Chunk length str: " + str(len_b))
    chunk_len = struct.unpack(">I", len_b)[0]
    print("Chunk length: " + str(chunk_len))
    chunk_type_b = key[curr_idx: curr_idx + 4]
    curr_idx += 4
    print("Chunk type: " + str(chunk_type_b))
    chunk_data_b = key[curr_idx:curr_idx + chunk_len]
    curr_idx += chunk_len
    print("Chunk data: " + str(chunk_data_b))
    chunk_crc_b = key[curr_idx:curr_idx + 4]
    curr_idx += 4
    # print("Chunk crc: " + str(chunk_crc_b))
    print("CRC as hex: " + str(to_hex(chunk_crc_b)))

    # Check CRC32
    import binascii
    calc_crc = binascii.crc32(chunk_type_b + chunk_data_b)
    crc_chunk = struct.unpack(">i", chunk_crc_b)[0]
    crc_chunk2 = struct.unpack("<i", chunk_crc_b)[0]
    print("crc_chunk in int: " + str(crc_chunk))
    if calc_crc != crc_chunk:
        print("Different CRC!")
        print("Calculated CRC: " + str(calc_crc))
        # print("In hex: " + str(to_hex(calc_crc)))

    if chunk_type_b == "IDAT":
        IDAT_chunk_data = chunk_data_b

    print("\n\n")


import zlib

print("First bytes of LZLIB ")
header_zlib = IDAT_chunk_data[:2]
print(to_hex(header_zlib))
print("0x78 | 0xDA - Best Compression ")

decompressed_data = zlib.decompress(IDAT_chunk_data, 0)
# import pdb; pdb.set_trace()
print("Decompressed data size: " + str(len(decompressed_data)))
print("Maybe should be 200*200*4: " + str(200 * 200 * 4))
with open('pixels.txt', 'w') as f:
    f.write(decompressed_data)

print("First 200bytes of decompressed data:")
print(to_hex(decompressed_data[:200]))

print("Second 200bytes of decompressed data:")
print(to_hex(decompressed_data[200:400]))

print("Last 200bytes of decompressed data:")
print(to_hex(decompressed_data[-200:]))


def split(str, num):
    return [str[start:start + num] for start in range(0, len(str), num)]


parts = split(decompressed_data, 4)
# r g b a
count_a = 0
for part in parts:
    r, g, b, a = part
    if a > 0:
        count_a += 1

print("alpha pixels > 0: " + str(count_a))


with open('image.ppm', 'wb') as f:
    f.write("P6\n200 200\n255\n")
    for part in parts:
        r, g, b, a = part
        f.write(r + g + b)

with open('image2.ppm', 'wb') as f:
    f.write("P6\n200 200\n255\n")
    row_idx = 0
    while row_idx < len(decompressed_data):
        row = decompressed_data[row_idx:row_idx + 200 * 4 + 1]
        print("row: (" + str(len(row)) + ")")
        print(to_hex(row))
        # ignore first byte
        row = row[1:]
        parts2 = split(row, 4)
        for part in parts2:
            r, g, b, a = part
            f.write(r + g + b)
        row_idx += 200 * 4 + 1

with open('image2_white.ppm', 'wb') as f:
    f.write("P6\n200 200\n255\n")
    row_idx = 0
    while row_idx < len(decompressed_data):
        row = decompressed_data[row_idx:row_idx + 200 * 4 + 1]
        print("row: (" + str(len(row)) + ")")
        print(to_hex(row))
        # ignore first byte
        row = row[1:]
        parts2 = split(row, 4)
        for part in parts2:
            r, g, b, a = part
            if ord(r) > 0 or ord(g) > 0 or ord(b) > 0 or ord(a) > 0:
                f.write(struct.pack(">BBB", 255, 255, 255))
            else:
                f.write(struct.pack(">BBB", 0, 0, 0))
        row_idx += 200 * 4 + 1

with open('image3.ppm', 'wb') as f:
    f.write("P6\n200 200\n255\n")
    for idx, part in enumerate(parts):
        r, g, b, a = part
        if ord(a) > 0:
            f.write(r + g + b)
        else:
            f.write(struct.pack(">BBB", 0, 0, 0))


with open('allpixels_white.ppm', 'wb') as f:
    f.write("P6\n200 200\n255\n")
    for idx, part in enumerate(parts):
        r, g, b, a = part
        if ord(a) > 0:
            f.write(struct.pack(">BBB", 255, 255, 255))
        else:
            f.write(struct.pack(">BBB", 0, 0, 0))

with open('allpixels_white_ignorebytes.ppm', 'wb') as f:
    f.write("P6\n200 200\n255\n")
    for idx, part in enumerate(parts):
        if idx > 200 * 200:
            break
        r, g, b, a = part
        if ord(a) > 0:
            f.write(struct.pack(">BBB", 255, 255, 255))
        else:
            f.write(struct.pack(">BBB", 0, 0, 0))



with open('image4.ppm', 'wb') as f:
    f.write("P6\n200 200\n255\n")
    for idx, part in enumerate(parts):
        r, g, b, a = part
        if ord(a) > 0:
            # print(ord(a))
            f.write(struct.pack(">BBB", 255, 255, 255))
        else:
            f.write(struct.pack(">BBB", 0, 0, 0))


with open('red.ppm', 'wb') as f:
    f.write("P6\n200 200\n255\n")
    for idx, part in enumerate(parts):
        r, g, b, a = part
        if ord(r) > 0:
            # print(ord(r))
            f.write(struct.pack(">BBB", 255, 255, 255))
        else:
            f.write(struct.pack(">BBB", 0, 0, 0))


with open('green.ppm', 'wb') as f:
    f.write("P6\n200 200\n255\n")
    for idx, part in enumerate(parts):
        r, g, b, a = part
        if ord(g) > 0:
            # print(ord(g))
            f.write(struct.pack(">BBB", 255, 255, 255))
        else:
            f.write(struct.pack(">BBB", 0, 0, 0))

with open('blue.ppm', 'wb') as f:
    f.write("P6\n200 200\n255\n")
    for idx, part in enumerate(parts):
        r, g, b, a = part
        if ord(b) > 0:
            # print(ord(b))
            f.write(struct.pack(">BBB", 255, 255, 255))
        else:
            f.write(struct.pack(">BBB", 0, 0, 0))

for idx, part in enumerate(parts):
        r, g, b, a = part
        if r == g == b == a and ord(a) != 0:
            print("all rgba same value!: " + str(ord(r)))