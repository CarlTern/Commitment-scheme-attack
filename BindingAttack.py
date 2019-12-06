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

# The receiver of the commitment performs the attack
def conceilingAttack():
    x = list()
    y = list()
    k = random.getrandbits(16)
    v = random.getrandbits(1)
    for sizeOfHash in range(1, 30): # As MD5 has 128 bit output.
        x.append(sizeOfHash)
        commitment = makeHash(k, v, sizeOfHash)
        hits = 0
        for kTest in range(0, pow(2,16)):
            for vTest in range(2):
                if(makeHash(kTest, vTest, sizeOfHash) == commitment and vTest == v):
                    hits += 1
        print("For K size " + str(sizeOfHash) + ", hits:", str(hits))
        y.append(hits / (2 * pow(2, 16)))
    plot.plot(x, y)
    plot.xlabel('Size of hash')
    plot.ylabel('Probability of breaking conceiling')
    plot.title('Simulation')
    plot.show()

#The creator of the commitment performs the attack
def bindingAttack():
    x = list()
    y = list()
    for sizeOfHash in range(1, 129): # As MD5 has 128 bit output.
        x.append(sizeOfHash)
        commitment = makeHash(0, 0, sizeOfHash)
        hits = 0
        for k in range(0, pow(2,16)):
            if(makeHash(k, 1, sizeOfHash) == commitment):
                hits += 1
        print("For K size " + str(sizeOfHash) + ", hits:", str(hits))
        y.append(hits / pow(2, 16))
    plot.plot(x, y)
    plot.xlabel('Size of hash')
    plot.ylabel('Probability of breaking binding')
    plot.title('Simulation')
    plot.show()

if __name__ == '__main__':
    #bindingAttack()
    conceilingAttack()