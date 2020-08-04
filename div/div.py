import struct
import random

# SIGN_INDEX = 31
# MANTIS_INDEX = 22
# BIAS = 127
# MAX_EXPONENT = 128
# MIN_EXPONENT = -127
SIGN_INDEX = 0
MANTIS_INDEX = 12
BIAS = 1023
MAX_EXPONENT = 1024
MIN_EXPONENT = -1023


class IEEE:
    def __init__(self, number):
        number = floatToBinary64(number)
        print(number)
        self.sign = int(number[SIGN_INDEX])
        self.mantis = '1' + number[MANTIS_INDEX:]
        # self.mantis = int(mantis, 2)
        self.exponent = int(number[1: MANTIS_INDEX], 2) - BIAS

    def __str__(self):
        return 'm: {}, exp: {}, sign: {}'.format(self.mantis, self.exponent, self.sign)

    def __repr__(self):
        return 'm: {}, exp: {}, sign: {}'.format(self.mantis, self.exponent, self.sign)

    def get_decimal(self):
        pass

    def get_binary32(self):
        pass


class Div:  # a / b
    def __init__(self, a, b):
        self.a = IEEE(a)
        self.b = IEEE(b)
        self.sign_bit = None
        self.mantis = None
        self.exponent = None
        self.Q = None
        self.is_finished = False

    def divison(self):
        self.is_valid()

        if self.is_finished == True:
            return self.get_result

        self.sign_bit = self.a.sign ^ self.b.sign
        self.exponent = self.a.exponent - self.b.exponent + BIAS
        self.calc_mantis()
        self.normalize()
        self.check_overflow()
        self.check_underflow()
        return self.get_result()

    def is_valid(self):
        len_mantis = len(self.a.mantis)
        zero_pattern = '0' * len_mantis         # 00000000000000
        one_pattern = '1' * len_mantis          # 11111111111111

        # a=NaN or b=NaN -> z=NaN
        if (self.a.exponent == MAX_EXPONENT and self.a.mantis != zero_pattern) or (self.b.exponent == MAX_EXPONENT and self.b.mantis != zero_pattern):
            self.sign_bit = 0
            self.exponent = MAX_EXPONENT
            self.mantis = one_pattern
            self.is_finished = True

        # a=inf or b=inf -> z=inf
        elif (self.a.exponent == MAX_EXPONENT and self.a.mantis == zero_pattern and not(self.b.exponent == MIN_EXPONENT and self.b.mantis == zero_pattern)) or (self.b.exponent == MAX_EXPONENT and self.b.mantis == zero_pattern and not(self.b.exponent == MIN_EXPONENT and self.b.mantis == zero_pattern)):
            self.sign_bit = self.a.sign ^ self.b.sign
            self.exponent = MAX_EXPONENT
            self.mantis = one_pattern
            self.is_finished = True

        # a=0,b=inf or a=inf,b=0 -> z=NaN
        elif ((self.a.exponent == MAX_EXPONENT and self.a.mantis == zero_pattern and self.b.exponent == MIN_EXPONENT and self.b.mantis == zero_pattern) or (self.b.exponent == MAX_EXPONENT and self.b.mantis == zero_pattern and self.b.exponent == MIN_EXPONENT and self.b.mantis == zero_pattern)):
            self.sign_bit = 0
            self.exponent = MAX_EXPONENT
            self.mantis = one_pattern
            self.is_finished = True

    def check_overflow(self):
        MAX = 2046 if len(self.a.mantis) == 53 else 254
        if self.exponent > MAX:
            self.is_finished = True
            self.sign_bit = self.a.sign ^ self.b.sign
            self.exponent = 1024
            self.mantis = '0' * len(self.a.mantis)

    def check_underflow(self):
        if self.exponent < 1:
            self.is_finished = True
            self.sign_bit = self.a.sign ^ self.b.sign
            self.exponent = 0
            self.mantis = '0' * len(self.a.mantis)

    def calc_mantis(self):
        len_mantis = len(self.a.mantis)
        count = round((len_mantis - 1) / 2)
        Q = '1' + self.a.mantis + '0' * (len_mantis - 1)
        M = '1' + self.b.mantis + '0' * (len_mantis)
        A = '0' * (len_mantis * 2 + 1)
        for i in range(count):
            for _ in range(4):
                if A[0] == '1':
                    A = A[1:] + Q[0:1]  # {A,Q} = {A,Q} << 1;
                    Q = Q[1:] + '0'
                    A = adder(A, M)
                else:
                    A = A[1:] + Q[0:1]
                    Q = Q[1:] + '0'
                    A = sub(A, M)

                c = '0' if A[0] == '1' else '1'
                Q = Q[0: len(Q) - 1] + c
            if i == 25:
                for _ in range(2):
                    if A[0] == '1':
                        A = A[1:] + Q[0:1]  # {A,Q} = {A,Q} << 1;
                        Q = Q[1:] + '0'
                        A = adder(A, M)
                    else:
                        A = A[1:] + Q[0:1]
                        Q = Q[1:] + '0'
                        A = sub(A, M)

                    c = '0' if A[0] == '1' else '1'
                    Q = Q[0: len(Q) - 1] + c

        self.Q = Q

    def normalize(self):
        Q = self.Q[::-1]
        index = len(self.a.mantis)
        if Q[index] == '0':
            # shift left
            Q = '0' + Q[0: len(Q) - 1]
            self.exponent -= 1
        self.mantis = Q[1: index]

    def get_result(self):
        print(self.mantis)
        result = str(self.sign_bit) + bin(self.exponent) + self.mantis
        result = result.replace('0b', '')
        # return binaryToFloat(result)
        return result


def adder(x, y):
    max_len = max(len(x), len(y))

    x = x.zfill(max_len)
    y = y.zfill(max_len)

    result = ''
    carry = 0

    for i in range(max_len-1, -1, -1):
        r = carry
        r += 1 if x[i] == '1' else 0
        r += 1 if y[i] == '1' else 0
        result = ('1' if r % 2 == 1 else '0') + result
        carry = 0 if r < 2 else 1

    if carry != 0:
        result = '1' + result

    if len(result) > max_len:
        result = result[1:]

    return result


def sub(a, b):
    not_b = ['0' if x == '1' else '1' for x in b]
    not_b = ''.join(not_b)
    _b = adder(not_b, '1')
    return adder(a, _b)[1:]


def getBin(x, is_positive=True):
    val = None
    if is_positive:
        bin_x = str(bin(x))[2:]
        zero_extend_len = 64 - len(bin_x)  # 0b1010 -> 1010
        val = '0'*zero_extend_len + bin_x
    else:
        bin_x = str(bin(x))[3:]
        zero_extend_len = 64 - len(bin_x)  # 0b1010 -> 1010
        val = "1" + bin_x
    return val


def floatToBinary64(value):
    val = struct.unpack('Q', struct.pack('d', value))[0]
    return getBin(val, is_positive=value > 0)


def floatToBinary32(value):
    double = floatToBinary64(value)
    single = double[0: 9] + double[MANTIS_INDEX: MANTIS_INDEX + 23]
    return single


def binaryToFloat(value):
    hx = hex(int(value, 2))
    return struct.unpack("d", struct.pack("q", int(hx, 16)))[0]


def generate_test():
    f64 = open("./input/input64.txt", "w")
    f32 = open("./input/input32.txt", "w")
    f10 = open("./input/input10.txt", "w")

    out64 = open("./output/output64.txt", "w")
    out10 = open("./output/output10.txt", "w")

    for _ in range(10):
        a = random.uniform(0, 10)
        b = random.uniform(0, 10)
        f10.write(str(a) + '\n' + str(b) + '\n')
        f32.write(floatToBinary32(a) + '\n' + floatToBinary32(b) + '\n')
        f64.write(floatToBinary64(a) + '\n' + floatToBinary64(b) + '\n')

        div = Div(a, b)
        result64 = div.divison()
        result10 = a / b
        out64.write(result64 + '\n')
        out10.write(str(result10) + '\n')

    f64.close()
    f32.close()
    f10.close()
    out64.close()
    out10.close()


# div = Div(3.3, 1.5)
# result = div.divison()
# print(result)

print(binaryToFloat('0100000000001010101010101010101010101010101010101010101010101010'))

# print(sub('100', '011'))

# print(bin(9))

# generate_test()
# 0100000000001010101010101010101010101010101010101010101010101010
# 0100000000000001100110011001100110011001100110011001100110011001
