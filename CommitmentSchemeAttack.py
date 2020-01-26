import hashlib
import matplotlib.pyplot as plot
import random

def makeHash(k , v):
    bitString =str(v) + str(bin(k)[2:])
    md5Hash = hashlib.md5(bitString.encode()).hexdigest()
    
    return (bin(int(md5Hash, 16))[2:]).zfill(128)

def truncate(bitString, outputSize):

    return bitString[:outputSize]


def createCommitments():
  # First we create the different commitments.
    commitmentsIsVote0 = list()
    commitmentsIsVote1 = list()
    for k in range(0, pow(2,16)):
        commitmentsIsVote0.append(makeHash(k, 0))
        commitmentsIsVote1.append(makeHash(k, 1))
    print("succesfully created hashes!")
    return commitmentsIsVote0, commitmentsIsVote1

# The receiver of the commitment performs the attack
#We want to prove a a collition between ANY hashes since then we can change the vote. 
def conceilingAttack(commitmentsIsVote0, commitmentsIsVote1):
    x = list()
    y = list()

    #The start of the sumilation. For every size of hash, let's simulate.     
    for sizeOfHash in range(1, 129): # As MD5 has 128 bit output.
        print("Current size:", sizeOfHash)
        x.append(sizeOfHash)
        hashes = dict()
        for i in range(pow(2, 16)):
            truncatedHash0 = truncate(commitmentsIsVote0[i], sizeOfHash)
            truncatedHash1 = truncate(commitmentsIsVote1[i], sizeOfHash)
            
            if(truncatedHash0 in hashes):
                hashes[truncatedHash0][0] +=1
            else:
                hashes[truncatedHash0] = [1, 0]
            
            #let's check vote 1 too. 
            if(truncatedHash1 in hashes):
                hashes[truncatedHash1][1] +=1
            else:
                hashes[truncatedHash1] = [0, 1]

        hashesWithoutCollisions = 0
        for hash in hashes:
            if(hashes[hash][0] == 0 or hashes[hash][1] == 0): # If no collisions => we can break the conceiling. 
                hashesWithoutCollisions += 1
        y.append(hashesWithoutCollisions / len(hashes))
    plot.plot(x, y)
    plot.xlabel('Size of hash')
    plot.ylabel('Probability of breaking concealing')
    plot.title('Simulation')
    plot.show()

#The creator of the commitment performs the attack
# We want to be certain of the vote howto? If many collisions => Hard to be certain of the vote. 
def bindingAttack(commitmentsIsVote0, commitmentsIsVote1):
    x = list()
    y = list()

    #The start of the sumilation. For every size of hash, let's simulate.     
    for sizeOfHash in range(1, 129): # As MD5 has 128 bit output.
        print("Current size:", sizeOfHash)
        x.append(sizeOfHash)
        hasCollision = 0 # Either 0% or 100%
        hashes = dict()
        for i in range(pow(2, 16)):
            truncatedHash0 = truncate(commitmentsIsVote0[i], sizeOfHash)
            truncatedHash1 = truncate(commitmentsIsVote1[i], sizeOfHash)
            
            if(truncatedHash0 in hashes):
                hashes[truncatedHash0][0] +=1
            else:
                hashes[truncatedHash0] = [1, 0]
            
            #let's check vote 1 too. 
            if(truncatedHash1 in hashes):
                hashes[truncatedHash1][1] +=1
            else:
                hashes[truncatedHash1] = [0, 1]

        for hash in hashes:
            if(hashes[hash][0] > 0 and hashes[hash][1] > 0):
                hasCollision = 1
                break
        y.append(hasCollision)
    plot.plot(x, y)
    plot.xlabel('Size of hash')
    plot.ylabel('Probability of breaking binding')
    plot.title('Simulation')
    plot.show()

if __name__ == '__main__':
    commitmentsIsVote0, commitmentsIsVote1 = createCommitments()
    #bindingAttack(commitmentsIsVote0, commitmentsIsVote1)
    conceilingAttack(commitmentsIsVote0, commitmentsIsVote1)