
# Image and GIF Converter

This Python application allows you to convert image and GIF files into various formats optimized for use with embedded systems. The program supports different color formats and block sizes, offering flexibility to meet the needs of microcontroller or FPGA-based systems.

## Features

- Convert images and GIFs into the following color formats:
  - Color RS5G6B5
  - Color A8R8G8B8
  - Color R5G5B5
  - Color R8G8B8
  - Grayscale 8-bit
  - Monochrome
- Ability to select image or GIF files and apply various conversion options.
- Supports block sizes of 8, 16, 24, and 32 bits.
- Automatically saves the converted data in a `.h` file compatible with embedded systems.

## Requirements

- Python 3.x
- PyQt5
- Pillow (PIL Fork)
- Numpy

## Installation

### 1. Clone the Repository

Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/dennarthecreator/image-gif-converter.git
cd image-gif-converter
```

### 2. Install Dependencies

Create a virtual environment (optional but recommended) and install the required dependencies:

#### Create and Activate Virtual Environment (Optional)

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# For Windows:
venv\Scripts\activate
# For macOS/Linux:
source venv/bin/activate
```

#### Install Dependencies

```bash
# Install the required dependencies
pip install -r requirements.txt
```

Alternatively, you can install the dependencies directly without a virtual environment using:

```bash
pip install PyQt5 Pillow numpy
```

### 3. Running the Application

Once you have installed the dependencies, you can run the application:

```bash
python converter.py
```

This will launch the graphical interface where you can select your image or GIF, choose the preset color format, block size, and then convert the file. The resulting data will be saved as a `.h` header file.

## Usage

1. **Select an Image or GIF File**: Click the "Select Image or GIF" button to browse and choose your file.
2. **Choose a Format**: Select the color format you want the image to be converted to from the preset dropdown.
3. **Choose Block Size**: Select the block size from the dropdown (8, 16, 24, or 32).
4. **Convert the Image**: Press the "Convert" button to process the image or GIF file and save the converted data in the appropriate format.

### Output File

The program saves the converted data as a `.h` file with the selected name and format. The file will be saved in the same directory as the original image or GIF file.

## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- **PyQt5**: For the graphical user interface.
- **Pillow (PIL Fork)**: For handling image and GIF processing.
- **Numpy**: For manipulating image data arrays.

## Contact

If you have any questions or feedback, feel free to open an issue on the GitHub repository or reach out to me directly.
