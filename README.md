# modelscope-agent-with-local-llm

## 1 介绍

本项目基于[modelscope-agent-v0.3](https://github.com/modelscope/modelscope-agent) 和 [api-for-open-llm](https://github.com/xusenlinzy/api-for-open-llm) 或 [llamacpp](https://github.com/ggerganov/llama.cpp)组件共同实现了一个AI Agent，能够利用本地的大模型（LLM）实现使用自定义工具功能。

在modelscope-agent的最新版本（v0.3）中，与之前的版本相比，进行了重大的改进。它不再直接支持集成本地大型语言模型，而是通过OpenAI接口与之交互。因此，用户需启动一个集成了OpenAI API风格接口的大模型服务。

为了实现与本地大模型交互，本项目采用了 [api-for-open-llm](https://github.com/xusenlinzy/api-for-open-llm) 或 [llamacpp](https://github.com/ggerganov/llama.cpp) 项目启动集成OpenAI API风格接口的本地大型模型服务。这样，modelscope-agent就可以利用这些服务与大型模型进行交互。

由于硬件限制，在测试时，[api-for-open-llm](https://github.com/xusenlinzy/api-for-open-llm) 选择了 [Qwen1.5-14B-Chat-GPTQ-Int8](https://modelscope.cn/models/qwen/Qwen1.5-14B-Chat-GPTQ-Int8/summary)，llamacpp 选择了 [qwen1_5-14b-chat-q4_k_m.gguf](https://modelscope.cn/models/qwen/Qwen1.5-14B-Chat-GGUF/files)。

本项目还根据需要，对modelscope-agent-v0.3的代码做了一些更改，具体在下面有说明。

## 2 环境

> linux
>
> RTX 3090Ti 24G显存

## 3 使用说明

### 3.1 下载

（1）下载本项目的代码

### 3.2 启动大模型服务接口

- **方式1：**如果存在显卡（显存24GB），推荐使用api-for-open-llm启动服务：说明为 [api-for-open-llm-docs/use-api-for-open-llm.md](https://github.com/MGzhou/modelscope-agent-with-local-llm/blob/main/api-for-open-llm-docs/use-api-for-open-llm.md) 文件。
- **方式2**：CPU启动，推荐llamacpp启动服务：说明为[llamacpp/readme.md](llamacpp/readme.md)文件。

<p style="color:red; font-weight:bold;">一定要先启动大模型服务才可以运行agent</p>

---

### 3.3 运行 agent

【1】**准备运行环境**

python=3.10

首先，安装 Pytorch，推荐2.1.2版本。

最后，其他包可以参考 `requirements.txt`。

一键安装命令：`pip install -r requirements.txt`

【2】**设置agent_demo.py大模型参数**

```python
llm_config = {
    'model': 'qwen2',  # 该值需要和api-for-open-llm启动的模型名称一样
    'model_server': 'openai',
    #　其他参数
    "api_base": "http://0.0.0.0:8012/v1",  # 大模型接口
    'api_key':'EMPTY',
    "is_chat": True,
    "is_function_call": False  # 是否采用函数调用方式, Qwen1.5-14B-Chat-GPTQ-Int8不存在function call功能，因此设置为False
}
```

【3】**运行agent**

运行agent_demo.py文件即可

> 可以参考代码里面的 `创建工具、工具列表`来新增工具。
>
> 在新建工具时，作为测试，我们一般会自行编造返回，这里要强调的是，自行编造的返回需要有意义。不然会导致agent重复调用工具。因为如果没有意义，大模型会认为还没有完成任务，会出现接着循环调用工具的情况。

```shell
python agent_demo.py
```

## 4 效果展示

运行agent_demo.py 结果示例

```python
用户提问:请帮我续费一台ECS实例，实例id是：i-rj90a7e840y5cde，续费时长22个月
-------------------------------------------

[日志]RenewInstance函数已调用

[日志] 最终agent结果= 
好的，我会为您续费这台ECS实例。请稍等，我将调用对应工具来完成操作。
Action: RenewInstance
Action Input: {"instance_id": "i-rj90a7e840y5cde", "period": "22"}

Observation: <result>{'result': '已完成ECS实例ID为i-rj90a7e840y5cde的续费，续费时长22月'}</result>
Answer:您的ECS实例i-rj90a7e840y5cde已经成功续费22个月。现在它将持续运行22个月，直到期满。请确保您的账单信息正确，以防止任何欠费。如有其他需求，请随时告诉我。

```

## 5 修改modelscope-agent代码说明

根据需要，对原始modelscope-agent的代码做了一些更改，具体可以查看本项目modelscope-agent目录下的代码。

（1）修改modelscope_agent/llm/openai.py

```python
# 1 _chat_stream() 函数
去除 **kwargs 参数，使用发现，这个参数没有作用，还可能导致调用大模型出错

# 2 为openai调用设置超时时间 timeout 参数
```

（2）修改modelscope_agent/agents/role_play.py 的_run() 函数

> 这个文件是agent管理者的实现类，通过循环检查大模型返回的信息，判断是否是结束还是调用工具。

```python
# 1 修改最大循环次数
max_turn = 3
# 设定了一个提问最多调用大模型的次数，原始默认最多只能循环10次，我将其设置为3，因为Qwen1.5-14B-Chat-GPTQ-Int8 大模型还不够聪明，可能会出现循环调用工具，将其设置为3已经足够应付了。



# 2 增加将 “调用工具后得到的结果” 添加到大模型输入中的代码
# 这是由于在debug 过程中，发现得到工具的结果后，再次调用大模型self.llm.chat(prompt=planning_prompt,stream=True,...)函数时，发现调用工具的结果并没有进入messages中
messages.append({
    'role': 'user',
    'content': planning_prompt
})

```

## 版权说明

此项目为 `Apache 2.0` 许可证授权，有关详细信息，请参阅 [LICENSE](https://github.com/MGzhou/modelscope-agent-with-local-llm/blob/main/LICENSE)文件。

## 鸣谢

- [modelscope/modelscope-agent: ModelScope-Agent(开源版GPTs)](https://github.com/modelscope/modelscope-agent)
- [xusenlinzy/api-for-open-llm](https://github.com/xusenlinzy/api-for-open-llm)
- [ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp)
