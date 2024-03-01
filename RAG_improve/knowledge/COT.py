from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

template = """
Step1 :

I have a problem related to {input}. Could you brainstorm three distinct solutions? Please consider a variety of factors such as {perfect_factors}
A:
"""

prompt = PromptTemplate(
    input_variables=["input", "perfect_factors"],
    template=template
)

chain1 = LLMChain(
    llm=ChatOpenAI(temperature=0, model="gpt-4"),
    prompt=prompt,
    output_key="solutions"
)

template = """
Step 2:

For each of the three proposed solutions, evaluate their potential. Consider their pros and cons, initial effort needed, implementation difficulty, potential challenges, and the expected outcomes. Assign a probability of success and a confidence level to each option based on these factors

{solutions}

A:"""

prompt = PromptTemplate(
    input_variables=["solutions"],
    template=template
)

chain2 = LLMChain(
    llm=ChatOpenAI(temperature=0, model="gpt-4"),
    prompt=prompt,
    output_key="review"
)

template = """
Step 3:

For each solution, deepen the thought process. Generate potential scenarios, strategies for implementation, any necessary partnerships or resources, and how potential obstacles might be overcome. Also, consider any potential unexpected outcomes and how they might be handled.

{review}

A:"""

prompt = PromptTemplate(
    input_variables=["review"],
    template=template
)

chain3 = LLMChain(
    llm=ChatOpenAI(temperature=0, model="gpt-4"),
    prompt=prompt,
    output_key="deepen_thought_process"
)

template = """
Step 4:

Based on the evaluations and scenarios, rank the solutions in order of promise. Provide a justification for each ranking and offer any final thoughts or considerations for each solution
{deepen_thought_process}

A:"""

prompt = PromptTemplate(
    input_variables=["deepen_thought_process"],
    template=template
)

chain4 = LLMChain(
    llm=ChatOpenAI(temperature=0, model="gpt-4"),
    prompt=prompt,
    output_key="ranked_solutions"
)


from langchain.chains import SequentialChain

overall_chain = SequentialChain(
    chains=[chain1, chain2, chain3, chain4],
    input_variables=["input", "perfect_factors"],
    output_variables=["ranked_solutions"],
    verbose=True
)

print(overall_chain({"input": "human colonization of Mars",
                     "perfect_factors": "The distance between Earth and Mars is very large, making regular resupply difficult"}))