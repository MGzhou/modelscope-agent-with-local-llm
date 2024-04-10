import openai
import time

client = openai.OpenAI(
    base_url="http://localhost:8012/v1", # "http://<Your api-server IP>:port"
    api_key = "sk-no-key-required"
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an AI assistant. "},
        {"role": "user", "content": "你是谁？"}
    ],
    presence_penalty=1.2,
    temperature=0.6,
    top_p=0.9,
    stream=False,
)
t1 = time.time()

# 非流式响应
# print(response.choices[0].message)


# 流式响应
for chunk in response:
    if hasattr(chunk.choices[0].delta, 'content'):
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='', flush=True)  # 加上flush=True 才实现打字机效果
    else:
        print("\n\nerror")

print(f"\n运行时间{time.time()-t1} 秒")