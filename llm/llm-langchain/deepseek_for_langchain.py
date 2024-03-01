from langchain.llms.base import LLM
from typing import Dict, List, Any, Optional
import torch, sys, os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
from langchain_core.output_parsers import StrOutputParser


class deepseek(LLM):
    max_token: int = 2048
    temperature: float = 0.1
    top_p: float = 0.95
    tokenizer: Any
    model: Any

    def __init__(self, model_name_or_path = "deepseek-ai/deepseek-llm-67b-chat", bit4=False):
        super().__init__()
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path,trust_remote_code=True)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        if bit4 == False:
            self.model  = AutoModelForCausalLM.from_pretrained(model_name_or_path, torch_dtype=torch.bfloat16, device_map="auto",
                                                         trust_remote_code=True)
            self.model.generation_config = GenerationConfig.from_pretrained(model_name_or_path)
            self.model.generation_config.pad_token_id = self.model.generation_config.eos_token_id
        else:
            from auto_gptq import AutoGPTQForCausalLM
            self.model = AutoGPTQForCausalLM.from_quantized(model_name_or_path, low_cpu_mem_usage=True, device="cuda:0",
                                                            use_triton=False, inject_fused_attention=False,
                                                            inject_fused_mlp=False)

        if torch.__version__ >= "2" and sys.platform != "win32":
            self.model = torch.compile(self.model)

    @property
    def _llm_type(self) -> str:
        return "Deepseek"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        print('prompt:', prompt)

        messages = [
            {"role": "user", "content": prompt}
        ]
        input_ids = self.tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt")
        input_ids_to_device = input_ids.to(self.model.device)
        generate_input = {
            "input_ids": input_ids_to_device,
            "max_new_tokens": 1024,
            "do_sample": True,
            "top_k": 50,
            "top_p": self.top_p,
            "temperature": self.temperature,
            "repetition_penalty": 1.2,
            "eos_token_id": self.tokenizer.eos_token_id,
            "bos_token_id": self.tokenizer.bos_token_id,
            "pad_token_id": self.tokenizer.pad_token_id
        }
        generate_ids = self.model.generate(**generate_input)
        result_message = self.tokenizer.decode(generate_ids[0][input_ids.shape[1]:], skip_special_tokens=True)
        return result_message



llm = deepseek(
    model_name_or_path="deepseek-ai/deepseek-llm-67b-chat"
)

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

template = "请客观回答下面问题 {product}?"

prompt = PromptTemplate.from_template(template)

llm_chain = LLMChain(prompt=prompt, llm=llm)

generated = llm_chain.run(product="你是谁")
print(generated)


question_gen = prompt | llm | StrOutputParser()

response = question_gen.invoke({"product": "你是谁"})
print(response)
