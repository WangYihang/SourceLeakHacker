#### Description
```
SourceLeakHacker is a muilt-thread web source leak detector.
```

#### Installation
```
pip install -r requirments.txt
```

#### Usage　
```
Usage :
        python SourceLeakHacker.py [URL] [ThreadNumbers] [Timeout]
Example :
        python SourceLeakHacker.py http://127.0.0.1/ 32 16
Tips :
        32 threadNumber is recommended.
        5 second timeout is recommended.(You can also use a decimal to set the timeout.)
        If you have any questions, please contact [ wangyihanger@gmail.com ]
```

#### Demo
![screenshot-00.png](https://raw.githubusercontent.com/WangYihang/SourceLeakHacker/master/image/screenshot-00.png)
![screenshot-01.png](https://raw.githubusercontent.com/WangYihang/SourceLeakHacker/master/image/screenshot-01.png)
![screenshot-02.png](https://raw.githubusercontent.com/WangYihang/SourceLeakHacker/master/image/screenshot-02.png)


#### TODOs
- [ ] Adjust dictionary elements order systematically.
- [x] Arguments parser.
- [x] Store scan result into csv file.
- [ ] Store scan result into sqlite database.
- [ ] Support for multiple urls (from file).
- [ ] Download small url contents, then store them into sqlite database.
- [ ] Change logger in order to suite for both windows and linux.
- [ ] Add log level.
- [ ] Update Screenshots.
- [ ] Update Usage.

