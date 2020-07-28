import struct

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
        mantis = '1' + number[MANTIS_INDEX:]
        self.mantis = int(mantis, 2)
        self.exponent = int(number[1: MANTIS_INDEX], 2) - BIAS

    def __str__(self):
        return 'm: {}, exp: {}, sign: {}'.format(self.mantis, self.exponent, self.sign)

    def __repr__(self):
        return 'm: {}, exp: {}, sign: {}'.format(self.mantis, self.exponent, self.sign)

    def get_decimal(self):
        pass


class Div:  # a / b
    def __init__(self, a, b):
        self.a = a
        self.b = b
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
        result = float_bin(self.a.mantis / self.b.mantis, 52)
        self.mantis = result[2:]
        # print('{}, {}, {}'.format(self.mantis, self.a.mantis, self.b.mantis))

    def normalize(self):
        pass

    def get_result(self):
        print(self.mantis)
        result = str(self.sign_bit) + bin(self.exponent) + self.mantis
        result = result.replace('0b', '')
        return binaryToFloat(result)


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


def binaryToFloat(value):
    hx = hex(int(value, 2))
    return struct.unpack("d", struct.pack("q", int(hx, 16)))[0]


def float_bin(number, places=3):    # 1.75 -> 1.11
    whole, dec = str(number).split(".")
    whole = int(whole)
    dec = int(dec)

    res = bin(whole).lstrip("0b") + "."
    for _ in range(places):
        whole, dec = str((decimal_converter(dec)) * 2).split(".")
        dec = int(dec)
        res += whole

    return res


def decimal_converter(num):
    while num > 1:
        num /= 10
    return num


# print(int('11100000000000000000000000000000000000000000000000000', 2))
# print(int('11000000000000000000000000000000000000000000000000000', 2))
a = IEEE(3.5)
b = IEEE(1.5)
div = Div(a, b)
result = div.divison()
print(result)

# print(float_bin(1.1666666666666667, 52))
