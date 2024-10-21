from pathlib import Path
import zipfile

coverDir = Path('/home/linus/Calibre Library/Gosho Aoyama/')
volumesDir = Path('/home/linus/Calibre Library/Gosho Aoyama/')

# name of the cover file that will be added inside the .cbz file
# make sure its the first file in the archive
coverFileName = '00000 - cover.jpg'

def main():
    # iterate over the .cbz files, and add the cover image added via calibre 'cover.jpg'
    # The cbz files are located in the volumesDir directory inside
    # a sub directory with the name 'Case Closed - Volume 001 (...)'

    # Files in subdirectory created by calibre:
    # - Case Closed - Volume 001 - Gosho Aoyama.cbz
    # - cover.jpg
    # - metadata.opf

    # iterate through the files, in this case they are all from the same author
    # so we can iterate through the whole directory
    for volumeDir in volumesDir.iterdir():
        # iterate through the files and find the cbz file
        for volumeFile in volumeDir.iterdir():
            if volumeFile.is_file() and volumeFile.suffix == '.cbz':
                # add the cover image to the volume

                coverImage = getCoverfile(volumeDir)
                if coverImage is None:
                    print(f"Cover image for volume {volumeDir} not found. Please make sure you added a cover image inside calibre")
                    continue

                # add the cover image to the volume
                print(f'Adding cover image {coverImage} to {volumeFile}')
                addCoverToVolume(volumeFile, coverImage)

def addCoverToVolume(volumeFile, coverImage):
    # make it a zip file
    volumeFile = volumeFile.rename(volumeFile.with_suffix('.zip'))

    # add the cover image to the zip file
    with zipfile.ZipFile(volumeFile, 'a') as zf:
        zf.write(coverImage, coverFileName)

    # rename back to cbz
    volumeFile = volumeFile.rename(volumeFile.with_suffix('.cbz'))

def getCoverfile(volumedir):
    #  find cover.jpg and return it
    for file in volumedir.iterdir():
        if file.is_file() and file.stem == 'cover':
            return file


    # TODO: add option to have a cover directory that contains all cover images instead of grabbing
    # them from calibre
    # foundVolumeDir = None
    # for volumeDir in coverDir.iterdir():
    #     if volumeDir.is_dir():
    #         volumeDirNo = int(volumeDir.stem.split(' ')[1])
    #         if volumeDirNo == volumeNo:
    #             foundVolumeDir = volumeDir
    #             break

    # if foundVolumeDir is None:
    #     print(f'Volume {volumeNo} not found')
    #     return None

    # for file in foundVolumeDir.iterdir():
    #     if file.is_file() and file.stem == 'cover':
    #         return file




if __name__ == '__main__':
    main()
