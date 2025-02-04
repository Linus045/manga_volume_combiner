import shutil
from pathlib import Path


# Map Chapters to volumes
# Key - Volume number
# Value is a a list with the start and end chapter e.g. [0,9] will combine all chapters from 0 to 9
# can be taken from sites like this: https://www.detectiveconanworld.com/wiki/Manga#Volume_21-30_-_Chapters_201-306
mangaMapping = {
    "1": [0,9],
    "2": [10,19],
    "3": [20,29],
    "4": [30,39],
    "5": [40,50],
    "6": [51,60],
    "7": [61,70],
    "8": [71,80],
    "9": [81,90],
    "10": [91,100],
    "11": [101,110],
    "12": [111,120],
    "13": [121,130],
    "14": [131,140],
    "15": [141,150],
    "16": [151,160],
    "17": [161,170],
    "18": [171,180],
    "19": [181,190],
    "20": [191,200],
    "21": [201, 211],
    "22": [212, 221],
    "23": [222, 231],
    "24": [232, 242],
    "25": [243, 253],
    "26": [254, 263],
    "27": [264, 273],
    "28": [274, 284],
    "29": [285, 295],
    "30": [296, 306],
    "31": [307, 317],
    "32": [318, 328],
    "33": [329, 339],
    "34": [340, 350],
    "35": [351, 361],
    "36": [362, 372],
    "37": [373, 382],
    "38": [383, 392],
    "39": [393, 403],
    "40": [404, 413],
    "41": [414, 424],
    "42": [425, 435],
    "43": [436, 446],
    "44": [447, 457],
    "45": [458, 468],
    "46": [469, 479],
    "47": [480, 490],
    "48": [491, 500],
    "49": [501, 510],
    "50": [511, 521],
    "51": [522, 532],
    "52": [533, 543],
    "53": [544, 553],
    "54": [554, 564],
    "55": [565, 575],
    "56": [576, 586],
    "57": [587, 597],
    "58": [598, 608],
    "59": [609, 619],
    "60": [620, 630],
    "61": [631, 641],
    "62": [642, 652],
    "63": [653, 663],
    "64": [664, 674],
    "65": [675, 685],
    "66": [686, 696],
    "67": [697, 707],
    "68": [708, 718],
    "69": [719, 729],
    "70": [730, 740],
    "71": [741, 751],
    "72": [752, 762],
    "73": [763, 773],
    "74": [774, 784],
    "75": [785, 795],
    "76": [796, 806],
    "77": [807, 817],
    "78": [818, 828],
    "79": [829, 839],
    "80": [840, 850],
    "81": [851, 861],
    "82": [862, 872],
    "83": [873, 882],
    "84": [883, 893],
    "85": [894, 904],
    "86": [905, 915],
    "87": [916, 926],
    "88": [927, 937],
    "89": [938, 948],
    "90": [949, 959],
    "91": [960, 970],
    "92": [971, 981],
    "93": [982, 992],
    "94": [993, 1003],
    "95": [1004, 1014],
    "96": [1015, 1025],
    "97": [1026, 1036],
    "98": [1037, 1047],
    "99": [1048, 1058],
    "100": [1059, 1069],
    "101": [1070, 1080],
    "102": [1081, 1091],
    "103": [1092, 1102],
    "104": [1103, 1113],
    "105": [1114, 1123],
    "106": [1124, 1133]
}

mangaDir = Path('manga')
tempDir = Path('temp')
outputZips = Path('output')

mangaName = "Case Closed - Fantranslation"

pageNumber = 1

onlyCreateZips = False

extractVolumeMappingFromDirectoryName = True


def main():
    mangaDir.mkdir(exist_ok=True)
    tempDir.mkdir(exist_ok=True)
    outputZips.mkdir(exist_ok=True)

    if not onlyCreateZips:
        volumePaths = dict()
        for chapter in sorted(mangaDir.iterdir(), key=lambda m: getChapterNumberFromChapterDirectoryName(m)):
            if chapter.is_dir():
                splits = chapter.name.split(" ",2)
                chapterNo = splits[1]
                chapterName = ""
                if len(splits) > 2:
                    chapterName = splits[2]

                volumeNo = findVolumeDirForChapter(chapter.name, chapterNo)

                if volumeNo not in volumePaths:
                    volumePath = tempDir.joinpath("Volume {}".format(volumeNo))
                    volumePath.mkdir()
                    volumePaths[volumeNo] = volumePath

                volumeDir = volumePaths[volumeNo]
                print(f"copying Chapter {chapterNo} into: {volumeNo} - {volumeDir.name}")

                copyChapterToOutputDir(chapter, volumeNo, volumeDir)

    for volumeDir in sorted(tempDir.iterdir(), key=lambda m: int(m.name.split(' ')[-1])):
        zipFile = shutil.make_archive(outputZips.joinpath(f"{volumeDir.name} - {mangaName}"), 'zip', volumeDir)
        zipFilePath = Path(zipFile)
        zipFilename = f"{zipFilePath.stem}.cbz"

        zipFilePath.rename(outputZips.joinpath(zipFilename))



def getChapterNumberFromChapterDirectoryName(chapterDir):
    splits = chapterDir.name.split(' ')
    # Ch.0001 -> 1
    chapterNo = splits[1].split('.')[1]
    return float(chapterNo)


def findVolumeDirForChapter(filename,chapterNo):
    if extractVolumeMappingFromDirectoryName:
        # Vol.01 -> 1
        return filename.split(" ")[0].split(".")[1]
    else:
        # cut off the .5, some chapters are named 19.5 and are a bonus chapter, we wanna include them in the same volume
        chapterNo = chapterNo.split(".")[0]
        for volume, chapterIndices in mangaMapping.items():
            if float(chapterNo) >= float(chapterIndices[0]) and float(chapterNo) <= float(chapterIndices[1]):
                return volume
    raise Exception("Volume for chapter {} not found".format(chapterNo))


def copyChapterToOutputDir(chapterDir, volumeNo, outputDir): 
    global pageNumber
    for page in sorted(chapterDir.iterdir()):
        pageExt = page.suffix
        originalFilename = "{}_{:05d}".format(chapterDir.name, int(page.stem))
        outputFilename = ("{:05d} - Volume {} - {}".format(pageNumber, volumeNo, originalFilename))
        outputFile = outputDir.joinpath("{}.{}".format(outputFilename,pageExt))
        shutil.copy(page, outputFile)
        pageNumber = pageNumber + 1


if __name__ == "__main__":
   main()
