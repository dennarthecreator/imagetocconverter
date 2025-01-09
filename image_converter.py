import sys
import os
import numpy as np
from PIL import Image, ImageSequence
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QFileDialog, QLabel,
    QComboBox, QMessageBox, QInputDialog
)
from PyQt5.QtCore import Qt

class ImageConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.selected_file = ""

    def initUI(self):
        layout = QVBoxLayout()

        # Centralized file label
        self.file_label = QLabel("No file selected")
        self.file_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.file_label)

        # Select file button
        self.select_button = QPushButton("Select Image or GIF")
        self.select_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_button)

        # Preset selection ComboBox
        self.preset_combo = QComboBox()
        self.preset_combo.addItems([
            "Color RS5G6B5",
            "Color A8R8G8B8",
            "Color R5G5B5",
            "Color R8G8B8",
            "Grayscale 8",
            "Monochrome"
        ])
        layout.addWidget(self.preset_combo)

        # Block size ComboBox
        self.block_size_combo = QComboBox()
        self.block_size_combo.addItems(["8", "16", "24", "32"])
        layout.addWidget(self.block_size_combo)

        # Convert button
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_image)
        layout.addWidget(self.convert_button)

        # Set layout and window properties
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
        self.setWindowTitle("Image and GIF Converter")

        # Set minimum window size
        self.setMinimumSize(400, 400)  # Minimum window size
        self.resize(400, 400)  # Start with the minimum size

        # Allow window to expand to the full screen width and height when maximized
        self.setWindowFlag(Qt.FramelessWindowHint, False)

        self.show()

    def select_file(self):
        self.selected_file, _ = QFileDialog.getOpenFileName(self, "Select Image or GIF")
        if self.selected_file:
            self.file_label.setText(os.path.basename(self.selected_file))

    def convert_image(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Warning", "No file selected!")
            return

        preset = self.preset_combo.currentText()
        block_size = int(self.block_size_combo.currentText())

        try:
            if self.selected_file.lower().endswith('.gif'):
                self.convert_gif(preset, block_size)
            else:
                img = Image.open(self.selected_file)
                img = img.convert("RGBA")  # Ensure image is in RGBA format
                self.convert_image_data(img, preset, block_size)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def convert_gif(self, preset, block_size):
        # Open the GIF and extract frames
        gif = Image.open(self.selected_file)
        frames = []
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("RGBA")  # Ensure each frame is in RGBA format
            frames.append(np.array(frame))

        self.convert_gif_data(frames, preset, block_size)

    def convert_gif_data(self, frames, preset, block_size):
        # Assume that all frames have the same width and height
        height, width, _ = frames[0].shape

        gif_data = []
        for frame in frames:
            data = frame
            if preset == "Color RS5G6B5":
                data = ((data[..., 0] >> 3) << 11) | ((data[..., 1] >> 2) << 5) | (data[..., 2] >> 3)
                data = data.flatten()
            elif preset == "Color A8R8G8B8":
                data = ((data[..., 3] << 24) | (data[..., 0] << 16) | (data[..., 1] << 8) | data[..., 2]).flatten()
            elif preset == "Color R5G5B5":
                data = ((data[..., 0] >> 3) << 10) | ((data[..., 1] >> 3) << 5) | (data[..., 2] >> 3)
                data = data.flatten()
            elif preset == "Color R8G8B8":
                data = (data[..., 0] << 16) | (data[..., 1] << 8) | data[..., 2]
                data = data.flatten()
            elif preset == "Grayscale 8":
                grayscale = (0.2989 * data[..., 0] + 0.5870 * data[..., 1] + 0.1140 * data[..., 2]).astype(np.uint8)
                data = grayscale.flatten()
            elif preset == "Monochrome":
                monochrome = (0.2989 * data[..., 0] + 0.5870 * data[..., 1] + 0.1140 * data[..., 2]) > 128
                data = (monochrome.astype(np.uint8) * 255).flatten()

            gif_data.append(data)

        self.write_gif_output(gif_data, width, height, preset, block_size)

    def write_gif_output(self, gif_data, width, height, format_name, block_size):
        # Replace spaces with underscores in variable names
        output_name = os.path.splitext(os.path.basename(self.selected_file))[0].replace(" ", "_")
        format_name_clean = format_name.replace(" ", "_")
        output_filename = f"{output_name}_{format_name_clean}_Gif.h"

        # Calculate the number of pixels per frame (width * height)
        frame_size = width * height

        # Check if the file exists and ask for overwrite or new filename
        if os.path.exists(output_filename):
            reply, ok = QInputDialog.getText(
                self, "File Exists",
                f"The file '{output_filename}' already exists. Enter a new filename or press OK to overwrite:",
                text=output_filename
            )
            if ok and reply.strip():
                output_filename = reply.strip()

        # Write the output file with gif frames
        try:
            with open(output_filename, "w") as f:
                f.write(f"// {output_name}, {width}x{height}\n")
                f.write(f"const unsigned short PROGMEM {output_name}_{format_name_clean}_Gif[][{len(gif_data)}][{frame_size}] = {{\n")

                for i, frame_data in enumerate(gif_data):
                    f.write("{\n")
                    total_values = len(frame_data)
                    for j in range(total_values):
                        if j > 0 and j % width == 0:
                            f.write("\n")

                        f.write(f"0x{frame_data[j]:0{block_size // 4}X}" + (", " if j < total_values - 1 else ""))

                    f.write("\n}")
                    if i < len(gif_data) - 1:
                        f.write(",\n")

                f.write("\n};\n")

            QMessageBox.information(self, "Success", f"GIF converted to {format_name} format and saved as '{output_filename}'!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to write file: {str(e)}")

    def convert_image_data(self, img, preset, block_size):
        width, height = img.size
        data = np.array(img)

        if preset == "Color RS5G6B5":
            data = ((data[..., 0] >> 3) << 11) | ((data[..., 1] >> 2) << 5) | (data[..., 2] >> 3)
            data = data.flatten()
        elif preset == "Color A8R8G8B8":
            data = ((data[..., 3] << 24) | (data[..., 0] << 16) | (data[..., 1] << 8) | data[..., 2]).flatten()
        elif preset == "Color R5G5B5":
            data = ((data[..., 0] >> 3) << 10) | ((data[..., 1] >> 3) << 5) | (data[..., 2] >> 3)
            data = data.flatten()
        elif preset == "Color R8G8B8":
            data = (data[..., 0] << 16) | (data[..., 1] << 8) | data[..., 2]
            data = data.flatten()
        elif preset == "Grayscale 8":
            grayscale = (0.2989 * data[..., 0] + 0.5870 * data[..., 1] + 0.1140 * data[..., 2]).astype(np.uint8)
            data = grayscale.flatten()
        elif preset == "Monochrome":
            monochrome = (0.2989 * data[..., 0] + 0.5870 * data[..., 1] + 0.1140 * data[..., 2]) > 128
            data = (monochrome.astype(np.uint8) * 255).flatten()

        self.write_output(data, width, height, preset, block_size)

    def write_output(self, data, width, height, format_name, block_size):
        # Replace spaces with underscores in variable names
        output_name = os.path.splitext(os.path.basename(self.selected_file))[0].replace(" ", "_")
        format_name_clean = format_name.replace(" ", "_")
        output_filename = f"{output_name}_{format_name_clean}.h"

        # Check if the file exists and ask for overwrite or new filename
        if os.path.exists(output_filename):
            reply, ok = QInputDialog.getText(
                self, "File Exists",
                f"The file '{output_filename}' already exists. Enter a new filename or press OK to overwrite:",
                text=output_filename
            )
            if ok and reply.strip():
                output_filename = reply.strip()

        # Write the output file
        try:
            with open(output_filename, "w") as f:
                f.write(f"// {output_name}, {width}x{height}\n")
                f.write(f"const unsigned short {output_name}_{format_name_clean} [] PROGMEM = {{\n")
                total_values = len(data)

                for i in range(total_values):
                    if i > 0 and i % width == 0:
                        f.write("\n")

                    f.write(f"0x{data[i]:0{block_size // 4}X}" + (", " if i < total_values - 1 else ""))

                f.write("\n};\n")

            QMessageBox.information(self, "Success", f"Image converted to {format_name} format and saved as '{output_filename}'!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to write file: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    converter = ImageConverter()
    sys.exit(app.exec_())
