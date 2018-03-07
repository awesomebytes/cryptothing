#!/usr/env/bin python

encrypted_text = "YMINNNUDZEHFQRITARBZRNVOLJGNVKOLSLREMOSEDFTTPQMMFLOZXMRUNPFFZFZVYAVGLGCEICKOAYGKUKAXWBBMTEMFSJLAUDDDWYCOSKVRILACTPDWYXHOYTCJFCFEPOOYHHPVYIKZMILDEYTEDIHDAPHJVIXNKHKZHYOQRBSPVYXETIXKSOVAYQZTNLEVEAAPZPGIWXGTAZMRVGZHGANOFEPOOYINDOSCRUDYJEJAENQNLNJJOHZSAREFCUAPZTCBFHZBMSGQJQJAKCKYEDFAYQRVBJWTZJXHUUKMOYPWVZGKQAFFAPXBLDFLGUJQFABGXFWQWSVWRDWYLQQZSZMLETTQYOQRBSPVYXETIXKVGLJKMKMIAAAEHFQRIORUVHHXQNMTKMJDFKNUEWPSCCIEHILSSOLQQNAZSSOLQQQJDXNLADACPPRVYXVCUYKFLOPFCHFPGWHGWEUKSSUSBRBBCACFICOOKZEVMSTTPXMZCVHNMSLCUAAUQROCTEJMXXAOHLQTTPZAXTRDNKLPYDZHCFXYVZGZFXBBEYOQRBSPVYXETIXKVGLJKMAZMOSCDWYCOOKRANDMIWUNIFQZVWFSMSGYHCRIHAVMPPQZHGXZRRMACTERBQFVDUGUHUOKBQSINYOQRBSPVYXETIXKVGLJKMYVMXMSFREZYBVZGCIEHILSUSGORBMWDTOXZBFBIOSCZSZABMBDCKHXDVZJFCOSCFEPOOYHUPBPXNNKSDABDQNMBBPXNNKSDABDQNMBBPXNNKSDABDQNMBBPXNNKSDABDQCCLPVYXETIXKVGLJKMKMIOETYOQRBSPVYXETIXKVGLJKMAZMOSCDWYCOOKRANDMIWUNIFQZVWFSMSGYHCRIHAVMPPQZHGXZRRMACTERBQFVDUGUHUOKBQSINYOQRBSPVYXETIXKVGLJKMYVMXMSFREZYBVZGCIEHILSUSGORBMWDTOXZBFBIOSCZSZABMBDCKHXDVZJFCOSCFEPOOYHUPBPXNNKSDABDQNMBBPXNNKSDABDQZQHJAIFEPOOYYST"

numbers = [23, 14, 1, 4, 5, 3, 7, 12, 6]

import string
string.ascii_uppercase
possible_key = ""
possible_key2 = ""
for n in numbers:
    possible_key += string.ascii_uppercase[n]
    #possible_key2 += string.ascii_uppercase[n+1]

# Hill Cipher
# Author: Rohit Yadav <rohit.yadav.cse07@itbhu.ac.in>
#         07020003, IDD Part IV, CSE

def hill(message, keymatrix, decrypt = False, alpha=string.ascii_uppercase + '0123456789 '):
    # from math import sqrt
    # n = int(sqrt(len(key)))
    # if n * n != len(key):
    #     raise Exception("Invalid key length, should be square-root-able like")

    #alpha = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.?,-;|'
    alpha = alpha
    print "[ALPHA LENGTH]: ", len(alpha)
    tonum = dict([(alpha[i], i * 1) for i in range(len(alpha))])

    # Pad the message with spacess if necessary
    # if len(message) % n > 0:
    #     print("Padding...")
    #     message += '|' * (n - (len(message) % n))

    # Construct our key matrix
    flat_list = [item for sublist in keymatrix for item in sublist]
    n = 3
    # key = 'XOBEFDHMI'
    keylist = []
    # for a in key:
    #     keylist.append(tonum[a])
    for a in flat_list:
        keylist.append(a)

    print("keylist:" + str(keylist))


    keymatrix = [] 
    for i in range(n): # loop 3
        keymatrix.append(keylist[i * n : i * n + n])

    print("keymatrix: " + str(keymatrix))

    from numpy import matrix
    from numpy import linalg

    keymatrix = matrix(keymatrix).round().T

    if decrypt:
        determinant = linalg.det(keymatrix).round()
        # print "[DETERMINANT]", determinant
        if determinant == 0:
            raise Exception("Determinant ZERO, CHANGE THE KEY!")
        elif determinant % len(alpha) == 0:
            raise Exception("Determinant divisible by ALPHA LENGTH, CHANGE THE KEY!")

        inverse = []
        keymatrix =  matrix(keymatrix.getI() * determinant).round()

        invdeterminant = 0
        for i in range(10000):
            if (determinant * i % len(alpha)) == 1:
                invdeterminant = i
                break

        # print "[INVERTED DETERMINANT]", invdeterminant

        # $uper l33t stuff: http://en.wikipedia.org/wiki/Modular_multiplicative_inverse
        for row in keymatrix.getA() * invdeterminant:
            newrow = []
            for i in row:
                newrow.append( i.round() % len(alpha) )
            inverse.append(newrow)
        
        keymatrix = matrix(inverse)

        # print "[DECIPHERING]: ", message
    else:
      print "[ENCIPHERING]: ", message

    # print "[MATRIX]\n", keymatrix

    # Main loop
    from string import join
    out = ''
    for i in range(len(message) / n):
        lst = matrix( [[tonum[a]] for a in message[i * n:i * n + n]] )
        # print("lst: " + str(lst))
        result = keymatrix * lst
        out += ''.join([alpha[int(result.A[j][0]) % len(alpha)] for j in range(len(result))])
    
    return out

key = possible_key
msg = encrypted_text
# cipherText = hill(msg, key)
# print "[CIPHERED TEXT]: |%s|\n" % cipherText
import string
cipherText = encrypted_text
numbers = string.digits
numbers2 = "0123456789"
space = " "
letters = string.ascii_uppercase

import itertools

matrix_vals =  [[23, 14, 1], [4, 5, 3], [7, 12, 8]]
matrix_vals2 = [[23, 14, 1], [4, 5, 3], [7, 12, 6]]
matrix_vals3 = [[23, 14, 1], [4, 5, 9], [7, 12, 6]]
matrix_vals4 = [[23, 14, 1], [4, 5, 9], [7, 12, 8]]

string.ascii_uppercase
possible_keys = [matrix_vals, matrix_vals2, matrix_vals3, matrix_vals4]

# tmp = ""
# for n in matrix_vals:
#     tmp += string.ascii_uppercase[n]
# possible_keys.append(tmp)

# tmp = ""
# for n in matrix_vals2:
#     tmp += string.ascii_uppercase[n]
# possible_keys.append(tmp)

# tmp = ""
# for n in matrix_vals3:
#     tmp += string.ascii_uppercase[n]
# possible_keys.append(tmp)

# tmp = ""
# for n in matrix_vals4:
#     tmp += string.ascii_uppercase[n]
# possible_keys.append(tmp)

# print("possible+keys: " + str(possible_keys))

for p in itertools.permutations([numbers, letters, space], 3):
    print(p)
    alpha = "".join(p)
    print("Trying alpha: " + str(alpha))
    for key in possible_keys:
        print("with key: " + str(key))
        decipherText = hill(cipherText, key, True, alpha=alpha)
        print("Result:")
        print(decipherText)
        print("\n")
    # print("with key: " + str(possible_key2))
    # decipherText = hill(cipherText, possible_key2, True, alpha=alpha)
    # print("Result:")
    # print(decipherText)

for p in itertools.permutations([numbers2, letters, space], 3):
    print(p)
    alpha = "".join(p)
    print("Trying alpha: " + str(alpha))
    for key in possible_keys:
        print("with key: " + str(key))
        decipherText = hill(cipherText, key, True, alpha=alpha)
        print("Result:")
        print(decipherText)
        print("\n")

for p in itertools.permutations([letters, space], 2):
    print(p)
    alpha = "".join(p)
    print("Trying alpha: " + str(alpha))
    for key in possible_keys:
        print("with key: " + str(key))
        decipherText = hill(cipherText, key, True, alpha=alpha)
        print("Result:")
        print(decipherText)
        print("\n")

for p in itertools.permutations([letters], 1):
    print(p)
    alpha = "".join(p)
    print("Trying alpha: " + str(alpha))
    for key in possible_keys:
        print("with key: " + str(key))
        flat_list = [item for sublist in key for item in sublist]
        actual_key = ""
        for num in flat_list:
            actual_key += string.ascii_uppercase[num]
        print("key as str: " + str(actual_key))
        print("used alpha: " + str(alpha))

        decipherText = hill(cipherText, key, True, alpha=alpha)
        print("Result:")
        print(decipherText)
        print("\n")

# for p in itertools.permutations([numbers2, letters, space], 3):
#     print(p)
#     alpha = "".join(p)
#     print("Trying alpha: " + str(alpha))
#     print("with key: " + str(possible_key))
#     decipherText = hill(cipherText, possible_key, True, alpha=alpha)
#     print("Result:")
#     print(decipherText)
#     print("\n")




# if decipherText.find('|') > -1 : decipherText = decipherText[:decipherText.find('|')]
# print "[DECIPHERED TEXT]: |%s|\n" % decipherText
# if( msg == decipherText ):
#     print "[ALGORITHM] CORRECT"
# else:
#     print "[ALGORITHM] INCORRECT"