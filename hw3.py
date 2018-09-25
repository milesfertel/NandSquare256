""" Basic template file that you should fill in for Problem Set 3. Some util
functions are provided from the NAND notebooks online that implement some
of the NAND essentials. """
from util import EVAL
from util import TRUTH
from util import NANDProgram

# TODO: Implement this function and return a string representation of its NAND
# implementation. You don't have to use the class we supplied - you could use
# other methods of building up your NAND program from scratch.
def nandsquare(n):
    '''Takes in an integer n. Outputs the string representation of a NAND prog
    that takes in inputs x_0, ..., x_{n-1} and squares it mod 2^n. The output
    will be y_0, ..., y_{n-1}. The first digit will be the least significant
    digit (ex: 110001 --> 35)'''
    # creates a blank NAND program with n inputs and n outputs.
    prog = NANDProgram(n, n, debug=False)
    prog.ONE("ONE")
    prog.ZERO("ZERO")

    partials = []
    # create partial sums
    for i in range(n):
        partial = ["ZERO" for z in range(i)]
        for j in range(n - len(partial)):
            partial.append(prog.allocate())
            prog.AND(partial[-1], prog.input_var(i), prog.input_var(j))
        partials.append(partial)

    # sum partial sums
    total = partials.pop(0)
    for index, partial in enumerate(partials):
        newtotal = total[:]
        carry = prog.allocate()

        newtotal[0] = prog.allocate()
        prog.ADD_3(newtotal[0] if index != len(partials) - 1 else prog.output_var(0), carry,
                   partial[0], total[0], "ZERO")
        last_carry = ""
        for i in range(1, n - 1):
            last_carry = carry
            carry = prog.allocate()
            newtotal[i] = prog.allocate()
            prog.ADD_3(newtotal[i] if index != len(partials) - 1 else prog.output_var(i), carry,
                       partial[i], total[i], last_carry)
        newtotal[n - 1] = prog.allocate()
        prog.ADD_3(newtotal[n - 1] if index != len(partials) - 1 else prog.output_var(n - 1), "TRASH",
                   partial[n - 1], total[n - 1], carry)
        total = newtotal

    # "compiles" your completed program as a NAND program string.
    return str(prog)

# TODO: Do this for bonus points and the leaderboard.
def nandsquare256():
    '''Implement nandsquare for a specific input size, n=256. This result gets
    placed on the leaderboard for extra credit. If you get close to the top
    score on the leaderboard, you'll still recieve BONUS POINTS!!!'''
    return nandsquare(256)


# Examples of using the NANDProgram class to build NAND Programs. Please don't
# worry too much about the details of using this class - this is not a class
# about designing NAND programs.
def nandadder(N):
    '''Creates a NAND adder that takes in two n-digit binary numbers and gets
    the sum, returning a n+1-digit binary number. Returns the string repr. of
    the NAND program created.'''
    nand = NANDProgram(2 * N, N + 1, debug=False) #set debug=True to show debug lines
    nand.ONE("ONE")

    carry = nand.allocate()
    nand.ADD_3(nand.output_var(0), carry,
               nand.input_var(0), nand.input_var(N), nand.NAND("ZERO", "ONE", "ONE"), debug=True)

    last_carry = ""
    for i in range(1, N - 1):
        last_carry = carry
        carry = nand.allocate()
        nand.ADD_3(nand.output_var(i), carry,
                   nand.input_var(i), nand.input_var(N + i), last_carry, debug=True)

    nand.ADD_3(nand.output_var(N-1), nand.output_var(N),
               nand.input_var(N-1), nand.input_var(2 * N - 1), carry, debug=True)
    return str(nand)

def tupToProg(t):
    nand = NANDProgram(t[0], t[1], debug=False)
    vs = [nand.input_var(v) for v in range(t[0])]
    i = 0
    for line in t[2]:
        if len(vs) >= t[0] + len(t[2]) - t[1]:
            vs.append(nand.output_var(i))
            i += 1
        else:
            vs.append(nand.allocate())
        nand.NAND(vs[line[0]], vs[line[1]], vs[line[2]])
    return str(nand)


if __name__ == '__main__':
    # Generate the string representation of a NAND prog. that adds numbers
    #TRUTH(tupToProg((3,1,((3,2,2),(4,1,1),(5,3,4),(6,2,1),(7,6,6),(8,0,0),(9,7,8),(10,5,0),(11,9,10)))))
    #addfive = str(nandadder(2))
    # Input Number 1: 11110 --> 15
    # Input Number 2: 10110 --> 13   1111010110
    # Expected Output: 28 --> 001110


    #816 0000110011
    #877 1011011011
    #  10111001011
    # print(EVAL(addfive,'1111'))

    def squaren(N):
        return str(nandsquare(N))

    #for bitcount in range(1, 6):
    #    print "bitcount: " + str(bitcount)
    #    square = squaren(bitcount)
    #    for value in range(2 ** bitcount):
    #        print "value: " + str(value)
    #        #valid = (('{0:0'+ str(bitcount) + 'b}').format(value ** 2))[::-1][:bitcount]
    #        res = EVAL(square, bin(2**10 + value)[2:][::-1][:bitcount])
    #        print(res)

    square = squaren(int(raw_input("number of bits:")))
    print len(square.split('\n'))
    print(EVAL(square, raw_input("binary: ")))
