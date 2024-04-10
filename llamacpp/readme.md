# llamacpp qwen 模型使用

## 环境

linux

docker

> 使用CPU推理，使用docker启动

## 模型

使用[qwen1_5-14b-chat-q4_k_m.gguf](https://modelscope.cn/models/qwen/Qwen1.5-14B-Chat-GGUF/files)

## 基本用法

**方式1 docker启动（推荐）**

*下面是通过docker启动，因为是国外仓库，首次启动速度可能很慢。但优点是不需要自行下载源码编译。*

```shell
docker run -p 8012:8080 -v /data/huggingface/Qwen1.5-14B-Chat-GGUF:/models ghcr.io/ggerganov/llama.cpp:server -m models/qwen1_5-14b-chat-q4_k_m.gguf -c 4096 --host 0.0.0.0 --port 8080
```

> -p 是端口映射, 含义是 `主机端口:docker容器端口`。
>
> -v 是容器卷，含义是 `主机地址:容器地址`，将主机地址映射去容器里面。**根据自己下载地址修改这里的主机地址**。
>
> -m 是大模型文件地址，根据-v的映射，本来地址是 /data/huggingface/Qwen1.5-14B-Chat-GGUF/qwen1_5-14b-chat-q4_k_m.gguf 变为 models/qwen1_5-14b-chat-q4_k_m.gguf
>
> -c 是大模型支持上下文窗口大小，默认是512。因为agent需要上下文较长，因此可以适当调高一些。
>
> -port 是启动大模型端口，在这是容器端口。因此，如果想改变访问地址，需要改变 -p 的第一个端口，如想通过 http://127.0.0.1:5000 访问大模型，-p 应该改为 `5000:8080`。

**方式2 命令启动**

```
./server -m /data/huggingface/Qwen1.5-14B-Chat-GGUF/qwen1_5-14b-chat-q4_k_m.gguf -c 4096 --host 0.0.0.0 --port 8012
```

*该启动方式需要先下载源码编译，具体可以参考[llamacpp官方教程](https://github.com/ggerganov/llama.cpp/blob/master/examples/server/README.md)*

如果是Windows则推荐这种方式启动，命令如下

```
server.exe -m models\qwen1_5-14b-chat-q4_k_m.gguf -c 4096 --host 0.0.0.0 --port 8012
```

*根据 CPU下载相应版本 server.exe 执行文件，[b2589版本地址](https://github.com/ggerganov/llama.cpp/releases/tag/b2589)*

## 测试

运行 `llamacpp/test.py` 文件，样例结果如下：

```
我是阿里云开发的一款超大规模语言模型，我叫通义千问。
运行时间10.192398309707642 秒
```
