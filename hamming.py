import random

data = 'HEART'
bin_data = ''.join([bin(ord(c))[2:] for c in data]) # list of 7 bits data
print(f'data: {data} -> {bin_data}')

''' Hamming(7, 4) | Even Parity Bit Type | Implementation by Heart '''

''' Split data to chunk of 4 bits '''
data_chunks = [f'{bin_data[i:i+4]:04}' for i in range(0, len(bin_data), 4)]

i_am_receiver = [] # pretend to be RECEIVER!

for chunk in data_chunks:
    data_to_send = ['' for _ in range(7)]
    
    ''' add parity bit '''
    for i in range(3):
        data_to_send[2**i-1] = f'p{i+1}'

    ''' add data bit '''
    cnt = 0
    for i in range(7):
        if data_to_send[i] == '':
            data_to_send[i] = chunk[cnt]
            cnt += 1

    ''' change parity bit value '''
    for i in range(3):
        number_of_1 = 0

        for pos in range(7):
            if (pos != 2**i-1) and (pos+1 & 2**i != 0):
                if data_to_send[pos] == '1':
                    number_of_1 += 1

        data_to_send[2**i-1] = '0' if number_of_1%2==0 else '1'

    print(f'{chunk} -> {''.join(data_to_send)} (add parity)')

    ''' Simulate Noise (Flip 1 Bit) '''
    idx = random.randint(0, 6)
    data_to_send[idx] = '1' if data_to_send[idx]=='0' else '0'

    ''' Send data to Receiver '''
    data_to_send = ''.join(data_to_send)
    i_am_receiver.append(data_to_send)


def custom_decode(encodes):
    decodes = []
    for enc in encodes:
        enc = [bit for bit in enc]
        for i in range(3):
            enc[2**i-1] = '' # remove parity bit
        decodes.append(''.join(enc))
    
    decoded_str = ''.join(decodes)
    return ''.join( [chr(int(decoded_str[i:i+7], 2)) for i in range(0, len(decoded_str), 7)] )

def error_correction(encodes):
    corrects = []
    for enc in encodes:
        enc = [bit for bit in enc]
        index_of_error = []
        for i in range(3):
            number_of_1 = 0
            for pos in range(7):
                if 2**i & pos+1 != 0 and enc[pos]=='1':
                    number_of_1 += 1
            if number_of_1 % 2 == 1:
                index_of_error.append('1')
            else:
                index_of_error.append('0')

        ''' fix error bit '''
        index_of_error = int(''.join(index_of_error)[::-1], 2) - 1 # convert to 0 based index
        if index_of_error != -1:
            enc[index_of_error] = '1' if enc[index_of_error]=='0' else '0'

        corrects.append(''.join(enc))

    return corrects

                    

# print('\n[RECEIVER]: I receive this data >', ' '.join(i_am_receiver))
print('\n[RECEIVER]: I receive this data >', ' '.join(i_am_receiver)[:31])
print('                                ', ' '.join(i_am_receiver)[31:])
print('[Before Error Correction]:', custom_decode(i_am_receiver))

''' Error Correction '''
i_am_receiver = error_correction(i_am_receiver)

print('[After Error Correction]:', custom_decode(i_am_receiver))