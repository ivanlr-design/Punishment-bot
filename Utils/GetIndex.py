def GetIndex(match, List : list):
    index = 0
    for i in List:
        if match == i:
            return index
        index += 1