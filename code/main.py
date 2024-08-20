import numpy as np
import random
import matplotlib.pyplot as plt

from ibm import *

from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)


def generate_directions():

    directions = []
    # parties = [A,B,C]
    for p in range(3):
        dirn = random.randint(0, 1)
        if dirn == 0:
            directions.append('x')
        else:
            directions.append('y')
    return directions

def isValid(dir_list):
    if(dir_list[0] == 'x'):
        if(dir_list[1] == dir_list[2]): #b,c dirs must be equal
            return True 
        else:
            return False
    else:
        if(dir_list[1] != dir_list[2]): #b,c dirs must be equal
            return True 
        else:
            return False



def measure_table(dirns, bbit, cbit):
    print("dirns")
    print(dirns)
    print("bbit  " + str(bbit))
    print("cbit  " + str(cbit))
    if dirns[0] == 'x' and dirns[1] == 'x' and dirns[2] == 'x':
        # print("hi")
        if cbit == bbit:
            return 1
        else:
            return 0   

    elif dirns[0] == 'x':
        if cbit == bbit:
            return 0
        else:
            return 1

    elif dirns[1] == 'x' and dirns[2] == 'y':
        if cbit == bbit:
            return 0
        else:
            return 1
    else:
        if cbit == bbit:
            return 0
        else:
            return 1

  

def reconstruct(directions, B_bit, C_bit, honesty):

    if honesty == 0: # B and C cooperate

        return measure_table(directions,B_bit, C_bit)
        
    else: # B and C do not cooperate
        guess = random.randint(0, 1)
        return measure_table(directions, B_bit, guess)

def getList(dict): 
    return list(dict.keys()) 


n_valid = 0 #number of valid direction selections
total = 0 # total ghz states generated


def main():

    global n_valid
    global total

    dirs = []

    # generating the chosen directions
    while True:
        total += 1
        dirs = generate_directions()
        # print(dirs)
        if isValid(dirs) == True:
            n_valid += 1
            break;

    result = create_and_measure(dirs)
    
    measurements = getList(result)
    
    print(measurements[0])
    
    A_key = int(measurements[0][0])

    B_bit = int(measurements[0][1])
    C_bit = int(measurements[0][2])

    h = 0

    A_bit = reconstruct(dirs, B_bit, C_bit, h)

    # abit = measure_table(dirs, B_bit, C_bit)
    # print(abit)


    B_key = A_bit
    C_key = A_bit

    print('A_key : '  +str(A_key))
    print('B_key : '  +str(B_key))
    print('C_key : '  +str(C_key))

    # print("-->"+str(A_key) + str(B_key) + str(C_key))


    return A_key

k = 5 # how many bits we wish to generate

data = np.empty((0,2), int) # used for data collection


full_key = []

for i in range(k):

    full_key.append(main())

    # used for data collection
    data = np.append(data, np.array([[n_valid,total]]), axis = 0)

print (full_key)

# plotting stuff

coef = np.polyfit(data[:,0],data[:,1],1)

print(coef)
poly1d_fn = np.poly1d(coef) 
fig0 = plt.figure(0)

plt.title('Honest vs. Dishonest participants')

l1, = plt.plot( data[:,0], data[:,1], marker='',color='r',linestyle="-",label='Honest')
l2, = plt.plot(data[:,0], poly1d_fn(data[:,0]), '--k', label='$R={:.2f}+{:.2f}b$'.format(coef[1],coef[0]),linewidth=0.7)

plt.xlabel(r'\textbf{Key length (bits)}')
plt.ylabel(r'\textbf{Total Rounds} ')

fig0.savefig("test.pdf", bbox_inches='tight')
