#### Description
SourceLeakHacker is a muilt-threads web dictories scanner.

#### Installation
```
pip install -r requirments.txt
```

#### Usage　
```
usage: SourceLeakHacker.py [options]

optional arguments:
  -h, --help            show this help message and exit
  --url URL             url to scan, eg: 'http://127.0.0.1/'
  --urls URLS           file contains urls to sacn, one line one url.
  --folders FOLDERS     dictionary for most common folder names
  --files FILES         dictionary for most common file names
  --backups BACKUPS     dictionary for most common backup file patterns
  --output OUTPUT       output csv filename
  --threads THREADS, -t THREADS
                        threads numbers, default: 4
  --timeout TIMEOUT     HTTP request timeout
  --verbose, -v         log level, eg: -vv
  --version, -V         show program's version number and exit
```

#### Example
```
$ python SourceLeakHacker.py --url=http://baidu.com --threads=4 --timeout=8
[302]   0       3.035766        text/html; charset=iso-8859-1   http://baidu.com/_/_index.php
[302]   0       3.038096        text/html; charset=iso-8859-1   http://baidu.com/_/__index.php.bak
...
[302]   0       0.063973        text/html; charset=iso-8859-1   http://baidu.com/_adm/_index.php
[302]   0       0.081672        text/html; charset=iso-8859-1   http://baidu.com/_adm/_index.php.bak
Result save in file: result/2020-02-27 07:07:47.csv
```

```
$ cat url.txt                 
http://baidu.com/
http://google.com/

$ python SourceLeakHacker.py --urls=url.txt --threads=4 --timeout=8
[302]   0       2.363600        text/html; charset=iso-8859-1   http://baidu.com/_/__index.php.bak
[302]   0       0.098417        text/html; charset=iso-8859-1   http://baidu.com/_adm/__index.php.bak
...
[302]   0       0.060524        text/html; charset=iso-8859-1   http://google.com/_adm/_index.php.bak
[302]   0       0.075042        text/html; charset=iso-8859-1   http://baidu.com/_adm/_index.php.back
Result save in file: result/2020-02-27 07:08:54.csv
```

#### Demo
![screenshot-00.png](https://raw.githubusercontent.com/WangYihang/SourceLeakHacker/master/image/screenshot-00.png)
![screenshot-01.png](https://raw.githubusercontent.com/WangYihang/SourceLeakHacker/master/image/screenshot-01.png)
![screenshot-02.png](https://raw.githubusercontent.com/WangYihang/SourceLeakHacker/master/image/screenshot-02.png)

#### TODOs
- [x] Arguments parser.
- [x] Store scan result into csv file.
- [x] Support for multiple urls (from file).
- [x] Add help comments for every params.
- [x] Update Usage.
- [ ] Adjust dictionary elements order systematically.
- [ ] Change logger in order to suite for both windows and linux.
- [ ] Retry
- [ ] Add log level.
- [ ] Update Screenshots.
- [ ] Store scan result into sqlite database.
- [ ] Download small url contents, then store them into sqlite database.

