import hashlib
import matplotlib.pyplot as plot
import random

def makeHash(k , v, outputSize):
    m = hashlib.md5()
    m.update(k.to_bytes(2, byteorder='big'))
    m.update(v.to_bytes(2, byteorder='big'))
    hexString = m.digest()
    bitString = bin(int.from_bytes(hexString, byteorder="big")).strip('0b')[:outputSize]
    cutHexString = int(bitString, 2).to_bytes(16, byteorder='big')
    return cutHexString

# The receiver of the commitment performs the attack
#We want to prove a a collition between ANY hashes since then we can change the vote. 
def conceilingAttack():
    x = list()
    y = list()
    k = random.getrandbits(16)
    v = random.getrandbits(1)
    for sizeOfHash in range(1, 30): # As MD5 has 128 bit output.
        x.append(sizeOfHash)
        commitment = makeHash(k, v, sizeOfHash)
        hits = 0
        uniqueHits = 0
        hashes = list()
        for kTest in range(0, pow(2,16)):
            v1Hash = makeHash(kTest, 1, sizeOfHash)
            v0Hash = makeHash(kTest, 0, sizeOfHash)
            if(v0Hash == commitment):
                hits += 1
            if (v1Hash == commitment):
                hits +=1
        if (hits is 1):
            uniqueHits += 1

        print("For K size " + str(sizeOfHash) + ", hits:", str(hits))
        #y.append(1 / hits)
        y.append(uniqueHits / pow(2, sizeOfHash))
    plot.plot(x, y)
    plot.xlabel('Size of hash')
    plot.ylabel('Probability of breaking conceiling')
    plot.title('Simulation')
    plot.show()

#The creator of the commitment performs the attack
# We want to be certain of the vote howto? If many collisions => Hard to be certain of the vote. 
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
                break   #( · ͜͞ʖ·) ̿'̿'\̵͇̿̿\з
        print("For K size " + str(sizeOfHash) + ", hits:", str(hits))
        y.append(hits)
    plot.plot(x, y)
    plot.xlabel('Size of hash')
    plot.ylabel('Probability of breaking binding')
    plot.title('Simulation')
    plot.show()

if __name__ == '__main__':
    #bindingAttack()
    conceilingAttack()