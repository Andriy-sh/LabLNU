import heapq
from collections import defaultdict


# Функція для кодування методом RLE
def rle_encode(data):
    encoding = ""
    i = 0
    while i < len(data):
        count = 1
        while i + 1 < len(data) and data[i] == data[i + 1]:
            count += 1
            i += 1
        encoding += data[i] + str(count)
        i += 1
    return encoding


# Функція для декодування методом RLE
def rle_decode(data):
    decoding = ""
    i = 0
    while i < len(data):
        char = data[i]
        count = ""
        i += 1
        while i < len(data) and data[i].isdigit():
            count += data[i]
            i += 1
        decoding += char * int(count)
    return decoding


# Функція для кодування методом LZ77
def lz77_encode(data, window_size=20):
    encoded_data = []
    i = 0
    while i < len(data):
        match = (-1, 0)  # (distance, length)
        for j in range(max(0, i - window_size), i):
            length = 0
            while length < len(data) - i and data[j + length] == data[i + length]:
                length += 1
            if length > match[1]:
                match = (i - j, length)
        if match[1] > 0:
            encoded_data.append((match[0], match[1], data[i + match[1]]))
            i += match[1] + 1
        else:
            encoded_data.append((0, 0, data[i]))
            i += 1
    return encoded_data


# Функція для декодування методом LZ77
def lz77_decode(encoded_data):
    decoded_data = ""
    for (distance, length, char) in encoded_data:
        if distance > 0:
            start = len(decoded_data) - distance
            decoded_data += decoded_data[start:start + length]
        decoded_data += char
    return decoded_data


# Клас для вузла дерева Хаффмана
class HuffmanNode:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


# Побудова дерева Хаффмана
def build_huffman_tree(data):
    freq = defaultdict(int)
    for char in data:
        freq[char] += 1
    heap = [HuffmanNode(char, freq) for char, freq in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    return heap[0]


# Створення таблиці кодування для Хаффмана
def build_huffman_code_table(node, binary_str="", code_table=None):
    if code_table is None:
        code_table = {}
    if node.char is not None:
        code_table[node.char] = binary_str
    else:
        build_huffman_code_table(node.left, binary_str + "0", code_table)
        build_huffman_code_table(node.right, binary_str + "1", code_table)
    return code_table


# Кодування методом Хаффмана
def huffman_encode(data):
    tree = build_huffman_tree(data)
    code_table = build_huffman_code_table(tree)
    encoded_data = "".join(code_table[char] for char in data)
    return encoded_data, code_table


# Декодування методом Хаффмана
def huffman_decode(encoded_data, code_table):
    reversed_code_table = {v: k for k, v in code_table.items()}
    decoded_data = ""
    buffer = ""
    for bit in encoded_data:
        buffer += bit
        if buffer in reversed_code_table:
            decoded_data += reversed_code_table[buffer]
            buffer = ""
    return decoded_data


# Обчислення коефіцієнта стиснення
def calculate_compression_ratio(original_data, compressed_data_size):
    original_size = len(original_data) * 8  # в бітах
    return original_size / compressed_data_size if compressed_data_size > 0 else 1


# Основна функція для тестування стиснення та збереження результатів у файли
def main():
    try:
        with open('l7coi.txt', 'r', encoding='utf-8') as file:
            data = file.read()
    except FileNotFoundError:
        print("File 'l7coi.txt' not found.")
        return

    # RLE
    rle_encoded = rle_encode(data)
    with open('rle_compressed.txt', 'w', encoding='utf-8') as file:
        file.write(rle_encoded)
    rle_decoded = rle_decode(rle_encoded)
    with open('rle_decoded.txt', 'w', encoding='utf-8') as file:
        file.write(rle_decoded)
    rle_ratio = calculate_compression_ratio(data, len(rle_encoded) * 8)

    # LZ77
    lz77_encoded = lz77_encode(data)
    with open('lz77_compressed.txt', 'w', encoding='utf-8') as file:
        file.write(str(lz77_encoded))
    lz77_decoded = lz77_decode(lz77_encoded)
    with open('lz77_decoded.txt', 'w', encoding='utf-8') as file:
        file.write(lz77_decoded)
    lz77_encoded_size = sum(len(str(item)) * 8 for item in lz77_encoded)
    lz77_ratio = calculate_compression_ratio(data, lz77_encoded_size)

    # Huffman
    huffman_encoded, code_table = huffman_encode(data)
    with open('huffman_compressed.bin', 'w', encoding='utf-8') as file:
        file.write(huffman_encoded)
    huffman_decoded = huffman_decode(huffman_encoded, code_table)
    with open('huffman_decoded.txt', 'w', encoding='utf-8') as file:
        file.write(huffman_decoded)
    huffman_ratio = calculate_compression_ratio(data, len(huffman_encoded))

    # Виведення коефіцієнтів стиснення
    print(f"RLE Compression Ratio: {rle_ratio:.2f}")
    print(f"LZ77 Compression Ratio: {lz77_ratio:.2f}")
    print(f"Huffman Compression Ratio: {huffman_ratio:.2f}")


if __name__ == "__main__":
    main()