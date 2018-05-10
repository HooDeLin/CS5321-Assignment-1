import sys
from oracle_python_v1_2 import pad_oracle, dec_oracle

def xor_strings(xs, ys):
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))

def add_padding(p):
    if len(p) != 8:
        original = p.encode("hex")
        return original + ("0" + str(8 - len(p))) * (8-len(p))
    else:
        return p.encode("hex")

plaintext = [sys.argv[1][i:i+8] for i in range(0, len(sys.argv[1]), 8)]
plaintext_padded = list(map(add_padding, plaintext))

if len(plaintext) == 0 or len(plaintext[-1]) == 8:
    plaintext_padded.append("08" * 8)

results = ["0x1234567890abcdef"]
for current_plaintext in reversed(plaintext_padded):
    prev = "0x" + "00" * 8
    ret_dec = dec_oracle(prev, results[0])
    new_prev = "0x" + xor_strings(ret_dec[2:].decode("hex"), current_plaintext.decode("hex")).encode("hex")
    results.insert(0, new_prev)

print(" ".join(results))

# Debug
# for i in range(len(results) - 1):
#     ret_dec = dec_oracle(results[i], results[i + 1])[2:].decode("hex")
#     print(ret_dec)