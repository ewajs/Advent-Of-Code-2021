## General
# Read and format the data in a convenient way
with open('input_data.txt', 'r') as f:
    lines = [line for line in f.readlines()]
    outputs = [output for line in lines for output in line.split("|")[1].strip().split(' ')]
    signals_and_outputs = [
                            {'signals': signals.strip().split(' '), 'outputs': outputs.strip().split(' ')} 
                            for signals, outputs in [line.split("|") for line in lines]
                        ]

# Constants
ONE = ["c", "f"]
FOUR = ["b", "c", "d", "f"]
SEVEN = ["a", "c", "f"]
EIGHT = ["a", "b", "c", "d", "e", "f", "g"]

DIGITS_OF_INTEREST = [ONE, FOUR, SEVEN, EIGHT]

## Part 1

def same_length(value, digit):
    # Since we know letters arent repeated we can use set comparison
    # which will take care of ignoring order
    return len(value) == len(digit)


amount = sum(1 for output in outputs if any(same_length(output, digit) for digit in DIGITS_OF_INTEREST))

print(f"Digits 1, 4, 7, or 8 appear {amount} times.")

## Part 2

def infer_value(signals, outputs):
    # First assign the obvious ones
    digits = {
        1: set([signal for signal in signals if len(signal) == 2][0]),
        4: set([signal for signal in signals if len(signal) == 4][0]),
        7: set([signal for signal in signals if len(signal) == 3][0]),
        8: set([signal for signal in signals if len(signal) == 7][0]),
        }
    # 3 is the only one that's 5 segments and contains all segments in 1
    digits[3] = set([signal for signal in signals if len(signal) == 5 and digits[1].issubset(set(signal))][0])
    
    # 9 is the only one that's 6 segments and contains all segments in 3
    digits[9] = set([signal for signal in signals if len(signal) == 6 and digits[3].issubset(set(signal))][0])
    # The bottom left segment is the one that is lit in 8 but not 9
    bottom_left_segment = digits[8] - digits[9]
    # 2 is the only one that's 5 segments and has the bottom left segment lit
    digits[2] = set([signal for signal in signals if len(signal) == 5 and bottom_left_segment.issubset(set(signal))][0])
    # 5 we get by elimination
    digits[5] = set([signal for signal in signals if len(signal) == 5 and set(signal) not in [digits[2], digits[3]]][0])
    # 6 is 5 plus the bottom left segment
    digits[6] = digits[5] | bottom_left_segment
    # 0 is the remainder
    digits[0] = set([signal for signal in signals if set(signal) not in digits.values()][0])
    
    # Now the values is our digits dictionary permutting keys for values
    # We'll need to use a frozenset instead of set because sets are not hashable
    values = {frozenset(v): k for k, v in digits.items()}
    return sum(values[frozenset(output)] * 10 ** (3 - i) for i, output in enumerate(outputs))


sum_of_decoded_outputs = sum(infer_value(line['signals'], line['outputs']) for line in signals_and_outputs)

print(sum_of_decoded_outputs)


#print(sum_of_decoded_outputs)