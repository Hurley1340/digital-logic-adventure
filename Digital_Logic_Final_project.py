###################################
# Program: Digital Logic Adventure
# Takes the user through a series of events that give an introduction to Digital Logic
# Author: Chapin Hurley
# Date: 6/2/2025
# Description: The user recieves a user-defined amount of floats that are selected using
# rand.gauss which selects either voltages that are distributed bimodally around 4.5 and .5V
# The user is asked to clean up the data by getting rid of indeterminate voltage levels
# The user selects a threshold level and the voltages are then converted into a binary bitstream
# Bitstream is reshaped to an n x 50 matrix then a pixilized representation is generated
# The program creates a new bitstream and the user decides what logic to send the two
# bitstreams into, AND, OR, XOR. A timing diagram is created and the user is asked to
# figure out what the logic gates does. Finally, the user is shown how to take her pixel image
# and use the XOR gate to scramble and unscramble the image.
###################################


import matplotlib.pyplot as plt #Import libraries
import random
import numpy as np
#Welcome Page
print(f"{'Welcome to a Digital Logic Adventure!': ^100}")
print('-'*100)
print('-'*100)
print("\u2022 There's a transmission signal coming in with varying voltage levels!")
print("\u2022 The frequency of the transmission is 50 Hz (50 data points per second)")

#Part I
#User chooses how many seconds to receieve transmission signal
#Error checks to make sure no invalid data is entered
while True:
    seconds = input('Choose how many (integer) seconds you want receive data for (max 100): ')
    try :
        seconds = int(seconds)
        if seconds <= 100 and seconds >= 10:
            break
        elif seconds <= 0:
            print("No negative seconds and no Zeros! ... c'mon")
        else:
            print("You need to choose a better (higher) number")
    except ValueError:
        print("This isn't valid input")
#Create a list of voltages received.
#Voltages are in a -bimodal- normal distrubution around 4.5 V and .5 V
bitstream = []
new_bitstream = [] #We use this later
indeterminate = 0 #accumulator for indeterminant values
for i in range(50 * seconds): #loop runs for user-defined num seconds
    negative = True #Must be false to break out of loop
    match random.randint(0,1): #heads or tails
        case 0:
            while(negative):
                level = random.gauss(4.5, .4) #chooses a number in Mode A
                if level > 0:
                    negative = False
        case 1:
            while(negative):
                level = random.gauss(.5, .4) #chooses a number in Mode B
                if level > 0:
                    negative = False
    if (level > 1.5 and level < 3.5):
        indeterminate += 1 #increment indeterminate value accumulator
    bitstream.append(level) #add the level to the list
#print(indeterminate)
#print(bitstream)
print(f'You received {len(bitstream)} distinct voltage levels, each between 0.0 and 6.5 volts')
print('-' *100)
print(f"The program made a list that contains all {len(bitstream)} data points... here's a sample")
print()
print(bitstream[:5]) #show the first 5 voltage levels in the bitstream

#Part II user cleans up the data
print(f"{'Now We Clean Up our Data':^100}")
print('-' * 100)
print("\u2022 The Voltages need to be either High or Low! We can't allow indeterminate data")
print("\u2022 0 Volts is the ideal Low voltage and 5.0 Volts is the ideal high voltage (in this context)")
print("\u2022 We need to search for indeterminate data points and force them into a category of High or Low")
print('-' * 101)

#Transform list into numpy array
bitstream = np.array(bitstream)
rows = seconds #copy the variable
#Show the user the indeterminate voltages received and their index in the array
print("""Let's find out info about the indeterminate values you received.
Anything over 1.5 V and below 3.5 V is indeterminate""")
#Create a Boolean Mask to find the values and locations
locmask = np.logical_and(bitstream > 1.5, bitstream < 3.5) #Boolean Mask to mask unwanted data
indet_values = bitstream[locmask]
#This is tricky. np.where returns a tuple of arrays
locations = np.where(locmask == True)[0] #Hence this [0] index
indet_values
#Zip the locations and the values of indeterminate voltages together
zipped = zip(locations, indet_values) #Zip Function
print('-' *65)
print(f'{"Index":^6} |  {"Indeterminate Voltages Received"}')
print('-' * 40 )
#Print the locations and values together.
for loc, val in zipped: #Loop to print out zipped data
    print(f'{loc: >6} |  {val:.4f} V')
print('-' * 40)
print(f'For a total of {indeterminate} indeterminate values')

print(f'This is a visualization of the voltages your recieved.')
print(f'Each row represents 1 second and 50 points of data')
shaped_arr = bitstream.reshape(rows, 50)

fig, ax = plt.subplots(figsize = (8,8))
image = shaped_arr #cast to np.array and reshape
plt.imshow(image, aspect = 'equal')
plt.show()

#Ask user how to sort the indeterminate voltages
print("\n-You get to decide how to sort this data-")
print("You need to transform your data into a binary: High and Low")
print('-' * 90)
while True:
    threshold = input(f"What should the threshold for low voltages be? Remember, 5V is High and 0V is Low: ")
    try:
        threshold = float(threshold) #try to cast the user input to a float
        if threshold <= 1.5 or threshold >= 3.5:
            print("These aren't threshold values, try again.")
            continue
        else :
            break
    except ValueError:
        print("This isn't valid input, try again")
#Educational
print(f"""You chose {threshold} V,
\u2022 Everything below this value will be classified as Low
\u2022 Everything above will be classified as High""")
print()
print("""Now we transform these voltages into a bitstream.
Let's take a look at the first and last rows of your bitstream""")
print()
#Convert voltages into bitstream
for i in range(len(bitstream)):
    if bitstream[i] < threshold:
       bitstream[i] = 0
    else:
       bitstream[i] = 1
bitstream = bitstream.astype(int)
#Show the user the first and last rows of the bitstream she created
print(f'{bitstream[:50]}  |*|  {bitstream[len(bitstream)-50:]}')

#Part III
#use the np array to get a pixel image
print(f'This is a visualization of the bitstream you defined!')
print(f'Each row represents 1 second and 50 points of data')
shaped_arr = bitstream.reshape(rows, 50)

fig, ax = plt.subplots(figsize = (8,8))
image = shaped_arr #cast to np.array and reshape
plt.imshow(image, aspect = 'equal')
plt.show()
print("-" * 80)
#Behind the scenes a new bitstream is created that matches user's bitstream length
print("The program is now generating a new bitstream that matches your bitstream's size")
print("In the next section your bitstream will interact with the program's bitstream")
new_bitstream = np.empty(len(bitstream), dtype=int)  # make an empty np.array
for i in range (len(bitstream)): # 50-50 chance of 1 or 0
    match random.randint(0,1):
        case 0:
            new_bitstream[i] = 1
        case 1:
            new_bitstream[i] = 0

#Part IV
#User chooses a Gate and a New Bitstream is created from her choice

print("""A logic gate is a device with inputs that performs a logical operation
based on what is presented at its inputs. The inputs can only be High or Low-
and the gate can only do one operation at a time.
The two inputs will be your bitstream and the program's bitstream.\n""")

#lists that make user input more flexible
AND = ['a','and', 'and gate']
OR = ['or','b', 'or gate']
XOR = ['c', 'xor','xor gate']

#The user may choose 'b' or type 'or' to choose the OR gate.
def gate_choice():
    """ The user is asked to choose 1 of 3 logic gates. AND, OR, XOR.
    The function returns the user's gate choice as a capitalized string. """
    while True:
        user_gate = input("""--Pick a Logic Gate to send the two bitstream into:
    a) AND Gate
    b) OR Gate
    c) XOR Gate """).strip().lower() #lowercase the user input
        if user_gate in OR:
            user_gate = 'OR'
            break
        elif user_gate in AND:
            user_gate = 'AND'
            break
        elif user_gate in XOR:
            user_gate = 'XOR'
            break
        else:
            print("Please choose a valid option (a, b, or c).")
            continue
    return user_gate #return the user's choice of gate

def calc_user_gate_stream(user_gate): #pass user_gate
    """This function depends on the user_gate_choice, the only parameter
    Another bitstream called user_gate_stream is created using the user-defined
    bitstream and the program-created bitstream with the bitwise
    and(&)/or(|)/xor(^) functions. The user defined stream is the logical result.
    The function returns the user_gate_stream as a numpy array.
    """
    if user_gate == 'OR': #make new bitsreams
        or_stream = bitstream | new_bitstream
        user_gate_stream = or_stream
    elif user_gate == 'AND':
        and_stream = bitstream & new_bitstream
        user_gate_stream = and_stream
    else:
        xor_stream = bitstream ^ new_bitstream
        user_gate_stream = xor_stream
    return user_gate_stream

user_gate = gate_choice()
print(f"\nYou chose an {user_gate} gate.")
user_gate_stream = calc_user_gate_stream(user_gate)

#Test Block
#print(new_bitstream[:12])
#print(bitstream[:12])
#print(or_stream[:12])
#print(and_stream[:12])
#print(xor_stream[:12])

#Part V
#Step Plot Timing Diagram and Puzzle for the user
print("Here is the first 2 bytes (16 bits) of the two streams, side by side")
print(f'Your bitstream:       {bitstream[:16]}')
print(f"Program's bitstream:  {new_bitstream[:16]}")

x = np.arange(0,16) # the graph shows before the 0 on the x-axis
fig, ax = plt.subplots(figsize = (8,8))
#changed from 'mid' to 'pre'
ax.step(x, bitstream[:16] + 1.6, where='mid') #y1 is offset by 1.3
ax.step(x, new_bitstream[:16] + 0.00, where='mid')
ax.step(x, user_gate_stream[:16]+ -1.6, where='mid')

ax.set_title(f'{user_gate} Gate Timing Diagram\n', fontsize = 16, fontweight ='bold')
ax.set_xlabel('Time (ms)')
ax.set_xticks(np.arange(0,16))
ax.set_xticklabels(np.arange(0,32, 2))
#ax.set_xticklabels((np.linspace(0,.32,16)).round(2))
ax.set_yticks([0.5, 2.1, -1])
ax.set_yticklabels(['New bitstream', 'Your bitstream','Output'])
#spines grant access to the terminal edges of the graph space
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(True)

plt.axis('scaled') # this feature gives it the proper scale 1:1
plt.xlim(-0.75, 17)
plt.show()
print("Can you figure out what your chosen logic gate is doing?")
print(f"What is the logic that the {user_gate} gate performs?")
print("-" * 80)

# Part VI
# Show the user an application of the XOR gate
# The user can see the bitstream scrambled and unscrambled

print("Now let's use XOR to scramble and unscramble your bitstream.")
print("-" * 80)
print("XOR has a special property: if you XOR data with the same key twice,")
print("you get the original data back.")
print()
print("Step 1: Original bitstream XOR program key = scrambled bitstream")
print("Step 2: Scrambled bitstream XOR same program key = original bitstream again")
print()
print("In other words:")
print("    original ^ key  = scrambled")
print("    scrambled ^ key = original")
print("-" * 80)

# The program's bitstream acts like a key
key = new_bitstream

# Scramble the user's bitstream by XORing it with the key
scramble = bitstream ^ key

# Unscramble the scrambled bitstream by XORing it with the same key again
unscramble = scramble ^ key

# Reshape the arrays so they can be displayed as pixel images
shaped_arr = bitstream.reshape(rows, 50)
shaped_key = key.reshape(rows, 50)
shaped_scramble = scramble.reshape(rows, 50)
shaped_unscramble = unscramble.reshape(rows, 50)

# Display the original, key, scrambled, and unscrambled bitstreams
fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=1, ncols=4, figsize=(12, 8))

ax1.set_title("Original")
ax2.set_title("Key")
ax3.set_title("Scrambled")
ax4.set_title("Unscrambled")

ax1.imshow(shaped_arr, aspect='equal')
ax2.imshow(shaped_key, aspect='equal')
ax3.imshow(shaped_scramble, aspect='equal')
ax4.imshow(shaped_unscramble, aspect='equal')

# Remove axis numbers/ticks to make the images cleaner
ax1.axis('off')
ax2.axis('off')
ax3.axis('off')
ax4.axis('off')

plt.tight_layout()
plt.show()

print()
print("The scrambled image looks random because each bit was XORed with the key.")
print("The unscrambled image matches the original because XORing with the same key twice cancels the key.")
print()
print("Thanks for taking part in this Digital Adventure!")