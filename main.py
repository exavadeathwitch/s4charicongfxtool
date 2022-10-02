from array import array
import os, glob, sys
filesizeoffset = 4
filesize = [0x42, 0x25, 0xFF, 0xFF]
arrmidicon = [0x0C, 0xFC, 0x85, 0x00, 0x00, 0x82, 0x82, 0x82, 0x82, 0xBF, 0x00, 0x33, 0x00, 0x00, 0x00, 0x86, 0x65, 0x80, 0x28, 0x05, 0x80, 0x28, 0x00, 0x02, 0x41, 0xFF, 0xFF, 0xD9, 0x40, 0x00, 0x05, 0x00, 0x00, 0x00, 0x41, 0x85, 0xD9, 0x40, 0x00, 0x05, 0x00, 0x00, 0x0C, 0xB0, 0x0B, 0x00, 0x00, 0x20, 0x15, 0x96, 0x01, 0x60, 0x17, 0x62, 0x80, 0x3B, 0x54, 0x01, 0xD9, 0x60, 0x0E, 0xDB, 0x00, 0x00]
arrboticon = [0xFF, 0x0A, 0x05, 0x00, 0x00, 0x00, 0xFF, 0x0, 0x85, 0x06, 0x03, 0x01, 0x00, 0xFF, 0x40, 0x00]
arrmid = [0x62, 0x72, 0x61, 0x6E, 0x6B, 0x5F, 0x6F, 0x74, 0x68]
arrbot = [0x61, 0x6C, 0x6C, 0x5F, 0x63, 0x68, 0x61, 0x72, 0x69, 0x63, 0x6F, 0x6E, 0x5F, 0x73]
arrdds = [0x2E, 0x64, 0x64, 0x73]
class icon():
    def __init__(self, name, id):
        self.name = name
        self.oldname = name
        self.id = id
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.ddsnum = None
    def __str__(self):
        return f'name: {self.name}, x1: {self.x1}, y1: {self.y1}, x2: {self.x2}, y2: {self.y2}, ddsnum: {self.ddsnum}'
    def fill(self, x1, y1, x2, y2, ddsnum):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.ddsnum = ddsnum

def getintfromarray(gamelist: list[int]) -> int:
    intstr = ''
    for x in gamelist:
        if (0 <= x <= 15):
            intstr += '0' + str(hex(x))[2:]
        else:
            intstr += str(hex(x))[2:]
    return int(intstr, 16)

def getarrayfromint(gameint: int, size: int) -> list[int]:
    retval = []
    var1 = ''
    if len(str(hex(gameint))[2:]) <= size * 2:
        var1 = '0' * (size * 2 - len(hex(gameint).replace('0x', ''))) + str(hex(gameint)).replace('0x', '')
    count = 0
    while True:
        if count == size * 2:
            break
        if count > size * 2:
            raise Exception("oof size")
        retval.append(int(var1[count:count + 2], base = 16))
        count += 2
    return retval

def get_offset(gamelist: list[int], arr: list[int], size: int, ret: bool=False) -> int:
    arraycount = 0
    while True:
        count = 0
        while True:
            if count == len(arr):
                break
            if gamelist[arraycount + count] != arr[count]:
                break
            if count == len(arr) - 1 and gamelist[arraycount + count] == arr[count]:
                return arraycount
            count += 1
        if (gamelist[arraycount] == size):
            if not ret:
                raise Exception("File formatted incorrectly")
            else:
                return 0
        arraycount += 1

def get_offsets(gamelist: list[int], arr: list[int], size: int) -> list[int]:
    retval = []
    count = 0
    while True:
        if count == len(gamelist):
            return retval
        for x in range(0, len(arr)):
            if gamelist[count + x] != arr[x]:
                break
            if x == len(arr) - 1:
                retval.append(count)
        count += 1

def add_icon(gamelist: list[int], name: str, imagenum: int, x1: int, y1: int, x2: int, y2: int, topoffset, bottomoffset):
    namearr = [int(name[x].encode('ansi').hex(), 16) for x in range(0, len(name))]
    botarr = []
    idoffset = topoffset - 10
    idarray = list(reversed([gamelist[x] for x in range(idoffset, idoffset + 2)]))
    newarray = list(reversed(getarrayfromint(getintfromarray(idarray) + 1, 2)))
    for x in range(0, len(arrboticon)):
        if x == 2:
            botarr.append(len(name) + 1)
        elif x == 6:
            for y in range(0, len(name)):
                botarr.append(namearr[y])
        elif x == 13:
            for y in range(0, 2):
                botarr.append(newarray[y])
        elif x > 6:
            botarr.append(arrboticon[x])
        else:
            botarr.append(arrboticon[x])
    for x in range(0, len(botarr)):
        gamelist.insert(bottomoffset - 28, list(reversed(botarr))[x])
    topoffset = get_offset(gamelist, arrmid, file_size)
    bottomoffset = get_offset(gamelist, arrbot, file_size)
    idsection = list(reversed([gamelist[x] for x in range(idoffset + 2, idoffset + 4)]))
    newidsection = list(reversed(getarrayfromint(getintfromarray(idsection) + 1, 2)))
    for x in range(0, 2):
        gamelist[idoffset + 2 + x] = newidsection[x]
        gamelist[idoffset + x] = newarray[x]
    bottomfilesize = list(reversed([gamelist[x] for x in range(topoffset - 14, topoffset - 12)]))
    newbottomfilesize = list(reversed(getarrayfromint(getintfromarray(bottomfilesize) + len(botarr), 2)))
    idf1 = list(reversed([gamelist[x] for x in range(topoffset - 10, topoffset - 8)]))
    newidf1 = list(reversed(getarrayfromint(getintfromarray(idf1) + 1, 2)))
    idf2 = list(reversed([gamelist[x] for x in range(bottomoffset - 20, bottomoffset - 18)]))
    newidf2 = list(reversed(getarrayfromint(getintfromarray(idf2) + 2, 2)))
    for x in range(0, 2):
        gamelist[topoffset - 10 + x] = newidf1[x]
        gamelist[bottomoffset - 20 + x] = newidf2[x]
        gamelist[topoffset - 14 + x] = newbottomfilesize[x]
    section2offset = topoffset - 16
    section2arr = []
    id = list(reversed(getarrayfromint(getintfromarray(idarray) + 1, 2)))
    idminus = list(reversed(getarrayfromint(getintfromarray(idarray), 2)))
    coordlist = [list(reversed(getarrayfromint(x1, 2))), list(reversed(getarrayfromint(y1, 2))),list(reversed(getarrayfromint(x2, 2))), list(reversed(getarrayfromint(y2, 2))) ]
    for x in range(0, len(arrmidicon)):
        if x == 2 or x == 35:
            for y in range(0, 2):
                section2arr.append(idminus[y])
        elif x == 3:
            section2arr.append(imagenum)
        elif 5 <= x <= 8:
            for y in range(0, 2):
                section2arr.append(coordlist[x - 5][y])
        elif x == 15:
            for y in range(0, 2):
                section2arr.append(id[y])
        else:
            section2arr.append(arrmidicon[x])
    for x in range(0, len(section2arr)):
        gamelist.insert(section2offset, list(reversed(section2arr))[x])
    idbot = list(reversed([gamelist[x] for x in range(len(gamelist) - 174, len(gamelist) - 172)]))
    newidbot = list(reversed(getarrayfromint(getintfromarray(idbot) + 2, 2)))
    for x in range(0, 2):
        gamelist[len(gamelist) - 174 + x] = newidbot[x]

def listddsinfo(gamelist: list[int], ddsnum: int) -> str:
    width = []
    height = []
    coordlist = []
    ddscoordlist = (get_offsets(gamelist, arrdds, len(gamelist)))
    for x in range(0, len(ddscoordlist)):
        count = 0
        while True:
            if gamelist[ddscoordlist[x] - count] == 0:
                coordlist.append(ddscoordlist[x] - count - 11)
                break
            count += 1
    for x in range(0, 2):
        width.append(gamelist[coordlist[ddsnum] + 7 + x])
    newwidth = getintfromarray(list(reversed(width)))
    for x in range(0, 2):
        height.append(gamelist[coordlist[ddsnum] + 9 + x])
    newheight = getintfromarray(list(reversed(height)))
    return f'Width: {newwidth} Height: {newheight}'

def changeddscoord(gamelist: list[int], ddsnum, width: int = None, height: int = None):
    coordlist = []
    ddscoordlist = (get_offsets(gamelist, arrdds, len(gamelist)))
    for x in range(0, len(ddscoordlist)):
        count = 0
        while True:
            if gamelist[ddscoordlist[x] - count] == 0:
                coordlist.append(ddscoordlist[x] - count - 11)
                break
            count += 1
    if width != None:
        newwidth = list(reversed(getarrayfromint(width, 2)))
        for x in range(0, 2):
            gamelist[coordlist[ddsnum] + 7 + x] = newwidth[x]
    if height != None:
        newheight = list(reversed(getarrayfromint(height, 2)))
        for x in range(0, 2):
            gamelist[coordlist[ddsnum] + 9 + x] = newheight[x]
    
def getddslist(gamelist: list[int]) -> list[str]:
    retval = []
    coordlist = []
    ddscoordlist = (get_offsets(gamelist, arrdds, len(gamelist)))
    for x in range(0, len(ddscoordlist)):
        count = 0
        while True:
            if gamelist[ddscoordlist[x] - count] == 0:
                coordlist.append(ddscoordlist[x] - count + 1)
                break
            count += 1
    for x in coordlist:
        stringname = ''
        count = 0
        while True:
            if gamelist[x + count] == 0x2E:
                retval.append(stringname[1:])
                break
            else:
                bytes_object = bytes.fromhex(hex(gamelist[x + count])[2:])
                ascii_string = bytes_object.decode("ASCII")
                stringname += ascii_string
            count += 1
    return retval

def getnamelist(gamelist: list[int], charoffset: int, brankoffset: int) -> list[icon]:
    retval = []
    offset = 0
    while True:
        if brankoffset + offset == charoffset:
            break
        if gamelist[brankoffset + offset] == 255:
            if gamelist[brankoffset + offset + 1] == 10:
                name = ''
                namecount = 0
                while True:
                    if gamelist[brankoffset + offset + 6 + namecount] == 0:
                        id = list(reversed([gamelist[x] for x in range(brankoffset + offset + 6 + namecount + 6, brankoffset + offset + 6 + namecount + 6 + 2)]))
                        retval.append(icon(name, getintfromarray(id)))
                        break
                    else:
                        bytes_object = bytes.fromhex(hex(gamelist[brankoffset + offset + 6 + namecount])[2:])
                        ascii_string = bytes_object.decode("ASCII")
                        name += ascii_string
                    namecount += 1
                offset += 1
        offset += 1
    return retval

def geticoninfo(gamelist: list[int], sicon: icon, endoffset: int) -> icon:
    offset = 0
    while True:
        if offset == endoffset:
            return
        data = [gamelist[x] for x in range(offset, offset + 2)]
        id = list(reversed(getarrayfromint(sicon.id, 2)))
        if (data == id):
            ocfc = [gamelist[x] for x in range(offset - 20, offset - 18)]
            if (ocfc == [0x0C, 0xFC]):
                sicon.ddsnum = getintfromarray([gamelist[x] for x in range(offset - 16, offset - 15)])
                sicon.x1 = getintfromarray(list(reversed([gamelist[x] for x in range(offset - 14, offset - 12)])))
                sicon.y1 = getintfromarray(list(reversed([gamelist[x] for x in range(offset - 12, offset - 10)])))
                sicon.x2 = getintfromarray(list(reversed([gamelist[x] for x in range(offset - 10, offset - 8)])))
                sicon.y2 = getintfromarray(list(reversed([gamelist[x] for x in range(offset - 8, offset - 6)])))
                return sicon
        
        offset += 1

def modicon(gamelist: list[int], sicon: icon, endoffset: int, endoffset2: int=0):
    offset = 0
    while True:
        if offset == endoffset:
            break
        data = [gamelist[x] for x in range(offset, offset + 2)]
        id = list(reversed(getarrayfromint(sicon.id, 2)))
        if (data == id):
            ocfc = [gamelist[x] for x in range(offset - 20, offset - 18)]
            if (ocfc == [0x0C, 0xFC]):
                x1 = list(reversed(getarrayfromint(sicon.x1, 2)))
                y1 = list(reversed(getarrayfromint(sicon.y1, 2)))
                x2 = list(reversed(getarrayfromint(sicon.x2, 2)))
                y2 = list(reversed(getarrayfromint(sicon.y2, 2)))
                modoffset = offset - 20
                for x in range(0, 5):
                    if x == 0:
                        gamelist[modoffset + 4] = sicon.ddsnum
                    if x == 1:
                        for y in range(0, 2):
                            gamelist[modoffset + 6 + y] = x1[y]
                    if x == 2:
                        for y in range(0, 2):
                            gamelist[modoffset + 8 + y] = y1[y]
                    if x == 3:
                        for y in range(0, 2):
                            gamelist[modoffset + 10 + y] = x2[y]
                    if x == 4:
                        for y in range(0, 2):
                            gamelist[modoffset + 12 + y] = y2[y]
                
                break
        
        offset += 1
    offset = 0
    if endoffset2 != 0:
        while True:
            if offset == endoffset2:
                break
            data = [gamelist[x] for x in range(offset, offset + 2)]
            id = list(reversed(getarrayfromint(sicon.id, 2)))
            if (data == id):
                ffoa = [gamelist[x] for x in range(offset - (12 + len(sicon.oldname)), offset - (10 + len(sicon.oldname)))]
                if (ffoa == [0xFF, 0x0A]):
                    namearr = list(reversed([int(sicon.name[x].encode('ansi').hex(), 16) for x in range(0, len(sicon.name))]))
                    print(offset - (12 + len(sicon.oldname)))
                    modoffset = offset - (12 + len(sicon.oldname))
                    gamelist[2 + modoffset] = len(sicon.name) + 1
                    for x in range(0, len(sicon.oldname)):
                        gamelist.pop(modoffset + 6)
                    for x in range(0, len(sicon.name)):
                        gamelist.insert(modoffset + 6, namearr[x])
                    topoffset = get_offset(gamelist, arrmid, file_size)
                    bottomfilesize = list(reversed([gamelist[x] for x in range(topoffset - 14, topoffset - 12)]))
                    newbottomfilesize = list(reversed(getarrayfromint(getintfromarray(bottomfilesize) + ((len(sicon.name)) - (len(sicon.oldname))), 2)))
                    for x in range(0, 2):
                        gamelist[topoffset - 14 + x] = newbottomfilesize[x]
                    break
            
            offset += 1
    sicon.oldname = sicon.name
    return

if __name__ == '__main__':
    filename = sys.argv[1]
    choice = ''
    while True:
        file = open(filename, "rb")
        file_size = os.path.getsize(filename)
        gamelist = list(file.read(file_size))
        offset2 = get_offset(gamelist, arrmid, file_size)
        offset3 = get_offset(gamelist, arrbot, file_size)
        iconlist = [geticoninfo(gamelist, x, offset2) for x in getnamelist(gamelist, offset3, offset2)]
        namelist = [x for x in getnamelist(gamelist, offset3, offset2)]
        file.close()
        if choice == '':
            choice = input('Welcome to the Naruto Storm 4 Charicon GFX tool!\nType 1 to add a new roster icon, type 2 to modify an existing icon, or type 3 to modify the dimensions of the dds files.')
        else:
            choice = input('The operation was successfully completed!\nType 1 to add a new roster icon, type 2 to modify an existing icon, or type 3 to modify the dimensions of the dds files.')
        if choice == '1':
            while True:
                name = input("Input the Icon Name:\n")
                x1 = int(input("Input the X1 Coordinate:\n"))
                y1 = int(input("Input the Y1 Coordinate:\n"))
                x2 = int(input("Input the X2 Coordinate:\n"))
                y2 = int(input("Input the Y2 Coordinate:\n"))
                ddsnum = 0
                while True:
                    ddslist = getddslist(gamelist)
                    for x in range(0, len(ddslist)):
                        print(ddslist[x].name)
                    dds = input("Input the DDS file that you'd like to use:\n")
                    val = False
                    for x in ddslist:
                        if x == dds:
                            val = True
                    if val == True:
                        ddsnum = ddslist.index(dds)
                        break
                    else:
                        print('dds file not found.\n')
                add_icon(gamelist, name, ddsnum, x1, y1, x2, y2, offset2, offset3)
                choice = input("Would you like to add another icon? Type Y for yes and anything else for no.\n")
                if choice != 'Y':
                    break
        if choice == '2':
            while True:
                for x in namelist:
                    print(x)
                nname = input("Input the icon that you'd like to modify:\n")
                nameindex = 0
                if nname in [x.name for x in namelist]:
                    nameindex = [x.name for x in namelist].index(nname)
                    break
                else:
                    print('Icon not found.\n')
            while True:
                print(str(iconlist[nameindex]))
                attribute = input("Which attribute would you like to modify?\n")
                if attribute in iconlist[nameindex].__dict__ and attribute != "id":
                    break
                else:
                    print('Invalid attribute.\n')
            if attribute == ("x1" or "y1" or "x2" or "y2" or "ddsnum"):
                newval = int(input("Enter in the new value.\n"))
            else:
                while True:
                    newval = input("Enter in the new value.\n")
                    if newval in [x.name for x in namelist]:
                        print("Cannot have duplicate icon names. Please choose another name.\n")
                    else:
                        break
            iconlist[nameindex].__dict__[attribute] = newval
            modicon(gamelist, iconlist[nameindex], offset2, offset3)
            choice = input("Would you like to modify another value? Type Y for yes and anything else for no.\n")
            if choice != 'Y':
                break
        if choice == '3':
            while True:
                ddsnum = 0
                ddslist = getddslist(gamelist)
                while True:
                    for x in range(0, len(ddslist)):
                        print(ddslist[x])
                    dds = input("Input the DDS file that you'd like to use:\n")
                    val = False
                    for x in ddslist:
                        if x == dds:
                            val = True
                    if val == True:
                        ddsnum = ddslist.index(dds)
                        break
                    else:
                        print('dds file not found.\n')
                print(listddsinfo(gamelist, ddsnum))
                width = 0
                while True:
                    pwidth = int(input('Enter width(1-65535):\n'))
                    if pwidth > 65535 or pwidth <= 0:
                        print('Width too high or too low. Please enter another value.\n')
                    else:
                        width = pwidth
                        break
                    height
                while True:
                    pheight = int(input('Enter height(1-65535):\n'))
                    if pheight > 65535 or pheight <= 0:
                        print('Height not in range. Please enter another value.\n')
                    else:
                        height = pheight
                        break
                changeddscoord(gamelist, ddsnum, width, height)
                choice = input("Would you like to modify another value? Type Y for yes and anything else for no.\n")
                if choice != 'Y':
                    break
        size_list = list(reversed(getarrayfromint(len(gamelist), 4)))
        for x in range(4, 8):
            gamelist[x] = size_list[x - 4]
        file.close()
        file = open(filename, "wb")
        file.write(bytearray([i for i in gamelist]))
        file.close()
