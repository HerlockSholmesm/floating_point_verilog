import struct
import random

# SIGN_INDEX = 31
# MANTIS_INDEX = 22
# BIAS = 127
SIGN_INDEX = 0
MANTIS_INDEX = 12
BIAS = 1023
MAX_EXPONENT = 10000
MIN_EXPONENT = -10000


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

    def divison(self):
        self.sign_bit = self.a.sign ^ self.b.sign
        self.exponent = self.a.exponent - self.b.exponent + BIAS
        self.calc_mantis()
        self.normalize()
        self.check_overflow()
        self.check_underflow()
        return self.get_result()

    def check_overflow(self):
        if self.exponent > MAX_EXPONENT:
            print('overflow')
            exit(4)

    def check_underflow(self):
        if self.exponent < MIN_EXPONENT:
            print('underflow')
            exit(4)

    def calc_mantis(self):
        count = 26
        Q = self.a.mantis
        M = self.b.mantis
        A = '0' * len(self.a.mantis)
        MSB = 51
        for _ in range(count):
            if A[0] == '1':
                A = A[1:] + Q[0:1]
                Q = Q[1:] + '0'
                A = adder(A, M)
            else:
                A = A[1:] + Q[0:1]
                Q = Q[1:] + '0'
                A = sub(A, M)

            Q = Q[0: len(Q) - 1] + '0' if A[0] == '1' else '1'

            if A[0] == '1':
                A = A[1:] + Q[0:1]
                Q = Q[1:] + '0'
                A = adder(A, M)
            else:
                A = A[1:] + Q[0:1]
                Q = Q[1:] + '0'
                A = sub(A, M)

            Q = Q[0: len(Q) - 1] + '0' if A[0] == '1' else '1'

        self.mantis = Q

    def normalize(self):
        pass

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

    return result.zfill(max_len)


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


# print(int('11100000000000000000000000000000000000000000000000000', 2))
# print(int('11000000000000000000000000000000000000000000000000000', 2))
# a = IEEE(3.5)
# b = IEEE(1.5)
# div = Div(3.5, 1.5)
# result = div.divison()
# print(result)

print(bin(9))

# generate_test()
