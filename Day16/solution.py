
import math
## General
# Read and format the data in a convenient way
with open('input_data.txt', 'r') as f:
    # We'll use a dictionary of points to track our grid (and we'll call it a graph)
    hex_stream = f.read()

## Part 1

class BITSDecoder:
    """This class will handle our decoding logic"""

    def __init__(self, hex_stream):
        # Convert to binary, discard the 0b at the start
        self.stream = bin(self.hex_to_int(hex_stream))[2:]
        # Pad the start so that we don't lose 0s
        remainder = len(self.stream) % 4
        self.stream  = ((4 - remainder) if remainder > 0 else 0) * '0' + self.stream
        self.stream_pointer = 0
        self.version_accumulator = 0
        # This will help us compute each packet value on the fly based on its children's values
        self.type_map = {
            0: sum,
            1: math.prod,
            2: min,
            3: max,
            5: lambda values: 1 if values[0] > values[1] else 0,
            6: lambda values: 1 if values[0] < values[1] else 0,
            7: lambda values: 1 if values[0] == values[1] else 0
        }

    def parse_packet(self, parent = None):
        current_packet = {}
        self.read_header(current_packet)
        self.version_accumulator += current_packet['version']
        if current_packet['type_id'] == 4:
            current_packet['value'] = self.read_literal()
        else:
            # This is an operator
            current_packet['length_type_id'] = self.read_part(1)
            # We'll save sub packets in the packet itself
            current_packet['sub_packets'] = []
            if current_packet['length_type_id'] == '0':
                current_packet['payload_bit_length'] = self.bin_to_int(self.read_part(15))
                current_packet['payload_start_bit'] = self.stream_pointer
                while self.stream_pointer < current_packet['payload_start_bit'] + current_packet['payload_bit_length']:
                    self.parse_packet(current_packet)
            else:
                current_packet['number_of_sub_packets'] = self.bin_to_int(self.read_part(11))
                while len(current_packet['sub_packets']) < current_packet['number_of_sub_packets']:
                    self.parse_packet(current_packet)
            # After this line all sub packets have been evaluated so we can compute the value of the operator
            # As these calls are all recursive, we can ensure we have no packets to parse down the hierarchy for
            # this operator
            current_packet['value'] = self.type_map[current_packet['type_id']]([sub_packet['value'] for sub_packet in current_packet['sub_packets']])
            
        
        if parent is None:
            # Lastly, we may need to move our pointer to align with next packet if this is not a sub packet
            self.align_pointer()
            # This is a root level packet, we append to our packet list
            return current_packet
        else:
            parent['sub_packets'].append(current_packet)
        
        current_packet['packet_length'] = self.stream_pointer - current_packet['stream_index'] - 1
       

    def read_header(self, packet):
        packet['stream_index'] = self.stream_pointer
        packet['version'] = self.bin_to_int(self.read_part(3))
        packet['type_id'] = self.bin_to_int(self.read_part(3))
    
    def read_literal(self):
        # This is a literal value, start a bit value accumulator
        bit_value = ''
        # We start reading in groups of 5
        read_last_part = False
        while not read_last_part:
            literal = self.read_part(5)
            # First bit indicates whether we should keep reading or not
            read_last_part = literal[0] == '0'
            # Last 4 is a value we accumulate until reaching the end
            bit_value += literal[1:] 
        return self.bin_to_int(bit_value)
        
       
    def hex_to_int(self, data):
        return int(data, 16)

    def bin_to_int(self, data):
        return int(data, 2)
    
    def read_part(self, length):
        raw_part = self.stream[self.stream_pointer:self.stream_pointer + length]
        self.stream_pointer += length
        return raw_part
    
    def align_pointer(self):
        # To align me move to the next multiple of 4
        remainder = (self.stream_pointer) % 4
        self.stream_pointer = self.stream_pointer + (4 - remainder) if remainder > 0 else self.stream_pointer

    def get_current_bit(self):
        return self.stream[self.stream_pointer]


decoder = BITSDecoder(hex_stream)
packet = decoder.parse_packet()
print(f"The accumulated versions are {decoder.version_accumulator}")
## Part 2
print(f"The packet value is {packet['value']}")


