import numpy as np

# Генерация матрицы Уолша (ортогональные коды)
def walsh_matrix(n):
    if n == 1:
        return np.array([[1]])
    H = walsh_matrix(n // 2)
    top = np.hstack((H, H))
    bottom = np.hstack((H, -H))
    return np.vstack((top, bottom))

# Перевод строки в биты ASCII
def string_to_bits(s):
    return [int(b) for c in s for b in format(ord(c), '08b')]

# Перевод битов обратно в строку
def bits_to_string(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        chars.append(chr(int("".join(map(str, byte)), 2)))
    return "".join(chars)

# CDMA кодирование
def cdma_encode(bits, code):
    return np.array([bit*2-1 for bit in bits for _ in range(len(code))]) * np.tile(code, len(bits))

# CDMA декодирование
def cdma_decode(signal, code, msg_len):
    chunk_size = len(code)
    decoded_bits = []
    for i in range(0, len(signal), chunk_size):
        chunk = signal[i:i+chunk_size]
        val = np.dot(chunk, code)
        bit = 1 if val > 0 else 0
        decoded_bits.append(bit)
    return decoded_bits[:msg_len]

# --- Основная программа ---
messages = {
    "A": "GOD",
    "B": "CAT",
    "C": "HAM",
    "D": "SUN"
}

# Генерируем коды Уолша 8-битные
codes = walsh_matrix(8)

# Берём первые 4 строки (для 4 станций)
station_codes = {
    "A": codes[0],
    "B": codes[1],
    "C": codes[2],
    "D": codes[3]
}

# Кодируем все сообщения
encoded_signals = []
message_bits = {}
for station, word in messages.items():
    bits = string_to_bits(word)
    message_bits[station] = bits
    encoded = cdma_encode(bits, station_codes[station])
    encoded_signals.append(encoded)

# Суммарный сигнал в канале
channel = sum(encoded_signals)

# Декодируем обратно
for station, code in station_codes.items():
    decoded_bits = cdma_decode(channel, code, len(message_bits[station]))
    decoded_word = bits_to_string(decoded_bits)
    print(f"Станция {station} передала: {decoded_word}")
