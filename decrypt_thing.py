#!/usr/bin/env python

import struct


encrypted_text = "YMINNNUDZEHFQRITARBZRNVOLJGNVKOLSLREMOSEDFTTPQMMFLOZXMRUNPFFZFZVYAVGLGCEICKOAYGKUKAXWBBMTEMFSJLAUDDDWYCOSKVRILACTPDWYXHOYTCJFCFEPOOYHHPVYIKZMILDEYTEDIHDAPHJVIXNKHKZHYOQRBSPVYXETIXKSOVAYQZTNLEVEAAPZPGIWXGTAZMRVGZHGANOFEPOOYINDOSCRUDYJEJAENQNLNJJOHZSAREFCUAPZTCBFHZBMSGQJQJAKCKYEDFAYQRVBJWTZJXHUUKMOYPWVZGKQAFFAPXBLDFLGUJQFABGXFWQWSVWRDWYLQQZSZMLETTQYOQRBSPVYXETIXKVGLJKMKMIAAAEHFQRIORUVHHXQNMTKMJDFKNUEWPSCCIEHILSSOLQQNAZSSOLQQQJDXNLADACPPRVYXVCUYKFLOPFCHFPGWHGWEUKSSUSBRBBCACFICOOKZEVMSTTPXMZCVHNMSLCUAAUQROCTEJMXXAOHLQTTPZAXTRDNKLPYDZHCFXYVZGZFXBBEYOQRBSPVYXETIXKVGLJKMAZMOSCDWYCOOKRANDMIWUNIFQZVWFSMSGYHCRIHAVMPPQZHGXZRRMACTERBQFVDUGUHUOKBQSINYOQRBSPVYXETIXKVGLJKMYVMXMSFREZYBVZGCIEHILSUSGORBMWDTOXZBFBIOSCZSZABMBDCKHXDVZJFCOSCFEPOOYHUPBPXNNKSDABDQNMBBPXNNKSDABDQNMBBPXNNKSDABDQNMBBPXNNKSDABDQCCLPVYXETIXKVGLJKMKMIOETYOQRBSPVYXETIXKVGLJKMAZMOSCDWYCOOKRANDMIWUNIFQZVWFSMSGYHCRIHAVMPPQZHGXZRRMACTERBQFVDUGUHUOKBQSINYOQRBSPVYXETIXKVGLJKMYVMXMSFREZYBVZGCIEHILSUSGORBMWDTOXZBFBIOSCZSZABMBDCKHXDVZJFCOSCFEPOOYHUPBPXNNKSDABDQNMBBPXNNKSDABDQZQHJAIFEPOOYYST"

with open('key.png', 'r') as f:
    keypng = f.read()

# decode png image to only have the data

# file signature is the first 8 bytes, ignore them
key = keypng[8:]

START_CHUNK = "IHDR"
END_CHUNK = "IEND"

chunks = []
curr_idx = 0
finished = False
while not finished:
    start_chunk_idx = key[curr_idx:].find(START_CHUNK)
    if start_chunk_idx != -1:
        print("curr_idx: " + str(curr_idx))
        print("start_chunk_idx: " + str(start_chunk_idx))
        print("Chunk starts at: " + str(curr_idx + start_chunk_idx))
        if key[curr_idx + start_chunk_idx:curr_idx + start_chunk_idx + 4] != START_CHUNK:
            print("START CHUNK IS NOT IHDR")
        # IHDR header is 13 bytes
        ini = curr_idx + start_chunk_idx + 4
        width = key[ini:ini + 4]
        height = key[ini + 4:ini + 8]
        bitdepth = key[ini + 8:ini + 9]
        colortype = key[ini + 9:ini + 10]
        compressionmethod = key[ini + 10:ini + 11]
        filtermethod = key[ini + 11:ini + 12]
        interlacemethod = key[ini + 12:ini + 13]
        print("width ,height ,bitdepth ,colortype ,compressionmethod ,filtermethod ,interlacemethod")
        titles = ["width ","height ","bitdepth ","colortype ","compressionmethod ","filtermethod ","interlacemethod"]
        for idx, i in enumerate([width ,height ,bitdepth ,colortype ,compressionmethod ,filtermethod ,interlacemethod]):
            if idx == 0 or idx == 1:
                num = struct.unpack(">I", i)[0]
            else:
                num = struct.unpack(">B", i)[0]
            print("   " + titles[idx] + ": " + str(num))
        print("Color type 6:")
        print("""Each pixel is an R,G,B triple, followed by an alpha sample.""")

        print("compression method 0 (deflate/inflate compression with a sliding window of at most 32768 bytes) ")
        print("only filter method 0 (adaptive filtering with five basic filter types) is defined")
        print("interlace: Two values are currently defined: 0 (no interlace) or 1 (Adam7 interlace).")

        end_chunk_idx = key[curr_idx + start_chunk_idx + 4 + 13:].find(END_CHUNK)
        print("end_chunk_idx: " + str(end_chunk_idx))
        print("Chunk ends at: " + str(curr_idx +
                                      start_chunk_idx + 4 + 13 + end_chunk_idx))
        print("Chunk ends at: " + str(curr_idx +
                                      start_chunk_idx + 4 + 13 + end_chunk_idx))
        chunk = key[curr_idx + start_chunk_idx +
                    4 + 13: curr_idx + start_chunk_idx + 4 + end_chunk_idx]
        print("Chunk: (len " + str(len(chunk)) + ")")
        print(chunk)
        chunks.append(chunk)
        curr_idx = curr_idx + start_chunk_idx + 4 + end_chunk_idx + 4
    else:
        finished = True

print("We got: " + str(len(chunks)) + " chunks of data")


def to_hex(s):
    return" ".join("{:02x}".format(ord(c)) for c in s)


def split(str, num):
    return [str[start:start + num] for start in range(0, len(str), num)]


for chunk in chunks:
    length = chunk[:4]
    print("chunk length: " + str(length))
    length_uint = struct.unpack(">I", length)[0]
    print("chunk length uint: " + str(length_uint))
    chunk_type_code = chunk[4:8]
    print("chunk type: " + str(chunk_type_code))
    # for b in chunk_type_code:
    #     print(ord(b))
    chunk_type_code_hex = to_hex(chunk_type_code)
    print("chunk type hex: " + str(chunk_type_code_hex))
    crc = chunk[8 + length_uint:8 + length_uint + 4]
    print("chunk crc: " + str(crc))
    print("chunk crc hex: " + str(to_hex(crc)))
    data = chunk[8:8 + length_uint]
    print("chunk data: " + str(data))
    data_hex = to_hex(data)
    print("data hex:")
    print(data_hex)
    idat_idx = data.find("IDAT")
    print("idat_idx: " + str(idat_idx))
    # actual data must be after IDAT, I guess
    actual_data = data[idat_idx + 4:]
    print("Actual data length: " + str(len(actual_data)))
    #print("Actual data:" + str(actual_data))
    # print("Actual data hex: " + str(to_hex(actual_data)))

    splitted = split(actual_data, 8)
    for s in splitted:
        print(to_hex(s))

    # from Crypto.Cipher import DES
    # obj = DES.new("actual_data", DES.MODE_ECB)
    # decripted = obj.decrypt(encrypted_text)
    # print(decripted)

# sudo pip install pypng
import png
reader = png.Reader('key.png')
import Crypto.Cipher
encryptions = ['AES',
               # 'ARC2',
               # 'ARC4',
               # 'Blowfish',
               # 'CAST',
               'DES',
               # 'DES3',
               # 'XOR',
               # 'PKCS1_v1_5',
               # 'PKCS1_OAEP'
               ]

modes = ['MODE_CBC',
         'MODE_CFB',
         'MODE_CTR',
         'MODE_ECB',
         'MODE_OFB',
         'MODE_OPENPGP',
         #'MODE_PGP' # not supported
         ]
actual_data = ""
for c in reader.chunks():
    print("chunk: " + str(c))
    print(type(c))
    if c[0] == 'IDAT':
        actual_data = c[1]
        print("LENGTH of IDAT is: " + str(len(actual_data)))
        from binascii import unhexlify, b2a_hex
        # b = unhexlify(actual_data)
        b = b2a_hex(actual_data)
        print("unhex size: " + str(len(b)))
    # if c[0] == '':

IHDR_idx = key.find("IHDR")
print(IHDR_idx)
bKGD_idx = key.find("bKGD")
print(bKGD_idx)
actual_data = key[IHDR_idx + 4 + 13:bKGD_idx]
print("HACKY")
print("actual_data: " + str(actual_data))
print("len: " + str(len(actual_data)))

actual_data = struct.pack(">BBBBBBBBB", 23, 14, 1, 4, 5, 3, 7, 12, 6)

from importlib import import_module
for encryption in encryptions:
    print("    Import crypto cipher: " + str(encryption))
    for mode in modes:
        module = import_module("Crypto.Cipher." + encryption)
        print("Trying mode: " + str(mode))
        try:
            obj = module.new(actual_data, getattr(module, mode), actual_data)
            decripted = obj.decrypt(encrypted_text)
            print("!!!!!!!!!!!!!!!!!!!")
            print(decripted)
            print("!!!!!!!!!!!!!!!!!!")
        except Exception as e:
            print("exception: " + str(e))
    print("\n\n")

# IDAT
# Begin with image scanlines represented as described in Image layout; the layout and total size of this raw data are determined by the fields of IHDR.
# Filter the image data according to the filtering method specified by the IHDR chunk. (Note that with filter method 0, the only one currently defined, this implies prepending a filter type byte to each scanline.)
# Compress the filtered data using the compression method specified by the IHDR chunk.

# Each chunk consists of four parts:

# Length
# A 4-byte unsigned integer giving the number of bytes in the chunk's data field. The length counts only the data field, not itself, the chunk type code, or the CRC. Zero is a valid length. Although encoders and decoders should treat the length as unsigned, its value must not exceed 231-1 bytes.
# Chunk Type
# A 4-byte chunk type code. For convenience in description and in examining PNG files, type codes are restricted to consist of uppercase and lowercase ASCII letters (A-Z and a-z, or 65-90 and 97-122 decimal). However, encoders and decoders must treat the codes as fixed binary values, not character strings. For example, it would not be correct to represent the type code IDAT by the EBCDIC equivalents of those letters. Additional naming conventions for chunk types are discussed in the next section.
# Chunk Data
# The data bytes appropriate to the chunk type, if any. This field can be of zero length.
# CRC
# A 4-byte CRC (Cyclic Redundancy Check) calculated on the preceding bytes in the chunk, including the chunk type code and chunk data fields, but not including the length field. The CRC is always present, even for chunks containing no data. See CRC algorithm.
