# 概述

程序 `checksum.py`非常简单：它可以用来计算不同种类（加法、基于异或或 Fletcher）的校验和，这些校验和可以基于程序生成的随机值，也可以基于你以一系列字节形式传入的值。

在默认模式下运行时：

```
prompt> ./checksum.py

OPTIONS seed 0
OPTIONS data_size 4
OPTIONS data

十进制:          216        194        107         66
十六进制:       0xd8       0xc2       0x6b       0x42
二进制:   0b11011000 0b11000010 0b01101011 0b01000010

加法校验和:      ?
异或校验和:      ?
Fletcher校验和: ?

prompt>
```

在这个例子中，程序生成了四个随机数字（"数据"）：216 194 107 66（十进制）。这些数字也用十六进制和二进制显示。

然后程序要求你计算加法、基于异或和 Fletcher 校验和。加法校验和只是将每个字节相加的结果，结果对 256 取模（只是一个单字节的校验和）。基于异或的校验和是将每个字节进行异或操作的结果（也是一个单字节）。最后，Fletcher 校验和是计算 Fletcher 校验和的两个部分的结果（如章节所述），总共是两个字节。

你可以更改种子来获得不同的问题：

```
prompt> ./checksum.py -s 1

OPTIONS seed 1
OPTIONS data_size 4
OPTIONS data

十进制:           34        216        195         65
十六进制:       0x22       0xd8       0xc3       0x41
二进制:   0b00100010 0b11011000 0b11000011 0b01000001

加法校验和:      ?
异或校验和:      ?
Fletcher校验和: ?

prompt>
```

你可以为随机数据指定不同的长度：

```
prompt> ./checksum.py -D 2

...

你也可以指定自己的数据字符串：

prompt> ./checksum.py -D 1,2,3,4

OPTIONS seed 0
OPTIONS data_size 4
OPTIONS data 1,2,3,4

十进制:            1          2          3          4
十六进制:       0x01       0x02       0x03       0x04
二进制:   0b00000001 0b00000010 0b00000011 0b00000100

加法校验和:      ?
异或校验和:      ?
Fletcher校验和: ?

prompt>
```

最后，你可以使用 `-c`让程序为你计算校验和。

```
prompt> ./checksum.py -D 1,2,3,4 -c

OPTIONS seed 0
OPTIONS data_size 4
OPTIONS data 1,2,3,4

十进制:            1          2          3          4
十六进制:       0x01       0x02       0x03       0x04
二进制:   0b00000001 0b00000010 0b00000011 0b00000100

加法校验和:             10       (0b00001010)
异或校验和:              4       (0b00000100)
Fletcher(a,b):   10, 20   (0b00001010,0b00010100)

prompt>
```

这个集合中最糟糕的 README 到此结束。
