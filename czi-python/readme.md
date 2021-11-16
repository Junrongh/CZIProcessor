#   说明

##   目录结构

```
czi-python                          // cziReader根目录
    ├── src                         // python脚本存放目录
    │   ├── input.txt               // 将你想要同时处理的czi文件列表放在这个txt里面
    │   ├── splitChannels.py        // 用于读取czi文件并保存原始信息
    │   ├── tonemapper.py           // 用于调色并保存文件
    ├── data                        // 用于存放你的czi文件
    │   ├── a.czi
    ├── tuned                       // 用于存放生成的各个channels以及brightfield
    ├── readme.md                   // 本文件
```

##  使用说明

1. 将你的czi文件放入data目录下
2. 打开src文件夹，将你一次性想要调整的几个czi文件明写入txt，以回车隔开，建议少于7个文件
3. 在src目录下运行 `python splitChannels.py`
4. 在src目录下运行 `python tonemapper.py` 进行调试
5. 在`rbb czi editor`窗口下按回车保存图片，注意terminal中会提示保存进度
6. 在`rbb czi editor`窗口下按esc退出