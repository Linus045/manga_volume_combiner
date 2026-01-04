import shutil
from pathlib import Path


# Map Chapters to volumes
# Key - Volume number
# Value is a a list with the start and end chapter e.g. [0,9] will combine all chapters from 0 to 9
# can be taken from sites like this: https://www.detectiveconanworld.com/wiki/Manga#Volume_21-30_-_Chapters_201-306
mangaMapping = {
    "1": [190, 222],
}

mangaDir = Path('manga')
tempDir = Path('temp')
outputZips = Path('output')

mangaName = "Dandadan"

pageNumber = 1

onlyCreateZips = False


# if true
# directory structure should be:
# <root>/manga/Dandadan.22 Ch.190/1.jpg
# <root>/manga/Dandadan.22 Ch.190/2.jpg
# ...

# <root>/manga/Dandadan.22 Ch.191/1.jpg
# <root>/manga/Dandadan.22 Ch.191/2.jpg
# <root>/manga/Dandadan.22 Ch.191/3.jpg
# ...
# <root>/manga/Dandadan.22 Ch.192/1.jpg
# ...
# <root>/manga/Dandadan.23 Ch.193/1.jpg
# ...
# where 22 and 23 are the volume numbers and Ch.190,.. the chapter numbers
# TODO: add description for the False case
extractVolumeMappingFromDirectoryName = True


def main():
    mangaDir.mkdir(exist_ok=True)
    tempDir.mkdir(exist_ok=True)
    outputZips.mkdir(exist_ok=True)

    if not onlyCreateZips:
        volumePaths = dict()
        for chapter in sorted(mangaDir.iterdir(), key=lambda m: getChapterNumberFromChapterDirectoryName(m)):
            if chapter.is_dir():
                splits = chapter.name.split(" ", 2)
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



# Dandadan.01 Ch.123
def getChapterNumberFromChapterDirectoryName(chapterDir):
    splits = chapterDir.name.split(' ')
    # Ch.0001 -> 1
    chapterNo = splits[1].split('.')[1]
    return float(chapterNo)


def findVolumeDirForChapter(filename, chapterNo):
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
        outputFile = outputDir.joinpath("{}.{}".format(outputFilename, pageExt))
        shutil.copy(page, outputFile)
        pageNumber = pageNumber + 1


if __name__ == "__main__":
    main()
