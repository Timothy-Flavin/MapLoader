
#given a sprite sheet and a map image this class creates a map file
#need to allow for sprite sheet array in the future but not now

from PIL import Image
import numpy as np


def pixelsMatch(ty,tx,sy,sx,tileHeight,tileWidth, mImage, sImage):
    match = True
    y=0
    x=0
    while match and y<tileHeight:
        x=0
        while match and x<tileWidth:
            for i in range (4):
                if (mImage[(ty<<5) + y, (tx<<5) + x, i] != sImage[(sy<<5) + y, (sx<<5) + x, i]):
                    match=False
                    break
            x+=1
        y+=1  

    return match  



#print("loaded the stuff")

#print(1)
#print(1<<5)

#TownDemoMapImage
def addToMapString(numLayers, imageName, voidTileNum):
    mapString=""
    layerNum = numLayers
    while layerNum > 0:
        print("Layer: "+str(layerNum))
        mapImage = Image.open(imageName+"_Layer "+str(layerNum)+".png")
        mapImage = np.asarray(mapImage)

        print(mapImage.shape)

        mapWidth=int(mapImage.shape[1]/tileWidth)
        mapHeight=int(mapImage.shape[0]/tileHeight)

        print("mapHeight: "+str(mapHeight))
        print("mapWidth: "+str(mapWidth))
        
        sheetNum=0

        for ty in range(mapHeight):
            for tx in range(mapWidth):
                tileCode="0,0\n"
                #spritesheetnum,tilenum where sprite sheet num -1 = null tile
                tileNotFound = True
                sy=0
                sx=0
                while sy < spriteSheetHeight and tileNotFound:
                    sx=0
                    while sx < spriteSheetWidth and tileNotFound:
                        #print(str(ty)+str(tx))
                        if pixelsMatch(ty,tx,sy,sx,tileHeight,tileWidth, mapImage, spriteSheet):
                            if(sy*spriteSheetWidth+sx == 126):
                                tileCode=str(sheetNum)+",-1\n"
                                print("got to the end")
                            else:
                                tileCode=str(sheetNum)+","+str(sy*spriteSheetWidth+sx)+"\n"
                            tileNotFound=False
                            #print(tileCode)
                        
                        sx+=1
                    sy+=1
                if(tileNotFound):
                    print("tile X: "+str(tx)+", tile Y: "+str(ty))
                mapString+=tileCode
        layerNum-=1
    return mapString



tileWidth = 32
tileHeight = 32
tileSetName =input("input the name of the png's, ex: TownTileSet.png: ")
spriteSheet = np.asarray(Image.open("TownTileSet.png"))
spriteSheetWidth=int(spriteSheet.shape[1]/tileWidth)
spriteSheetHeight=int(spriteSheet.shape[0]/tileHeight)
print("sprite sheet dimensions: "+str(spriteSheetWidth)+", "+str(spriteSheetHeight))
voidTileNum =0 #this is the first empty tile so the map knows to change 15 to -1
mapName = input("input the name of the png's, ex: Bramwich (for Bramwich.png): ")
howManyLayers=int(input("input the number of layers in your map: "))
mapString = addToMapString(howManyLayers, mapName, voidTileNum)

file1 = open(mapName+".txt","w") 

file1.write(mapString)
