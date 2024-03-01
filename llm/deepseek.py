L = {'文件存储': 3.0, '文件存储 目录结构': 1.0, '缓存盘': 0.5, '公共数据盘': 0.3333333333333333}

original_array = sorted(L, key=lambda k: L[k], reverse=True)

odd_part = original_array[::2]
even_part = original_array[1::2][::-1]

prompt = odd_part + even_part
query =  "你是谁"
content = f'请根据一下背景知识{prompt}，回答以下问题{query}'


import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig

model_name = "deepseek-ai/deepseek-llm-67b-chat"
tokenizer = AutoTokenizer.from_pretrained(model_name,trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16, device_map="auto",trust_remote_code=True)
model.generation_config = GenerationConfig.from_pretrained(model_name)
model.generation_config.pad_token_id = model.generation_config.eos_token_id

messages = [
    {"role": "user", "content": content}
]
input_tensor = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt")
outputs = model.generate(input_tensor.to(model.device), max_new_tokens=100)

result = tokenizer.decode(outputs[0][input_tensor.shape[1]:], skip_special_tokens=True)
print(result)

