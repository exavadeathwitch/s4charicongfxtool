from array import array
import os, glob
filesizeoffset = 4
filesize = [0x42, 0x25, 0xFF, 0xFF]
arrmidicon = [0x0C, 0xFC, 0x85, 0x00, 0x00, 0x82, 0x82, 0x82, 0x82, 0xBF, 0x00, 0x33, 0x00, 0x00, 0x00, 0x86, 0x65, 0x80, 0x28, 0x05, 0x80, 0x28, 0x00, 0x02, 0x41, 0xFF, 0xFF, 0xD9, 0x40, 0x00, 0x05, 0x00, 0x00, 0x00, 0x41, 0x85, 0xD9, 0x40, 0x00, 0x05, 0x00, 0x00, 0x0C, 0xB0, 0x0B, 0x00, 0x00, 0x20, 0x15, 0x96, 0x01, 0x60, 0x17, 0x62, 0x80, 0x3B, 0x54, 0x01, 0xD9, 0x60, 0x0E, 0xDB, 0x00, 0x00]
arrboticon = [0xFF, 0x0A, 0x05, 0x00, 0x00, 0x00, 0xFF, 0x0, 0x85, 0x06, 0x03, 0x01, 0x00, 0xFF, 0x40, 0x00]
arrmid = [0x62, 0x72, 0x61, 0x6E, 0x6B, 0x5F, 0x6F, 0x74, 0x68]
arrbot = [0x61, 0x6C, 0x6C, 0x5F, 0x63, 0x68, 0x61, 0x72, 0x69, 0x63, 0x6F, 0x6E, 0x5F, 0x73]

def getintfromarray(gamelist: list[int]) -> int:
    retval = 0
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
    if len(str(gameint)) <= size * 2:
        var1 = '0' * (size * 2 - len(hex(gameint).replace('0x', ''))) + str(hex(gameint)).replace('0x', '')
    print(var1)
    count = 0
    while True:
        if count == size * 2:
            break
        if count > size * 2:
            raise Exception("oof size")
        retval.append(int(var1[count:count + 2], base = 16))
        count += 2
    return retval

def get_offset(gamelist: list[int], arr: list[int], size: int) -> int:
    arraycount = 0
    while True:
        escape = 0
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
            raise Exception("File formatted incorrectly")
        arraycount += 1

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
            section2arr.append(0)
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

    
if __name__ == '__main__':
    filename = os.path.dirname(os.path.realpath(__file__)) + "\\charicon_s.gfx"
    file = open(filename, "rb")
    file_size = os.path.getsize(filename)
    gamelist = list(file.read(file_size))
    name = input("Input the Icon Name:\n")
    x1 = int(input("Input the X1 Coordinate:\n"))
    y1 = int(input("Input the Y1 Coordinate:\n"))
    x2 = int(input("Input the X2 Coordinate:\n"))
    y2 = int(input("Input the Y2 Coordinate:\n"))
    ddsnum = int(input("Input the dds number:\n"))
    offset2 = get_offset(gamelist, arrmid, file_size)
    offset3 = get_offset(gamelist, arrbot, file_size)
    add_icon(gamelist, name, ddsnum, x1, y1, x2, y2, offset2, offset3)
    size_list = list(reversed(getarrayfromint(len(gamelist), 4)))

    print(len(gamelist))
    #update filesize
    for x in range(4, 8):
        gamelist[x] = size_list[x - 4]
    file.close()
    file = open(filename, "wb")
    file.write(bytearray([i for i in gamelist]))
    file.close()