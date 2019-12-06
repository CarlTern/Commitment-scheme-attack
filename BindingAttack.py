import hashlib
import timeit
import matplotlib.pyplot as plot
import random
import tkinter

def makeHash(k , v, outputSize):
    m = hashlib.md5()
    m.update(k.to_bytes(2, byteorder='big'))
    m.update(v.to_bytes(2, byteorder='big'))
    hexString = m.digest()
    bitString = bin(int.from_bytes(hexString, byteorder="big")).strip('0b')[:outputSize]
    cutHexString = int(bitString, 2).to_bytes(16, byteorder='big')
    return cutHexString

def conceilingAttack():
    x = list()
    y = list()
    # @TODO Implement attack 
    plot.plot(x, y)
    plot.xlabel('size of hash')
    plot.ylabel('Probability for collision')
    plot.title('Simulation')
    plot.show()

def bindingAttack():
    x = list()
    y = list()
    for sizeOfK in range(1, 129): # As MD5 has 128 bit output.
        x.append(sizeOfK)
        commitment = makeHash(0, 0, sizeOfK)
        hits = 0
        for k in range(0, pow(2,16)):
            if(makeHash(k, 1, sizeOfK) == commitment):
                hits += 1
        print("For K size " + str(sizeOfK) + ", hits:", str(hits))
        y.append(hits / pow(2, 16))
    plot.plot(x, y)
    plot.xlabel('size of hash')
    plot.ylabel('Probability for collision')
    plot.title('Simulation')
    plot.show()

if __name__ == '__main__':

    bindingAttack()
    conceilingAttack()