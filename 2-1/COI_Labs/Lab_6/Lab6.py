import matplotlib
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

# Define font paths
arial_path = 'Arial.ttf'
broadway_path = 'Broadway.ttf'

# Check font file existence
assert os.path.exists(arial_path), f"Font file {arial_path} not found."
assert os.path.exists(broadway_path), f"Font file {broadway_path} not found."

# Constants
IMAGE_SIZE = (64, 64)
FONT_SIZE = 64
SYMBOLS_ACF = ['1']
SYMBOLS_CCF = ['0', '1', '2', '3', '4', '5', '6', '7']

def generate_symbol_image(symbol, font_path, font_name):
    try:
        font = ImageFont.truetype(font_path, FONT_SIZE)
    except IOError:
        print(f"Failed to load font from {font_path}")
        return None

    image = Image.new('L', IMAGE_SIZE, color=255)
    draw = ImageDraw.Draw(image)

    bbox = draw.textbbox((0, 0), symbol, font=font)
    width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    x_pos = (IMAGE_SIZE[0] - width) // 2
    y_pos = (IMAGE_SIZE[1] - height) // 2

    draw.text((x_pos, y_pos), symbol, font=font, fill=0)

    image_file = f"img/{symbol}_{font_name}_image.png"
    image.save(image_file)
    print(f"Image for symbol '{symbol}' saved as {image_file}")

    return np.array(image)

def compute_acf(image_data):
    result = np.correlate(image_data.flatten(), image_data.flatten(), mode='full')
    return result[result.size // 2:]

def compute_ccf(image_data1, image_data2):
    return np.correlate(image_data1.flatten(), image_data2.flatten(), mode='full')

# Generate images for symbols and compute autocorrelation
for symbol in SYMBOLS_ACF:
    arial_image = generate_symbol_image(symbol, arial_path, "Arial")
    broadway_image = generate_symbol_image(symbol, broadway_path, "Broadway")

    if arial_image is not None:
        plt.imshow(arial_image, cmap='gray')
        plt.title(f"Arial Symbol: {symbol}")
        plt.show()

    if broadway_image is not None:
        plt.imshow(broadway_image, cmap='gray')
        plt.title(f"Broadway Symbol: {symbol}")
        plt.show()

    # Calculate autocorrelations
    acf_arial = compute_acf(arial_image)
    acf_broadway = compute_acf(broadway_image)

    print(f"Autocorrelation for symbol '{symbol}' in Arial:", acf_arial)
    print(f"Autocorrelation for symbol '{symbol}' in Broadway:", acf_broadway)

    # Plot autocorrelation graphs
    plt.figure(figsize=(10, 4))
    plt.plot(acf_arial, label=f'Arial ACF for {symbol}')
    plt.plot(acf_broadway, label=f'Broadway ACF for {symbol}')
    plt.xlabel("Shift")
    plt.ylabel("Autocorrelation")
    plt.title(f"Autocorrelation Function for Symbol '{symbol}'")
    plt.legend()
    plt.grid()
    plt.show()

def calculate_correlation(img1, img2):
    arr1 = img1.flatten()
    arr2 = img2.flatten()
    correlation = np.corrcoef(arr1, arr2)[0, 1]
    return correlation

# Generate images for correlation matrix and compute correlation
arial_images = [generate_symbol_image(symbol, arial_path, "Arial") for symbol in SYMBOLS_CCF]

correlation_matrix = np.zeros((len(SYMBOLS_CCF), len(SYMBOLS_CCF)))

for i, img1 in enumerate(arial_images):
    for j, img2 in enumerate(arial_images):
        correlation_matrix[i, j] = calculate_correlation(img1, img2)

print("Correlation matrix for symbols (Arial):")
print(correlation_matrix)

# Plot correlation matrix
plt.figure(figsize=(8, 6))
plt.imshow(correlation_matrix, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.xticks(ticks=range(len(SYMBOLS_CCF)), labels=SYMBOLS_CCF)
plt.yticks(ticks=range(len(SYMBOLS_CCF)), labels=SYMBOLS_CCF)
plt.title("Correlation Matrix for Symbols in Arial")
plt.savefig("correlation_matrix.png", dpi=300)
plt.show()

# Plot correlation graph
plt.figure(figsize=(8, 6))
for i in range(correlation_matrix.shape[0]):
    plt.plot(SYMBOLS_CCF, correlation_matrix[i], label=f'Symbol {SYMBOLS_CCF[i]}')

plt.xlabel('Symbols')
plt.ylabel('Correlation')
plt.title('Correlation Graph for Symbols in Arial')
plt.legend(loc='upper right')
plt.savefig("correlation_graph.png", dpi=300)
plt.show()
