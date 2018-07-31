# Tesseract tessdata downloader from GitHub repositories

Python script to help download only selected traineddata from repositories.

## Usage

To download English files usable for tesseract 3.05:
```
$ python3 tessdata_downloader.py -r "tessdata" -t "3.04.00" -l eng
```
or you can use windows frozen script:
```
$ tessdata_downloader.exe -r "tessdata" -t "3.04.00" -l eng
```

To download Orientation and script detection file usable for tesseract 4.0:
```
$ python3 tessdata_downloader.py -l osd
```

## Proxy support

Run script with with proxy information

```
$ python3 tessdata_downloader.py -l osd -x proxy_server:proxy_port -U user:password
```

You can also store your proxy information to local file with name [local_settings.py](https://github.com/zdenop/tessdata_downloader/blob/master/local_settings.py). Be carewfull not making your credential public ;-).

## Known issues
- no gui (yet) - this is command line tool at the moment. If you do not know what does it mean, please do not try this script ;-)
- tested on python 3.6, so there issues with older python version. Please report only python3 issues. There is no intention to support python2

## Python Dependencies
* requests

You can install dependencies by:
```
$ pip install -r requirements.txt
```
