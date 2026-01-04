from pathlib import Path
import zipfile

coverDir = Path('covers')
volumesDir = Path('volumes')

# name of the cover file that will be added inside the .cbz file
# make sure its the first file in the archive
coverFileNamePrefix = '00000 - cover - '


# whether to grab the cover image from calibre or from the coverDir
grabCoverFromCalibre = False

def main():
    if not coverDir.exists() or not volumesDir.exists():
        coverDir.mkdir(exist_ok=True)
        volumesDir.mkdir(exist_ok=True)
        print(f'Please add the cover images to {coverDir} and the volumes to {volumesDir}')
        print(f'The Cover image should be named "Volume 01 -... .jpg/png". Important is the volume number after the first space')
        print(f"If you want to grab them from a calibre library, set 'grabCoverFromCalibre' to True. It will then use the cover.jpg file inside the volume directory")
        print(f"The volumes inside the volumes directory should be the .cbz files, named like the cover files with the volume number after the first space")
        return

    # iterate over the .cbz files, and add the cover image added via calibre 'cover.jpg'
    # The cbz files are located in the volumesDir directory inside
    # a sub directory with the name 'Case Closed - Volume 001 (...)'

    # Files in subdirectory created by calibre:
    # - Case Closed - Volume 001 - Gosho Aoyama.cbz
    # - cover.jpg
    # - metadata.opf

    # iterate through the files, in this case they are all from the same author
    # so we can iterate through the whole directory
    if grabCoverFromCalibre:
        for volumeDir in volumesDir.iterdir():
            # iterate through the files and find the cbz file
            for volumeFile in volumeDir.iterdir():
                if volumeFile.is_file() and volumeFile.suffix == '.cbz':
                    volumeNo = getVolumeNo(volumeDir)
                    coverImage = getCoverfile(volumeDir, volumeNo)
                    if coverImage is None:
                        print(f"Cover image for volume {volumeDir} not found. Please make sure you added a cover image inside calibre")
                        continue

                    # add the cover image to the volume
                    print(f'Adding cover image {coverImage} to {volumeFile}')
                    addCoverToVolume(volumeFile, coverImage)
    else:
        # iterate through the volume files directly
        for volumeFile in volumesDir.iterdir():
            if volumeFile.is_file() and volumeFile.suffix == '.cbz':
                volumeNo = getVolumeNo(volumeFile)
                coverImage = getCoverfile(volumeFile, volumeNo)
                if coverImage is None:
                    print(f"Cover image for volume {volumeNo} not found. Please make sure you added a cover image inside calibre")
                    continue

                # add the cover image to the volume
                print(f'Adding cover image {coverImage} to {volumeFile}')
                addCoverToVolume(volumeFile, coverImage)

def addCoverToVolume(volumeFile: Path, coverImage: Path):
    # make it a zip file
    volumeFile = volumeFile.rename(volumeFile.with_suffix('.zip'))

    coverFileName = coverFileNamePrefix + coverImage.stem + '.png'
    # add the cover image to the zip file
    with zipfile.ZipFile(volumeFile, 'a') as zf:
        # check if file already exists
        if coverFileName in zf.namelist():
            print(f'WARNING: Cover image {coverFileName} already exists in {volumeFile}')
        else:
            zf.write(coverImage, coverFileName)

    # rename back to cbz
    volumeFile = volumeFile.rename(volumeFile.with_suffix('.cbz'))


def getVolumeNo(volumeDir):
    return int(volumeDir.stem.split(' ')[1])


def getCoverfile(volumedir, volumeNo):
    #  find cover.jpg and return it
    if grabCoverFromCalibre:
        for file in volumedir.iterdir():
            if file.is_file() and file.stem == 'cover':
                return file
    else:
        # grab cover from coverDir instead of from calibre
        for file in coverDir.iterdir():
            # expected file namne: 'Volume 001 - cover.jpg'
            if file.is_file() and int(file.stem.split(' ')[1]) == volumeNo:
                return file

        print(f'Volume {volumeNo} not found')
        return None

if __name__ == '__main__':
    main()
