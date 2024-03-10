# api-for-open-llm使用

【1】下载[Qwen1.5-14B-Chat-GPTQ-Int8 ](https://modelscope.cn/models/qwen/Qwen1.5-14B-Chat-GPTQ-Int8/summary) 模型权重，将其`目录`记录下来。

> 启动Qwen1.5-14B-Chat-GPTQ-Int8 20GB以上显存比较合适

【2】准备运行环境。

> 推荐另外新建一个虚拟环境来单独运行api-for-open-llm

python=3.10

首先，安装 Pytorch，推荐2.1.2版本。

最后，其他包可以参考本项目`api-for-open-llm-docs/requirements.txt`。

> 与`api-for-open-llm`官方说明的包相比，运行Qwen1.5 GPTQ 量化模型 需要增加optimum和auto-gptq包

【4】进入下载的api-for-open-llm代码目录，将 本项目的`"api-for-open-llm-docs\server.py"` 和 `"api-for-open-llm-docs\.env"文件复制到api-for-open-llm代码目录下。



【5】修改 `.env`配置文件的参数，下面几个是重要的参数。

第3个参数是模型权重地址，需要`改`为第一步下载模型权重时放置的目录地址。

```python
# 1 端口
PORT=8012
# 2 模型名称
MODEL_NAME=qwen2
# 3 大模型本地地址
MODEL_PATH=llm/Qwen1.5-14B-Chat-GPTQ-Int8
# 4 启动后接口名称
PROMPT_NAME=qwen2
```

【6】启动大模型

在api-for-open-llm代码目录运行命令

```
python server.py
```

出现接口信息说明启动成功

```
INFO:     Started server process [169371]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8012 (Press CTRL+C to quit)
```

启动大模型成功就可以去运行agent了。

【7】也可以运行下面测试代码测试大模型接口

```python
from openai import OpenAI

client = OpenAI(
    api_key="EMPTY",
    base_url="http://0.0.0.0:8012/v1/",
)

chat_completion = client.chat.completions.create(
    messages=[{'role': 'user', 'content': '你好'}],
    model="qwen2",
)
print(chat_completion)
```

