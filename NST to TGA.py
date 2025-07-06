from codingTools import *

files = dialogs.files()

for file in files:
    pixels = []
    colors = []
    colorCount = 32
    palFile = folder(file)+"/"+nameNoExt(file)+".ntfp"
    print(palFile)
    while True:
        try:
            colors = imageData.customWidthsAndOrder(palFile, 0, 0, colorCount, 1, [5,5,5,1], [0,1,2,3])
            break
        except:
            colorCount-=1
            #print(colorCount)
            #input()
    while len(colors) < 32:
        colors.append((0, 0, 0))
    for colorPal in range(8):
        colors.extend(colors)

    with open(file, "rb") as nst:
        nst.read(4) #Signature
        pixelDataLength = LE_Unpack.uint(nst.read(4))
        imageWidth = LE_Unpack.ushort(nst.read(2))
        padding = nst.read(6)
        #print(imageWidth)
        imageHeight = pixelDataLength//imageWidth
        for i in range(pixelDataLength):
            index = nst.read(1)[0]
            if index == 0:
                pixel = (0,0,0,0)
            else:
                pixel = colors[index]+(255,)
                #print(pixel)
                #input()
            pixels.append(pixel)
        TGA = imageData.generateTGA(imageWidth, imageHeight, pixels)
        with open(folder(file)+"/"+nameNoExt(file)+".tga", "w+b") as tga:
            tga.write(TGA)

        

        
    
