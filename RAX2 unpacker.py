#Children of Mana Nintendo DS RAX unpacker
from codingTools import *

print("Because this script also decompresses the files, it might take a while to finish")

#LZSS format overview
"""
"LZSS" file signature
Version number
Compressed data size
Decompressed data size

(Bit stream starts here)
1 = get literal byte from bit stream (read 8 bits)
0 = get back reference (read 8-bit length + 3, read 13-Bit offset)
"""

def decompressLZSS(file):
    currentSize = 0
    bufferIndex = 0
    with open(file, "rb") as lzss:
        lzssReader = BE_BitReader(lzss)
        
        signature = lzss.read(4)
        if signature == b'LZSS': 
            versionNumber = lzss.read(4)
            compressedSize = LE_Unpack.uint(lzss.read(4))
            decompressedSize = LE_Unpack.uint(lzss.read(4))
            
            decompressedData = bytearray(decompressedSize)
            
            while currentSize != decompressedSize:
                bit = lzssReader.read(1)
                if bit == 1:
                    data = lzssReader.read(8)
                    decompressedData[bufferIndex] = data
                    
                    bufferIndex = (bufferIndex + 1)
                    currentSize+=1
                else:
                    length = lzssReader.read(8)+3
                    offset = lzssReader.read(13)
                    source = (bufferIndex - offset - 1)
                    for i in range(length):
                        data = decompressedData[source]
                        decompressedData[bufferIndex] = data
                        source = (source + 1)
                        bufferIndex = (bufferIndex + 1)
                        currentSize+=1
            return decompressedData

#RAX format overview
"""
"RAX2" file signature
File count
Length of filename table
Length of RAX file

(Loop next part)

File format (extension stored as an uppercase string)
Name offset within filename table
File offset after filename table
Size of file
"""

#The following code opens a file, parses the format and saves the embedded files
files = dialogs.files()
for file in files:
    print(f"Unpacking {file}...")
    with open(file, "rb") as rax:
        signature = rax.read(4)
        fileCount = LE_Unpack.uint(rax.read(4))
        fileNames = LE_Unpack.uint(rax.read(4))
        RAX2_Size = LE_Unpack.uint(rax.read(4))

        #Now some additional variables...
        nameTable = (fileCount*16)+16   #Size of entries + header size
        dataStart = nameTable+fileNames #Start of the raw file data

        for fileIndex in range(fileCount): #Main unpacking loop
            fileType = rax.read(4)
            fileName = getZeroTerminatedString(file, LE_Unpack.uint(rax.read(4))+nameTable)
            fileOffset = dataStart+LE_Unpack.uint(rax.read(4))
            fileSize = LE_Unpack.uint(rax.read(4))
            
            #Now extract the data
            fileData = getFileData(file, fileOffset, fileSize)
            
            if fileData.startswith(b'LZSS'): #If it's compressed, decompress it
                with open("TEST.bin", "w+b") as compressed:
                    compressed.write(fileData)
                fileData = decompressLZSS("TEST.bin")
                
            outputDirectory = createOutputDirectoryFromFilePath(fileName)
            with open(f"OUTPUT/{fileName}", "w+b") as outputFile:
                outputFile.write(fileData)
            

        
