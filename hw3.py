""" Basic template file that you should fill in for Problem Set 3. Some util
functions are provided from the NAND notebooks online that implement some
of the NAND essentials. """
from util import EVAL
from util import TRUTH
from util import NANDProgram
from math import floor

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
    #return onandsquare(256)
    return fasternand256()

def fastestnand256():
    ''' TODO: Git gud '''
    n = 256
    prog = NANDProgram(n, n)
    prog.ONE("ONE")
    prog.ZERO("ZERO")

    partials = []
    table = {}
    # create symmetric partial sums
    for i in range(n):
        partial = ["ZERO" for z in range(i)]
        for j in range(n - len(partial)):
            if j + i >= 2 * i:
                partial.append(prog.allocate())
                prog.AND(partial[-1], prog.input_var(i), prog.input_var(j))
                table[str(i) + ' ' +  str(j)] = partial[-1]
            else:
                if str(i) + ' ' + str(j) in table:
                    partial.append(table[str(i) + ' ' + str(j)])
                elif str(j) + ' ' + str(i) in table:
                    partial.append(table[str(j) + ' ' + str(i)])
                else:
                    return
        partials.append(partial)

    def getHeight(partials, i):
        counter = 0
        for partial in partials:
            if partial[i] == "ZERO":
                return counter
            counter += 1
        return counter

    d = [2.0]
    while d[-1] < n:
        d.append(floor(d[-1] * 1.5))
    d.pop()

    while len(d) > 1:
        cutoff = d.pop()
        for col in range(n):
            colHeight = getHeight(partials, col)
            if colHeight == cutoff + 1:
                out = prog.allocate()
                carry = prog.allocate()

                prog.ADD_2(out, carry,
                           partials[0][col], partials[1][col])
            elif colHeight > cutoff + 1:
                out = prog.allocate()
                carry = prog.allocate()
                if col == n - 1:
                    prog.ADD_3_1(out,
                               partials[0][col], partials[1][col], partials[2][col])
                else:
                    prog.ADD_3(out, carry,
                               partials[0][col], partials[1][col], partials[2][col])

    # 256 bit adder
    prog.AND(prog.output_var(0), partials[0][0], "ONE")
    carry = ""
    for i in range(255):


    prog.ADD_3_1(prog.output_var(n - 1),
                 partials[0][255], partials[1][255], carry)


        return str(prog)



def fasternand256():
    '''Implement nandsquare for a specific input size, n=256. This result gets
    placed on the leaderboard for extra credit. If you get close to the top
    score on the leaderboard, you'll still recieve BONUS POINTS!!!'''
    n = 256
    prog = NANDProgram(n, n)
    prog.ONE("ONE")
    prog.ZERO("ZERO")

    half = n/2
    inputs = [prog.input_var(i) for i in range(n)]
    a = inputs[:half]
    b = inputs[half:]
    c = inputs[:half]
    d = inputs[half:]
    partials = []
    table = {}
    # create symmetric partial sums for BD
    for i in range(n/2):
        partial = ["ZERO" for _ in range(i)]
        for j in range(n/2):
            if j + i >= 2 * i:
                partial.append(prog.allocate())
                prog.AND(partial[-1], prog.input_var(i), prog.input_var(j))
                table[str(i) + ' ' +  str(j)] = partial[-1]
            else:
                if str(i) + ' ' + str(j) in table:
                    partial.append(table[str(i) + ' ' + str(j)])
                elif str(j) + ' ' + str(i) in table:
                    partial.append(table[str(j) + ' ' + str(i)])
                else:
                    print "PANIC"
                    return
        for j in range(n-len(partial)):
            partial.append("ZERO")
        partials.append(partial)

    # calculate BD
    seenzero = False
    total = partials.pop(0)
    prog.AND(prog.output_var(0), total[0], "ONE")
    for index, partial in enumerate(partials):
        newtotal = total[:]
        carry = prog.allocate()
        last_carry = ""
        prog.ADD_2(prog.output_var(index + 1), carry,
                   partial[index + 1], total[index + 1])
        if index == n/2 - 1:
            break;

        seenzero = False
        for i in range(index + 2, n - 1):
            last_carry = carry
            if seenzero:
                assert partial[i] == "ZERO"
                newtotal[i] = "ZERO"
            else:
                if partial[i] == "ZERO":
                    seenzero = True

                carry = prog.allocate()
                newtotal[i] = prog.allocate()
                prog.ADD_3(newtotal[i], carry,
                           partial[i], total[i], last_carry)
        # This can also be optimized for ZEROs
        if seenzero:
            assert partial[n - 1] == "ZERO"
            newtotal[n - 1] = "ZERO"
        else:
            newtotal[n - 1] = prog.allocate()
            prog.ADD_3(newtotal[n - 1], "TRASH",
                       partial[n - 1], total[n - 1], carry)
        total = newtotal

    # create partial sums for AD
    partials = []
    for i in range(n/2 - 1):
        partial = ["ZERO" for _ in range(i + (n / 2) + 1)]
        for j in range(n/2 - 1 - i):
            partial.append(prog.allocate())
            prog.AND(partial[-1], a[i], d[j])
        partials.append(partial)
    # calcualte AD
    for uindex, partial in enumerate(partials):
        newtotal = total[:]
        index = uindex + n/2
        carry = prog.allocate()
        last_carry = ""
        prog.ADD_2(prog.output_var(index + 1), carry,
                   partial[index + 1], total[index + 1])
        if index == n - 2:
            break;

        for i in range(index + 2, n - 1):
            last_carry = carry
            carry = prog.allocate()
            newtotal[i] = prog.allocate()
            prog.ADD_3(newtotal[i], carry,
                       partial[i], total[i], last_carry)
        newtotal[n - 1] = prog.allocate()
        prog.ADD_3(newtotal[n - 1], "TRASH",
                   partial[n - 1], total[n - 1], carry)
        total = newtotal

    # "compiles" your completed program as a NAND program string.
    return str(prog)

def fastnand256():
    '''Implement nandsquare for a specific input size, n=256. This result gets
    placed on the leaderboard for extra credit. If you get close to the top
    score on the leaderboard, you'll still recieve BONUS POINTS!!!'''
    n = 256
    prog = NANDProgram(n, n)
    prog.ONE("ONE")
    prog.ZERO("ZERO")

    table = {}
    half = n/2
    inputs = [prog.input_var(i) for i in range(n)]
    a = inputs[:half]
    b = inputs[half:]
    c = inputs[:half]
    d = inputs[half:]
    partials = []
    table = {}
    # create symmetric partial sums for BD
    for i in range(n/2):
        partial = ["ZERO" for _ in range(i)]
        for j in range(n/2):
            if j + i >= 2 * i:
                partial.append(prog.allocate())
                prog.AND(partial[-1], prog.input_var(i), prog.input_var(j))
                table[str(i) + ' ' +  str(j)] = partial[-1]
            else:
                if str(i) + ' ' + str(j) in table:
                    partial.append(table[str(i) + ' ' + str(j)])
                elif str(j) + ' ' + str(i) in table:
                    partial.append(table[str(j) + ' ' + str(i)])
                else:
                    print "PANIC"
                    return
        for j in range(n-len(partial)):
            partial.append("ZERO")
        partials.append(partial)

    # calculate BD
    seenzero = False
    total = partials.pop(0)
    prog.AND(prog.output_var(0), total[0], "ONE")
    for index, partial in enumerate(partials):
        newtotal = total[:]
        carry = prog.allocate()
        last_carry = ""
        prog.ADD_3(prog.output_var(index + 1), carry,
                   partial[index + 1], total[index + 1], "ZERO")
        if index == n/2 - 1:
            break;

        seenzero = False
        for i in range(index + 2, n - 1):
            last_carry = carry
            if seenzero:
                assert partial[i] == "ZERO"
                newtotal[i] = "ZERO"
            else:
                if partial[i] == "ZERO":
                    seenzero = True

                carry = prog.allocate()
                newtotal[i] = prog.allocate()
                prog.ADD_3(newtotal[i], carry,
                           partial[i], total[i], last_carry)
        if seenzero:
            assert partial[n - 1] == "ZERO"
            newtotal[n - 1] = "ZERO"
        else:
            newtotal[n - 1] = prog.allocate()
            prog.ADD_3(newtotal[n - 1], "TRASH",
                       partial[n - 1], total[n - 1], carry)
        total = newtotal

    # create partial sums for AD
    partials = []
    for i in range(n/2 - 1):
        partial = ["ZERO" for _ in range(i + (n / 2) + 1)]
        for j in range(n/2 - 1 - i):
            partial.append(prog.allocate())
            prog.AND(partial[-1], a[i], d[j])
        partials.append(partial)
    # calcualte AD
    for uindex, partial in enumerate(partials):
        newtotal = total[:]
        index = uindex + n/2
        carry = prog.allocate()
        last_carry = ""
        prog.ADD_3(prog.output_var(index + 1), carry,
                   partial[index + 1], total[index + 1], "ZERO")
        if index == n - 2:
            break;

        for i in range(index + 2, n - 1):
            last_carry = carry
            carry = prog.allocate()
            newtotal[i] = prog.allocate()
            prog.ADD_3(newtotal[i], carry,
                       partial[i], total[i], last_carry)
        newtotal[n - 1] = prog.allocate()
        prog.ADD_3(newtotal[n - 1], "TRASH",
                   partial[n - 1], total[n - 1], carry)
        total = newtotal

    # "compiles" your completed program as a NAND program string.
    return str(prog)

## TODO: Do this for bonus points and the leaderboard.
def onandsquare(n):
    '''Implement nandsquare for a specific input size, n=256. This result gets
    placed on the leaderboard for extra credit. If you get close to the top
    score on the leaderboard, you'll still recieve BONUS POINTS!!!'''
    prog = NANDProgram(n, n)
    prog.ONE("ONE")
    prog.ZERO("ZERO")
    partials = []
    table = {}
    # create symmetric partial sums
    for i in range(n):
        partial = ["ZERO" for z in range(i)]
        for j in range(n - len(partial)):
            if j + i >= 2 * i:
                partial.append(prog.allocate())
                prog.AND(partial[-1], prog.input_var(i), prog.input_var(j))
                table[str(i) + ' ' +  str(j)] = partial[-1]
            else:
                if str(i) + ' ' + str(j) in table:
                    partial.append(table[str(i) + ' ' + str(j)])
                elif str(j) + ' ' + str(i) in table:
                    partial.append(table[str(j) + ' ' + str(i)])
                else:
                    print "PANIC"
                    return
        partials.append(partial)

    # sum partial sums
    total = partials.pop(0)
    prog.AND(prog.output_var(0), total[0], "ONE")
    for index, partial in enumerate(partials):
        newtotal = total[:]
        carry = prog.allocate()
        last_carry = ""
        prog.ADD_3(prog.output_var(index + 1), carry,
                   partial[index + 1], total[index + 1], "ZERO")
        if index == 254:
            break;

        for i in range(index + 2, n - 1):
            last_carry = carry
            carry = prog.allocate()
            newtotal[i] = prog.allocate()
            prog.ADD_3(newtotal[i], carry,
                       partial[i], total[i], last_carry)
        newtotal[n - 1] = prog.allocate()
        prog.ADD_3(newtotal[n - 1], "TRASH",
                   partial[n - 1], total[n - 1], carry)
        total = newtotal

    # "compiles" your completed program as a NAND program string.
    return str(prog)

# TODO: Do this for bonus points and the leaderboard.
def onandsquare256():
    '''Implement nandsquare for a specific input size, n=256. This result gets
    placed on the leaderboard for extra credit. If you get close to the top
    score on the leaderboard, you'll still recieve BONUS POINTS!!!'''
    n = 256
    prog = NANDProgram(n, n)
    prog.ONE("ONE")
    prog.ZERO("ZERO")
    partials = []
    table = {}
    # create symmetric partial sums
    for i in range(n):
        partial = ["ZERO" for z in range(i)]
        for j in range(n - len(partial)):
            if j + i >= 2 * i:
                partial.append(prog.allocate())
                prog.AND(partial[-1], prog.input_var(i), prog.input_var(j))
                table[str(i) + ' ' +  str(j)] = partial[-1]
            else:
                if str(i) + ' ' + str(j) in table:
                    partial.append(table[str(i) + ' ' + str(j)])
                elif str(j) + ' ' + str(i) in table:
                    partial.append(table[str(j) + ' ' + str(i)])
                else:
                    print "PANIC"
                    return
        partials.append(partial)

    # sum partial sums
    total = partials.pop(0)
    prog.AND(prog.output_var(0), total[0], "ONE")
    for index, partial in enumerate(partials):
        newtotal = total[:]
        carry = prog.allocate()
        last_carry = ""
        prog.ADD_3(prog.output_var(index + 1), carry,
                   partial[index + 1], total[index + 1], "ZERO")
        if index == 254:
            break;

        for i in range(index + 2, n - 1):
            last_carry = carry
            carry = prog.allocate()
            newtotal[i] = prog.allocate()
            prog.ADD_3(newtotal[i], carry,
                       partial[i], total[i], last_carry)
        newtotal[n - 1] = prog.allocate()
        prog.ADD_3(newtotal[n - 1], "TRASH",
                   partial[n - 1], total[n - 1], carry)
        total = newtotal

    # "compiles" your completed program as a NAND program string.
    return str(prog)
#
## TODO: Do this for bonus points and the leaderboard.
#def oldnandsquare256():
#    '''Implement nandsquare for a specific input size, n=256. This result gets
#    placed on the leaderboard for extra credit. If you get close to the top
#    score on the leaderboard, you'll still recieve BONUS POINTS!!!'''
#    prog = NANDProgram(256, 256)
#    prog.ONE("ONE")
#    prog.ZERO("ZERO")
#    n = 256
#    partials = []
#    table = {}
#    # create partial sums
#    for i in range(n):
#        partial = ["ZERO" for z in range(i)]
#        for j in range(n - len(partial)):
#            if j + i >= 2 * i:
#                partial.append(prog.allocate())
#                prog.AND(partial[-1], prog.input_var(i), prog.input_var(j))
#                table[str(i) + ' ' +  str(j)] = partial[-1]
#            else:
#                if str(i) + ' ' + str(j) in table:
#                    partial.append(table[str(i) + ' ' + str(j)])
#                elif str(j) + ' ' + str(i) in table:
#                    partial.append(table[str(j) + ' ' + str(i)])
#                else:
#                    print "PANIC"
#                    return
#        partials.append(partial)
#
#    # sum partial sums
#    total = partials.pop(0)
#    for index, partial in enumerate(partials):
#        newtotal = total[:]
#        carry = prog.allocate()
#
#        newtotal[0] = prog.allocate()
#        prog.ADD_3(newtotal[0] if index != len(partials) - 1 else prog.output_var(0), carry,
#                   partial[0], total[0], "ZERO")
#        last_carry = ""
#        for i in range(1, n - 1):
#            last_carry = carry
#            carry = prog.allocate()
#            newtotal[i] = prog.allocate()
#            prog.ADD_3(newtotal[i] if index != len(partials) - 1 else prog.output_var(i), carry,
#                       partial[i], total[i], last_carry)
#        newtotal[n - 1] = prog.allocate()
#        prog.ADD_3(newtotal[n - 1] if index != len(partials) - 1 else prog.output_var(n - 1), "TRASH",
#                   partial[n - 1], total[n - 1], carry)
#        total = newtotal
#
#    # "compiles" your completed program as a NAND program string.
#    return str(prog)
#

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
    #print(tupToProg((3,1,((3,2,2),(4,1,1),(5,3,4),(6,2,1),(7,6,6),(8,0,0),(9,7,8),(10,5,0),(11,9,10)))))
    #addfive = str(nandadder(2))
    # Input Number 1: 11110 --> 15
    # Input Number 2: 10110 --> 13   1111010110
    # Expected Output: 28 --> 001110


    #816 0000110011
    #877 1011011011
    #  10111001011
    # print(EVAL(addfive,'1111'))

    #def squaren(N):
    #    return str(nandsquare(N))

    #for bitcount in range(1, 6):
    #    print "bitcount: " + str(bitcount)
    #    square = squaren(bitcount)
    #    for value in range(2 ** bitcount):
    #        print "value: " + str(value)
    #        #valid = (('{0:0'+ str(bitcount) + 'b}').format(value ** 2))[::-1][:bitcount]
    #        res = EVAL(square, bin(2**10 + value)[2:][::-1][:bitcount])
    #        print(res)

    #square = squaren(int(raw_input("number of bits:")))
    #print len(square.split('\n'))
    #print(EVAL(nandsquare256(), '10001' + '0'*251))
    #TRUTH(square)
    fastestnand256()
    #print len(nandsquare256().split('\n'))
    #print len(onandsquare(256).split('\n'))
    #print TRUTH(knandsquare256()) == TRUTH(nandsquare(6))
