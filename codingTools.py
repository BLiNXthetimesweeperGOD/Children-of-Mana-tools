import struct
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import zlib

def nameNoExt(path):
        """
        Returns the filename with no extension
        """
        return os.path.splitext(os.path.basename(path))[0]
    
def getFileData(file, offset, size):
    with open(file, "rb") as f:
        f.seek(offset)
        return f.read(size)

def getZeroTerminatedString(file, offset):
    string = ""
    scan = b''
    with open(file, "rb") as fileWithString:
        fileWithString.seek(offset)
        while scan != b'\x00':
            scan = fileWithString.read(1)
            if scan != b'\x00':
                string = string+scan.decode("UTF-8")
    return string

def folder(path):
    return os.path.dirname(path)
    
def createOutputDirectoryFromFilePath(path):
    outDir = os.getcwd()+"/OUTPUT/"+folder(path)
    if not os.path.exists(outDir):
        os.makedirs(outDir)
        return outDir

class dialogs:
    def file():
        root = tk.Tk()
        root.withdraw()
        file = filedialog.askopenfilename()
        root.destroy()
        return file
    
    def files():
        root = tk.Tk()
        root.withdraw()
        files = filedialog.askopenfilenames()
        root.destroy()
        return files
    
    def folder():
        root = tk.Tk()
        root.withdraw()
        folder = filedialog.askdirectory()
        root.destroy()
        return folder
    
    def listedFolder():
        root = tk.Tk()
        root.withdraw()
        folder = filedialog.askdirectory()
        root.destroy()
        return os.listdir(folder)

class LE_Pack:
    def byte(value):
        return struct.pack("<b", value)
    
    def ubyte(value):
        return struct.pack("<B", value)
    
    def short(value):
        return struct.pack("<h", value)
    
    def ushort(value):
        return struct.pack("<H", value)
    
    def int(value):
        return struct.pack("<i", value)
    
    def uint(value):
        return struct.pack("<I", value)
    
    def long(value):
        return struct.pack("<q", value)
    
    def ulong(value):
        return struct.pack("<Q", value)
    
    def float(value):
        return struct.pack("<f", value)
    
    def double(value):
        return struct.pack("<d", value)

class LE_MultiPack:
    def byte(values):
        return struct.pack("<{}b".format(len(values)), *values)
    
    def ubyte(values):
        return struct.pack("<{}B".format(len(values)), *values)
    
    def short(values):
        return struct.pack("<{}h".format(len(values)), *values)
    
    def ushort(values):
        return struct.pack("<{}H".format(len(values)), *values)
    
    def int(values):
        return struct.pack("<{}i".format(len(values)), *values)
    
    def uint(values):
        return struct.pack("<{}I".format(len(values)), *values)
    
    def long(values):
        return struct.pack("<{}q".format(len(values)), *values)
    
    def ulong(values):
        return struct.pack("<{}Q".format(len(values)), *values)
    
    def float(values):
        return struct.pack("<{}f".format(len(values)), *values)
    
    def double(values):
        return struct.pack("<{}d".format(len(values)), *values)

class LE_Unpack:
    def byte(data):
        return struct.unpack("<b", data)[0]
    
    def ubyte(data):
        return struct.unpack("<B", data)[0]

    def short(data):
        return struct.unpack("<h", data)[0]
    
    def ushort(data):
        return struct.unpack("<H", data)[0]

    def s24(data):
        return int.from_bytes(data, byteorder='little', signed=True)
           
    def u24(data):
        return int.from_bytes(data, byteorder='little', signed=False)
    
    def int(data):
        return struct.unpack("<i", data)[0]
    
    def uint(data):
        return struct.unpack("<I", data)[0]

    def long(data):
        return struct.unpack("<q", data)[0]
    
    def ulong(data):
        return struct.unpack("<Q", data)[0]
    
    def float(data):
        return struct.unpack("<f", data)[0]
    
    def double(data):
        return struct.unpack("<d", data)[0]

class LE_MultiUnpack:
    def byte(data):
        count = len(data)
        return struct.unpack("<{}b".format(count), data)
    
    def ubyte(data):
        count = len(data)
        return struct.unpack("<{}B".format(count), data)

    def short(data):
        count = len(data) // 2
        return struct.unpack("<{}h".format(count), data)
    
    def ushort(data):
        count = len(data) // 2
        return struct.unpack("<{}H".format(count), data)
    
    def int(data):
        count = len(data) // 4
        return struct.unpack("<{}i".format(count), data)
    
    def uint(data):
        count = len(data) // 4
        return struct.unpack("<{}I".format(count), data)

    def long(data):
        count = len(data) // 8
        return struct.unpack("<{}q".format(count), data)
    
    def ulong(data):
        count = len(data) // 8
        return struct.unpack("<{}Q".format(count), data)
    
    def float(data):
        count = len(data) // 4
        return struct.unpack("<{}f".format(count), data)
    
    def double(data):
        count = len(data) // 8
        return struct.unpack("<{}d".format(count), data)

class BE_BitReader:
    def __init__(self, file, offset=0):
        """Initialize BitReader with a file object opened in binary mode ('rb')
        Args:
            file: File object opened in binary mode
            offset (int): Starting byte offset in the file
        """
        self.file = file
        self.bitBuffer = 0
        self.bitsInBuffer = 0
        if offset > 0:
            self.file.seek(offset)
    
    def read(self, num_bits):
        """Read specified number of bits from the file
        
        Args:
            num_bits (int): Number of bits to read
            
        Returns:
            int: Value read from the bits
        """
        while self.bitsInBuffer < num_bits:
            byte = self.file.read(1)
            if not byte:
                raise EOFError("Reached end of file while reading bits")
            self.bitBuffer = (self.bitBuffer << 8) | int.from_bytes(byte, 'big')
            self.bitsInBuffer += 8
            
        value = (self.bitBuffer >> (self.bitsInBuffer - num_bits)) & ((1 << num_bits) - 1)
        self.bitsInBuffer -= num_bits
        return value
    
    def align(self):
        """Align the bit reader to the next byte boundary by discarding remaining bits"""
        self.bitBuffer = 0
        self.bitsInBuffer = 0
    
    def seek(self, offset):
        """Seek to a specific byte offset in the file
        
        Args:
            offset (int): Byte offset to seek to
        """
        self.file.seek(offset)
        self.bitBuffer = 0
        self.bitsInBuffer = 0
    
    def tell(self):
        """Get current position in the file
        
        Returns:
            tuple: (byte_offset, bits_into_byte)
            - byte_offset is the offset of the last byte read
            - bits_into_byte is how many bits we've read into the current byte
        """
        byte_pos = self.file.tell()
        
        if self.bitsInBuffer > 0:
            complete_bytes = self.bitsInBuffer // 8
            byte_pos -= complete_bytes
            bits_into_byte = 8 - (self.bitsInBuffer % 8)
            if bits_into_byte == 8:
                bits_into_byte = 0
        else:
            bits_into_byte = 0
            
        return (byte_pos, bits_into_byte)

class LE_BitReader:
    def __init__(self, file, chunk_size=1, offset=0):
        """Initialize BitReaderLE with a file object opened in binary mode ('rb')
        
        Args:
            file: File object opened in binary mode
            chunk_size (int): Number of bytes to read at once for each data chunk
            offset (int): Starting byte offset in the file
        """
        self.file = file
        self.chunk_size = chunk_size
        self.bitBuffer = 0
        self.bitsInBuffer = 0
        if offset > 0:
            self.file.seek(offset)
    
    def read(self, num_bits):
        """Read specified number of bits from the file in little endian order
        
        Args:
            num_bits (int): Number of bits to read
            
        Returns:
            int: Value read from the bits
        """
        while self.bitsInBuffer < num_bits:
            bytes_needed = max(self.chunk_size, (num_bits - self.bitsInBuffer + 7) // 8)
            chunk = self.file.read(bytes_needed)
            if not chunk:
                raise EOFError("Reached end of file while reading bits")
                
            # Process bytes in little endian order
            value = int.from_bytes(chunk, 'little')
            self.bitBuffer |= value << self.bitsInBuffer
            self.bitsInBuffer += len(chunk) * 8
            
        # Extract the requested bits
        value = self.bitBuffer & ((1 << num_bits) - 1)
        self.bitBuffer >>= num_bits
        self.bitsInBuffer -= num_bits
        return value
    
    def align(self):
        """Align the bit reader to the next byte boundary by discarding remaining bits"""
        remaining_bits = self.bitsInBuffer % 8
        if remaining_bits:
            self.bitBuffer >>= remaining_bits
            self.bitsInBuffer -= remaining_bits
    
    def seek(self, offset):
        """Seek to a specific byte offset in the file
        
        Args:
            offset (int): Byte offset to seek to
        """
        self.file.seek(offset)
        self.bitBuffer = 0
        self.bitsInBuffer = 0
    
    def tell(self):
        """Get current position in the file
        
        Returns:
            tuple: (byte_offset, bits_into_byte)
            - byte_offset is the offset of the last byte read
            - bits_into_byte is how many bits we've read into the current byte
        """
        byte_pos = self.file.tell()
        
        if self.bitsInBuffer > 0:
            complete_bytes = self.bitsInBuffer // 8
            byte_pos -= complete_bytes
            bits_into_byte = self.bitsInBuffer % 8
        else:
            bits_into_byte = 0
            
        return (byte_pos, bits_into_byte)



class imageData:
    def maxValueForBits(bits): #Used later on in the color functions
        maxValue = (1 << bits) - 1
        return maxValue
    def indexedLinear(bits, file, offset, order, x, y):
        """Reads indexed pixel data of the specified bit width from a file
        
        Format: indexed(bits, file, offset, order, x, y)
        bits defines how many bits there is per pixel
        file defines the file path
        offset defines the start offset in the file
        order defines the pixel order (0 is linear, 1 is reverse order)
        x is the width, y is the height
        
        Returns: A list of integers used to assign colors from a palette to each pixel
        """
        #These might be common mistakes. Fix them automatically for the user.
        if x == 0:
            x = 1
        if y == 0: 
            y = 1
        
        convertedPixels = []
        with open(file, "rb") as pixels:
            pixels.seek(offset)
            pixelReader = BitReader(pixels)
            for vertical in range(y):
                for horizontal in range(x//2):  # Divide by 2 since we're reading pairs
                    if order == 0:  #Linear order (1, 2)
                        pixel1 = pixelReader.read(bits)
                        pixel2 = pixelReader.read(bits)
                        convertedPixels.extend([pixel1, pixel2])
                    elif order == 1:#Reverse order (2, 1)
                        pixel2 = pixelReader.read(bits)
                        pixel1 = pixelReader.read(bits)
                        convertedPixels.extend([pixel1, pixel2])
        return convertedPixels

    def indexedLinearFrame(bits, file, offset, order, x, y, frame):
        """Reads indexed pixel data of the specified bit width from a file (and gets the specified frame or tile)
        
        Format: indexed(bits, file, offset, order, x, y)
        bits defines how many bits there is per pixel
        file defines the file path
        offset defines the start offset in the file
        order defines the pixel order (0 is linear, 1 is reverse order)
        x is the width, y is the height
        frame is the frame number you want parsed
        
        Returns: A list of integers used to assign colors from a palette to each pixel
        """
        #These might be common mistakes. Fix them automatically for the user.
        if x == 0:
            x = 1
        if y == 0: 
            y = 1
        
        convertedPixels = []
        with open(file, "rb") as pixels:
            pixels.seek(offset)
            pixelReader = BitReader(pixels)
            for frames in range(frame): #Skip forward (frame) number of frames
                for vertical in range(y):
                    for horizontal in range(x//2):  # Divide by 2 since we're reading pairs
                        pixelReader.read(bits)
                        pixelReader.read(bits)
            for vertical in range(y):
                for horizontal in range(x//2):  # Divide by 2 since we're reading pairs
                    if order == 0:  #Linear order (1, 2)
                        pixel1 = pixelReader.read(bits)
                        pixel2 = pixelReader.read(bits)
                        convertedPixels.extend([pixel1, pixel2])
                    elif order == 1:#Reverse order (2, 1)
                        pixel2 = pixelReader.read(bits)
                        pixel1 = pixelReader.read(bits)
                        convertedPixels.extend([pixel1, pixel2])
        return convertedPixels

    def bgr555(file, offset, alphaMode, x, y):
        """Reads a BGR555/5551 palette from a file at the specified offset
        
           Format: bgr555(file, offset, alphaMode)
           file defines the file path
           offset defines the start offset in the file
           alphaMode defines if there is or isn't an alpha channel - 1 for True, 0 for False
           x is the width, y is the height
           
           Returns: A list of integers used to assign colors from a palette
           For color palettes, X should be the color count and Y should be 1
        """
        #These might be common mistakes. Fix them automatically for the user.
        if x == 0:
            x = 1
        if y == 0: 
            y = 1
        if alphaMode > 1:
            alphaMode = 1
        
        convertedPixels = []
        with open(file, "rb") as pixels:
            pixels.seek(offset)
            pixelReader = BitReader(pixels)
            for vertical in range(y):
                for horizontal in range(x):
                    blue = pixelReader.read(5)
                    green = pixelReader.read(5)
                    red = pixelReader.read(5)
                    alpha = pixelReader.read(1)
                    
                    blue = (blue * 255) // 31
                    green = (green * 255) // 31
                    red = (red * 255) // 31
                    alpha = alpha * 255
                    
                    if alphaMode == 0:
                        convertedPixels.append((red, green, blue))
                    elif alphaMode == 1:
                        convertedPixels.append((red, green, blue, alpha))
        return convertedPixels
    
    def bgr555LE(file, offset, alphaMode, x, y):
        """Reads a BGR555/5551 palette from a file at the specified offset in little endian byte order
        
           Format: bgr555_little_endian(file, offset, alphaMode)
           file defines the file path
           offset defines the start offset in the file
           alphaMode defines if there is or isn't an alpha channel - 1 for True, 0 for False
           x is the width, y is the height
           
           Returns: A list of integers used to assign colors from a palette
           For color palettes, X should be the color count and Y should be 1
        """
        #These might be common mistakes. Fix them automatically for the user.
        if x == 0:
            x = 1
        if y == 0: 
            y = 1
        if alphaMode > 1:
            alphaMode = 1
        
        convertedPixels = []
        with open(file, "rb") as pixels:
            pixels.seek(offset)
            # Use 2-byte chunks since BGR555 uses 16 bits per pixel
            pixelReader = BitReaderLE(pixels, chunk_size=2)
            
            for vertical in range(y):
                for horizontal in range(x):
                    # In little endian, the order is reversed at the byte level
                    # but we still read the bits in the same order within each 16-bit word
                    red = pixelReader.read(5)
                    green = pixelReader.read(5)
                    blue = pixelReader.read(5)
                    alpha = pixelReader.read(1)
                    
                    blue = (blue * 255) // 31
                    green = (green * 255) // 31
                    red = (red * 255) // 31
                    alpha = alpha * 255
                    
                    if alphaMode == 0:
                        convertedPixels.append((red, green, blue))
                    elif alphaMode == 1:
                        convertedPixels.append((red, green, blue, alpha))
        return convertedPixels

    def rgb555LE(file, offset, alphaMode, x, y):
        """Reads a BGR555/5551 palette from a file at the specified offset in little endian byte order
        
           Format: bgr555_little_endian(file, offset, alphaMode)
           file defines the file path
           offset defines the start offset in the file
           alphaMode defines if there is or isn't an alpha channel - 1 for True, 0 for False
           x is the width, y is the height
           
           Returns: A list of integers used to assign colors from a palette
           For color palettes, X should be the color count and Y should be 1
        """
        #These might be common mistakes. Fix them automatically for the user.
        if x == 0:
            x = 1
        if y == 0: 
            y = 1
        if alphaMode > 1:
            alphaMode = 1
        
        convertedPixels = []
        with open(file, "rb") as pixels:
            pixels.seek(offset)
            # Use 2-byte chunks since BGR555 uses 16 bits per pixel
            pixelReader = BitReaderLE(pixels, chunk_size=2)
            
            for vertical in range(y):
                for horizontal in range(x):
                    # In little endian, the order is reversed at the byte level
                    # but we still read the bits in the same order within each 16-bit word
                    red = pixelReader.read(5)
                    green = pixelReader.read(5)
                    blue = pixelReader.read(5)
                    alpha = pixelReader.read(1)
                    
                    blue = (blue * 255) // 31
                    green = (green * 255) // 31
                    red = (red * 255) // 31
                    alpha = alpha * 255
                    
                    if alphaMode == 0:
                        convertedPixels.append((blue, green, red))
                    elif alphaMode == 1:
                        convertedPixels.append((blue, green, red, alpha))
        return convertedPixels
    
    def rgb555(file, offset, alphaMode, x, y):
        """Reads an RGB555/5551 palette from a file at the specified offset
        
           Format: rgb555(file, offset, alphaMode)
           file defines the file path
           offset defines the start offset in the file
           alphaMode defines if there is or isn't an alpha channel - 1 for True, 0 for False
           x is the width, y is the height
           
           Returns: A list of integers used to assign colors from a palette
           For color palettes, X should be the color count and Y should be 1
        """
        #These might be common mistakes. Fix them automatically for the user.
        if x == 0:
            x = 1
        if y == 0: 
            y = 1
        if alphaMode > 1:
            alphaMode = 1
        
        convertedPixels = []
        with open(file, "rb") as pixels:
            pixels.seek(offset)
            pixelReader = BitReader(pixels)
            for vertical in range(y):
                for horizontal in range(x):
                    red = pixelReader.read(5)
                    green = pixelReader.read(5)
                    blue = pixelReader.read(5)
                    alpha = pixelReader.read(1)
                    
                    red = (red * 255) // 31
                    green = (green * 255) // 31
                    blue = (blue * 255) // 31
                    alpha = alpha * 255
                    
                    if alphaMode == 0:
                        convertedPixels.append((red, green, blue))
                    elif alphaMode == 1:
                        convertedPixels.append((red, green, blue, alpha))
        return convertedPixels

    def customWidthsAndOrder(file, offset, alphaMode, x, y, channelBits, channelOrder, littleEndian=True):
        """Reads a color palette from a file at the specified offset with custom bit widths and channel order
        
           Parameters:
           file: str - defines the file path
           offset: int - defines the start offset in the file
           alphaMode: int - defines if there is or isn't an alpha channel - 1 for True, 0 for False
           x: int - the width (for palettes, this is the color count)
           y: int - the height (for palettes, this should be 1)
           channelBits: list[int] - list of 4 integers defining bit widths for [R,G,B,A]
           channelOrder: list[int] - list of 4 integers defining channel order using [0=R,1=G,2=B,3=A]
           littleEndian: bool - determines which bit reader to use (default: True for little endian)
           
           Returns: A list of tuples containing color values (RGB or RGBA)
           
           Example usage:
           # For BGR format:
           colors = customWidthsAndOrder(file, 0, 1, 16, 1, [5,5,5,1], [2,1,0,3])
           # For RGB format:
           colors = customWidthsAndOrder(file, 0, 1, 16, 1, [5,5,5,1], [0,1,2,3])
        """
        # Input validation
        if x == 0:
            x = 1
        if y == 0: 
            y = 1
        if alphaMode > 1:
            alphaMode = 1
        
        if len(channelBits) != 4 or len(channelOrder) != 4:
            raise ValueError("channelBits and channelOrder must each contain exactly 4 values")
        if not all(0 <= order <= 3 for order in channelOrder):
            raise ValueError("channelOrder values must be between 0 and 3")
        if len(set(channelOrder)) != 4:
            raise ValueError("channelOrder must contain unique values")
        
        # Calculate total bits per pixel to determine chunk size
        total_bits = sum(channelBits)
        chunk_size = (total_bits + 7) // 8  # Round up to nearest byte
        
        convertedPixels = []
        with open(file, "rb") as pixels:
            pixels.seek(offset)
            # Choose the appropriate bit reader based on endianness
            ReaderClass = LE_BitReader if littleEndian else BE_BitReader
            pixelReader = ReaderClass(pixels, chunk_size=chunk_size)
            
            for vertical in range(y):
                for horizontal in range(x):
                    # Initialize color values
                    color_values = [0, 0, 0, 0]  # [R,G,B,A]
                    
                    # Read each channel in the specified order
                    for position, channel_type in enumerate(channelOrder):
                        bits = channelBits[channel_type]
                        if bits > 0:  # Only read if bits > 0
                            value = pixelReader.read(bits)
                            if channel_type == 3: #TEMPORARY FIX, DON'T KEEP!
                                value-=imageData.maxValueForBits(4)
                                if value < 0:
                                    value = value * -1
                            if bits > 0:  # Convert to 8-bit color value
                                value = (value * 255) // imageData.maxValueForBits(bits)
                            color_values[channel_type] = value
                    
                    # Create the final color tuple
                    if alphaMode == 0:
                        convertedPixels.append(tuple(color_values[:3]))  # RGB
                    else:
                        convertedPixels.append(tuple(color_values))  # RGBA
                        
            return convertedPixels
                        
        return convertedPixels
    def readBgr555Palette(file, offset, numColors): #For cases where the palette is little endian
        palette = []
        with open(file, "rb") as f:
            f.seek(offset)
            for i in range(numColors):
                bgr555 = struct.unpack('<H', f.read(2))[0]
                b = (bgr555 & 0x1F) << 3
                g = ((bgr555 >> 5) & 0x1F) << 3
                r = ((bgr555 >> 10) & 0x1F) << 3
                palette.append((r, g, b))
        return palette

    def generateTGA(width, height, pixels):
        """
        Generate TGA file data in memory
        
        Parameters:
        width (int): Image width
        height (int): Image height
        pixels (list): List of RGB or RGBA tuples containing color data
        
        Returns:
        bytearray: Complete TGA file data
        """
        # Validate input
        if len(pixels) != width * height:
            raise ValueError(f"Pixel count {len(pixels)} doesn't match dimensions {width}x{height}")
        
        # Check if we have alpha channel
        has_alpha = len(pixels[0]) == 4
        
        # Initialize TGA header (18 bytes)
        header = bytearray([
            0,      # ID length
            0,      # No color map
            2,      # Uncompressed true-color
            0, 0,   # Color map first entry
            0,      # Color map length LSB
            0,      # Color map length MSB
            0,      # Color map entry size
            0, 0,   # X origin
            0, 0,   # Y origin
            width & 0xFF, (width >> 8) & 0xFF,    # Width LSB, MSB
            height & 0xFF, (height >> 8) & 0xFF,   # Height LSB, MSB
            32 if has_alpha else 24,   # Bits per pixel
            0x28 if has_alpha else 0x20    # Image descriptor (0x20 = normal, 0x28 = normal + 8-bit alpha)
        ])
        
        # Create pixel data
        image_data = bytearray()
        for pixel in pixels:
            # TGA uses BGRA/BGR order
            if has_alpha:
                r, g, b, a = pixel
                image_data.extend([b, g, r, a])
            else:
                r, g, b = pixel
                image_data.extend([b, g, r])
        
        # Optional TGA footer (26 bytes)
        # Convert string to bytes using ord()
        signature = "TRUEVISION-XFILE."
        footer = bytearray([
            0, 0, 0, 0,    # Extension area offset
            0, 0, 0, 0,    # Developer directory offset
        ])
        footer.extend(ord(c) for c in signature)
        footer.append(0)  # Null terminator
        
        # Combine all parts
        tga_data = header + image_data + footer
        
        return tga_data
    
    #TO-DO: Implement a color sorting function so people can define a custom color order for palettes
    #Palette decoders should be designed to be reused to decode non-indexed (RGB/BGR/RGBA/BGRA) image data.
