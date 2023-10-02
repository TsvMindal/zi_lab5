import matplotlib.pyplot as plt
import numpy as np

def generate_lfsr_sequence(length, seed, taps):
    sequence = []
    for _ in range(length):
        sequence.append(seed[0])
        shift_lfsr(seed, taps)
    return sequence

def shift_lfsr(seed, taps):
    feedback = [0]  # Исправлено: feedback должен быть списком
    for t in taps:
        feedback[0] ^= seed[t]

    seed[1:] = seed[:-1]
    seed[0] = feedback[0]  # Исправлено: seed[0] и feedback[0]

def convert_bits_to_bytes(bits):
    byte_list = [0] * 8
    for i in range(8):
        for j in range(8):
            byte_list[i] |= bits[i * 8 + j] << j
    return byte_list

def calculate_chi_square(key):
    observed = [key.count(0), key.count(1)]
    chi_square = 0
    for i in range(2):
        expected = len(key) / 2
        chi_square += ((observed[i] - expected) ** 2) / expected
    return chi_square

def plot_sequence(sequence, filename):
    plt.plot(range(len(sequence)), sequence, '-o', color='purple')
    plt.xlabel('Bit number')
    plt.ylabel('Bit value')
    plt.ylim([-0.5, 1.5])
    plt.savefig(filename, format='png')  # Сохранение графика в формате PNG
    plt.close()  # Закрытие текущего графика
    print("Последовательность для построения графика:", sequence)

def encrypt_image_with_lfsr(image_path, seed, taps):
    byte_list = np.fromfile(image_path, dtype=np.uint8)
    count_blocks = int((len(byte_list) - 110) / 8)
    encrypted_image = byte_list.copy()

    for i in range(count_blocks):
        block_arr = encrypted_image[110 + i * 8: 110 + (i + 1) * 8]
        key = convert_bits_to_bytes(generate_lfsr_sequence(8 * 8, seed, taps))
        encrypted_block = np.bitwise_xor(block_arr, key)

        encrypted_image[110 + i * 8: 110 + (i + 1) * 8] = encrypted_block

    with open('modified_tux.bmp', 'wb') as file:
        file.write(encrypted_image.tobytes())

# Пользовательский ввод seed и taps
seed = [int(bit) for bit in input("Введите seed: ")]
taps = [int(tap) for tap in input("Введите taps: ")]
print("Построение графика...")
lfsr_sequence = generate_lfsr_sequence(2 ** max(taps) - 1, seed, taps)
chi_square_value = calculate_chi_square(lfsr_sequence)
print("χ2 = ", chi_square_value)
plot_sequence(lfsr_sequence, 'lfsr_plot.png')
print("Построенный график сохранен в файле 'lfsr_plot.png'")

# Вызов функции для шифрования изображения
encrypt_image_with_lfsr("tux.bmp", seed, taps)
