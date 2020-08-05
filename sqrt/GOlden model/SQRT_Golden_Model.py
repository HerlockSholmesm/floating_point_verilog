import math
import struct

SIGN_INDEX = 0
MANTIS_INDEX = 9
MANTIS_SIZE = 23
BIAS = 127
# for double precision you should use CONSTANTS below
# SIGN_INDEX = 0
# MANTIS_INDEX = 12
# MANTIS_SIZE = 52
# BIAS = 1023
MAX_EXPONENT = 10000
MIN_EXPONENT = -10000


class IEEE:
    def __init__(self, number):
        self.sign = int(number[SIGN_INDEX])
        mantis = '1' + number[MANTIS_INDEX:]
        last_index = mantis.rfind('1')
        self.binary_mantis = int(mantis[:last_index + 1], 2)
        self.mantis = int(mantis, 2)
        self.exponent = int(number[1: MANTIS_INDEX], 2) - BIAS

    def __str__(self):
        return 'm: {}, exp: {}, sign: {}'.format(self.mantis, self.exponent, self.sign)

    def __repr__(self):
        return 'm: {}, exp: {}, sign: {}'.format(self.mantis, self.exponent, self.sign)

    def get_decimal(self):
        pass


def integer_square(d):  # non restoring algorithm
    r = 0
    q = 0

    result_bits = (int(math.log2(d)) + 1) // 2 + 1

    for i in range(result_bits - 1, -1, -1):

        if r >= 0:
            r = (r << 2) | ((d >> (i + i)) & 3)
            r = r - ((q << 2) | 1)
        else:
            r = (r << 2) | ((d >> (i + 1)) & 3)
            r = r + ((q << 2) | 3)

        if r >= 0:
            q = ((q << 1) | 1)
        else:
            q = ((q << 1) | 0)

        if r < 0:
            r = r + ((q << 1) | 1)
    length = int(math.log2(q))
    zero_extend = MANTIS_SIZE - length
    result = str(bin(q))[3:] + '0' * zero_extend
    return result


def get_binary(x, is_positive=True):
    val = None
    if is_positive:
        bin_x = str(bin(x))[2:]
        zero_extend_len = 64 - len(bin_x)  # 0b1010 -> 1010
        val = '0' * zero_extend_len + bin_x
    else:
        bin_x = str(bin(x))[3:]
        zero_extend_len = 64 - len(bin_x)  # 0b1010 -> 1010
        val = "1" + bin_x
    return val


def float_to_binary64(value):
    val = struct.unpack('Q', struct.pack('d', value))[0]
    return get_binary(val, is_positive=value > 0)


def binary_to_float(value):
    hx = hex(int(value, 2))
    return struct.unpack("d", struct.pack("q", int(hx, 16)))[0]

# for double precision you should use dp_sim_out.txt instead of sp_sim_out.txt below
file_r = open("sp_sim_out.txt", "r")
# for double precision you should use SQRT_text_file_DP.txt instead of SQRT_text_file_SP.txt below
file_w = open("SQRT_text_file_SP.txt", "w")
row = file_r.read().split("\n")
for i in range(2, len(row)):
    hex_index = int(row[i].rfind(','))
    # for double precision you should use 16 instead of 8 below
    binar = bin(int(row[i][hex_index - 16: hex_index], 16))[2:]
    # for double precision you should use 64 instead of 32 below
    z_extend = 64 - len(binar)
    binar = '0' * z_extend + binar
    sqrt_num = IEEE(binar)
    if sqrt_num.sign == 1:
        response = "NAN"
    else:
        sqrt_num.exponent = sqrt_num.exponent >> 1
        zero_extend = MANTIS_INDEX - 1 - len(str(bin(sqrt_num.exponent + BIAS))[2:])
        if sqrt_num.mantis != int(math.pow(2, MANTIS_SIZE)):
            fraction = integer_square(sqrt_num.binary_mantis)
            sqrt_str = str(sqrt_num.sign) + '0' * zero_extend + str(bin(sqrt_num.exponent + BIAS))[2:] + fraction
        else:
            sqrt_str = str(sqrt_num.sign) + '0' * zero_extend + str(bin(sqrt_num.exponent + BIAS))[
                                                                2:] + '0' * MANTIS_SIZE
        response = sqrt_str
        response = hex(int(response, 2))[2:]
    file_w.write(row[i] + " Golden_Model_Output: " + response + "\n")
