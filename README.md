# Tesseract tessdata downloader from GitHub repositories

Python script to help download only selected traindata from repositories.

## Usage

To download English files usable for tesseract 3.05:
```
$ python3 tessdata_downloader.py -r "tessdata" -t "3.04.00" -l eng
```

To download Orientation and script detection file usable for tesseract 4.0:
```
$ python3 tessdata_downloader.py -l osd
```

## Known issues
- no support for proxy (yet)
- no gui (yet) - this is commandline tool at the moment. If you do not know what does it mean, please do not try this script ;-)
- tested on python 3.6, so there isssues with older python version. Please report only python3 issues. There is no intention to suport python2

## Python Dependencies
* requests

You can install dependencies by:
```
$ pip install -r requirements.txt
```
