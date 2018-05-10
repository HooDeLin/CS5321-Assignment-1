import sys
from oracle_python_v1_2 import pad_oracle, dec_oracle

def xor_strings(xs, ys):
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))

c_0 = sys.argv[1][2:].decode("hex")
c_1 = sys.argv[2][2:].decode("hex")

results = []
num_of_padding = 0
existing_padding = "00" * 8

# Find the num of existing padding
for i in range(8):
    mod = ("00" * i + "01" + "00" * (7-i)).decode("hex")
    c_0_mod = xor_strings(c_0, mod)
    ret_pad = pad_oracle("0x" + c_0_mod.encode("hex"), sys.argv[2])
    if ret_pad == "0":
        num_of_padding = 8 - i
        existing_padding = mod
        break

for i in range(num_of_padding, 8):
    pad = ("00" * (7 - i) +("0" + str(i + 1)) * (i + 1)).decode("hex")
    prev = ''.join(results)
    for j in range(256):
        current_guess = "0" * (14 - (num_of_padding * 2) - len(prev) + 1 - (len(hex(j)[2:])/ 2)) + hex(j)[2:] + prev + ("0" + str(num_of_padding)) * num_of_padding
        c_0_mod = xor_strings(c_0, current_guess.decode("hex"))
        c_0_mod = xor_strings(c_0_mod, pad)
        ret_pad = pad_oracle("0x" + c_0_mod.encode("hex"), sys.argv[2])
        if ret_pad == "1":
            results.insert(0, "0" * (1 - (len(hex(j)[2:])/ 2)) + hex(j)[2:])
            break

print(''.join(results).decode("hex"))