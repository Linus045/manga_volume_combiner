# HowTo

1. Download a manga via [hakuneko](https://hakuneko.download/)
	See https://www.reddit.com/r/Mangafire/comments/1atva6u/simple_guide_to_download_chapters_on_pc/

2. Put files inside a directory called 'manga'
3. Define how the chapters should be combined (into volumes) by setting the 'mangaMapping' variable inside main.py
4. Set the manga name inside the 'mangaName' variable
5. If you already converted into volumes and wanna recreate the cbz files you can use the 'onlyCreateZips' variable
6. Run the script `python main.py` (CWD should be the root directory)
7. The script will combine the Chapters into volumes as stated in the 'mangaMapping' variable


# TODO:
Add support to add a cover File at the beginning
