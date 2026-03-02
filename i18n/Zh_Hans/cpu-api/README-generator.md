
# 概述: `generator.py`

该工具 `generator.py` 允许用户创建小型 C 程序，通过以不同方式调用 `fork` 函数，从而更深入地理解 `fork` 的工作原理。

一个示例用法如下：
```sh
prompt> ./generator.py -n 1 -s 0
```

运行此程序时，你将看到一个随机生成的 C 程序输出结果。具体而言，你会看到类似以下内容：

```c
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <sys/wait.h>
#include <unistd.h>

void wait_or_die() {
    int rc = wait(NULL);
    assert(rc > 0);
}

int fork_or_die() {
    int rc = fork();
    assert(rc >= 0);
    return rc;
}

int main(int argc, char *argv[]) {
    // process a
    if (fork_or_die() == 0) {
        sleep(6);
        // process b
        exit(0);
    }
    wait_or_die();
    return 0;
}
```

让我们来理解一下这段代码。第一部分（从顶部开始，直到 `main()` 函数开头）将被包含在每个生成的 C 程序中。`wait_or_die()` 和 `fork_or_die()` 这两段代码本质上是对 `wait` 和 `fork` 系统调用的简单封装。它们要么成功执行（通常如此），要么通过检查存储在rc中的返回码检测错误，并通过 `assert()` 调用终止程序。当允许直接在失败时退出程序时（此处适用但非普遍情况），这些封装函数能使 `main()` 中的代码更易于阅读。

注：`assert()`，如果你不熟悉它，是一个宏，它简单地检查你传递给它的表达式的真假。如果断言为真，`assert()`就简单地返回，程序继续执行。如果为假，进程将退出。

代码的有趣部分（随着不同随机种子而变化）可以在 `main()`中找到。在这里我们看到主进程（我们称之为“进程 a”，或简称“a”）启动，调用 `fork_or_die()`创建另一个进程，然后等待那个进程完成（通过调用 `wait_or_die()`）。

子进程（称为“b”）只是休眠一段时间（这里是 4 秒），然后退出。

那么，你的挑战是预测当这个程序运行时输出会是什么样子。像往常一样，我们可以简单地使用 `-c`标志来得到结果：

```sh
prompt> ./generator.py -n 1 -s 0 -c
  0 a+
  0 a->b
  6      b+
  6      b-
  6 a<-b
prompt> 
```

解读输出的方法如下。第一列显示特定事件发生的时间。在这个例子中，时间 0 发生了两件事。首先，进程 a 开始运行（用 `a+`表示）；然后，a 进行 fork 并创建了 b（用 `a->b`表示）。

接着，b 开始运行，并立即进入睡眠状态 6 秒，如代码所示。这次睡眠完成后，b 打印出它已被创建（`b+`），但实际上它没做什么；事实上，它只是退出，这也被显示出来了（`b-`）。输出显示这两件事都发生在时间 6；然而，实际上我们知道 `b+`发生在 `b-`之前。

最后，一旦 b 退出，其父进程 a 中的 `wait_or_die()`调用就会返回，然后会进行最终打印（`a<-b`）来表明此事已发生。

有几个标志控制所创建的随机生成代码。它们是：

- `-s SEED`- 不同的随机种子会产生不同的程序
- `-n NUM_ACTIONS`- 程序应包含多少个操作（`fork`, `wait`）
- `-f FORK_CHANCE`- 添加 `fork()`的几率，范围是 1-99%
- `-w WAIT_CHANCE`- 同上，但针对 `wait()`（当然，必须有一个未处理的 `fork`才能调用此操作）
- `-e EXIT_CHANCE`- 同上，但针对进程将 `exit`的几率
- `-S MAX_SLEEP_TIME`- 在代码中添加睡眠时选择的最大睡眠时间

还有一些标志控制为代码创建的 C 文件：

- `-r READABLE`- 这是展示给你的文件（并针对可读性进行了优化）
- `-R RUNNABLE`- 这是将要编译和运行的文件；它与上面相同，但添加了 print 语句等

最后，还有另一个标志 `-A`，可以让你精确指定一个程序。例如：

```sh
prompt> ./generator.py -A "fork b,1 {} wait"
```

以下是结果生成的C代码:
```c
int main(int argc, char *argv[]) {
    // process a
    if (fork_or_die() == 0) {
        sleep(1);
        // process b
        exit(0);
    }
    wait_or_die();
    return 0;
}
```

这个命令创建默认进程 ("a")，然后 "a" 创建了 "b"，"b" 会休眠 1 秒但不做其他任何事情；与此同时，"a" 会等待 "b" 完成。

可以创建更复杂的例子。例如：

- `-A "fork b,1 {} fork c,2 {} wait wait"`- 进程 "a" 创建两个进程 "b" 和 "c"，然后等待两者。
- `-A "fork b,1 {fork c,2 {} fork d,3 {} wait wait} wait"`- 进程 "a" 创建 "b" 并等待其完成；"b" 创建 "c" 和 "d" 并等待它们完成。

请你仔细阅读并完成家庭作业问题，以获得对 `fork`的更全面理解。



