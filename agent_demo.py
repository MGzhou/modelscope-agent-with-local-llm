
# 添加项目路径,以访问modelscope_agent代码
import sys
import os
current_file_path = os.path.abspath(__file__)
p_path = os.path.dirname(current_file_path)
print(f"项目路径：{p_path}")
sys.path.append(p_path)

from modelscope_agent.tools.base import BaseTool
from modelscope_agent.tools import register_tool
from modelscope_agent.agents import RolePlay

# 创建工具
@register_tool('RenewInstance')
class AliyunRenewInstanceTool(BaseTool):
    description = '续费一台包年包月ECS实例'
    name = 'RenewInstance'
    parameters: list = [{
        'name': 'instance_id',
        'description': 'ECS实例ID',
        'required': True,
        'type': 'string'
    }, {
        'name': 'period',
        'description': '续费时长以月为单位',
        'required': True,
        'type': 'string'
    }]

    def call(self, params: str, **kwargs):
        print(f"\n[日志]RenewInstance函数已调用")
        params = self._verify_args(params)
        instance_id = params['instance_id']
        period = params['period']
        return str({'result': f'已完成ECS实例ID为{instance_id}的续费，续费时长{period}月'})

# 工具列表
function_list = ['RenewInstance']

# 角色 system prompt
role_template = '你扮演一名AI助理，你需要根据用户的要求来满足他们'
# 模型配置
llm_config = {
    'model': 'qwen2',  # # 该值需要和api-for-open-llm启动的模型名称一样
    'model_server': 'openai',
    #　其他参数
    "api_base": "http://0.0.0.0:8012/v1",
    'api_key':'EMPTY',
    "is_chat": True,
    "is_function_call": False  # 是否采用函数调用方式, Qwen1.5-14B-Chat-GPTQ-Int8不存在function call功能，因此设置为False
}

# 创建agent
bot = RolePlay(function_list=function_list,llm=llm_config, instruction=role_template)


# 使用agent
user_prompt = "请帮我续费一台ECS实例，实例id是：i-rj90a7e840y5cde，续费时长22个月"
print(f"\n用户提问:{user_prompt}\n-------------------------------------------")
response = bot.run(user_prompt, remote=False, print_info=True)
text = ''
for chunk in response:
    text += chunk
print(f"\n[日志] 最终agent结果= \n{text}\n")

