# Tesseract tessdata downloader from GitHub repositories

Python script to help download only selected traineddata from repositories.


## Usage

### Program arguments
```
tessdata_downloader.py [-h] [-v] [-o OUTPUT_DIR]
                              [-r {tessdata,tessdata_fast,tessdata_best}]
                              [-lr] [-t TAG] [-lt] [-lof] [-l LANG]
                              [-U PROXY_USER] [-x PROXY]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Print version info
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Directory to store downloaded file. Default:
                        TESSDATA_PREFIX environment variable if set, otherwise
                        current directory
  -r {tessdata,tessdata_fast,tessdata_best}, --repository {tessdata,tessdata_fast,tessdata_best}
                        Specify repository for download. Default:
                        'tessdata_best'
  -lr, --list_repos     Display list of repositories
  -t TAG, --tag TAG     Specify repository tag for download. Default:
                        'the_latest' (e.g. the latest commit)
  -lt, --list_tags      Display list of tag for know repositories
  -lof, --list_of_files
                        Display list of files for specified repository and tag
                        (e.g. argument -r and -t must be used with this
                        argument)
  -l LANG, --lang LANG  Language or data code of traineddata.
  -U PROXY_USER, --proxy-user PROXY_USER
                        <user:password> Proxy user and password.
  -x PROXY, --proxy PROXY
                        host[:port] for https. Use this proxy. If not
                        specified system proxy will be used by default.
```

### Usage examples

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

To download Latin script file usable for tesseract 4.0.0 from repository tessdata_best:
```
$ python3 tessdata_downloader.py  -r "tessdata_best" -t "4.0.0" -l script/Latin -o script
```

To run script with with proxy information:

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
