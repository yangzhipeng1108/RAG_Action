
from langchain import PromptTemplate
from langchain.llms import GooglePalm
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0)
# 第 3 步：生成初始基线响应

BASELINE_PROMPT = """Answer the below question which is asking for a concise factual answer. NO ADDITIONAL DETAILS.

Question: {query}

Answer:"""


# Chain to generate initial response
baseline_response_prompt_template = PromptTemplate.from_template(BASELINE_PROMPT)
baseline_response_chain = baseline_response_prompt_template | llm | StrOutputParser()
# 步骤4：生成验证问题的问题模板
# 现在我们将构建一个验证问题模板，该模板将有助于生成下一步的验证问题。

VERIFICATION_QUESTION_TEMPLATE = """Your task is to create a verification question based on the below question provided.
Example Question: Who wrote the book 'God of Small Things' ?
Example Verification Question: Was book [God of Small Things] written by [writer]? If not who wrote [God of Small Things] ? 
Explanation: In the above example the verification question focused only on the ANSWER_ENTITY (name of the writer) and QUESTION_ENTITY (book name).
Similarly you need to focus on the ANSWER_ENTITY and QUESTION_ENTITY from the actual question and generate verification question.

Actual Question: {query}

Final Verification Question:"""


# Chain to generate a question template for verification answers
verification_question_template_prompt_template = PromptTemplate.from_template(VERIFICATION_QUESTION_TEMPLATE)
verification_question_template_chain = verification_question_template_prompt_template | llm | StrOutputParser()
# 第5步：生成验证问题
# 现在我们将使用上面定义的验证问题模板生成验证问题：

VERIFICATION_QUESTION_PROMPT= """Your task is to create a series of verification questions based on the below question, the verfication question template and baseline response.
Example Question: Who wrote the book 'God of Small Things' ?
Example Verification Question Template: Was book [God of Small Things] written by [writer]? If not who wrote [God of Small Things]?
Example Baseline Response: Jhumpa Lahiri
Example Verification Question: 1. Was God of Small Things written by Jhumpa Lahiri? If not who wrote God of Small Things ?


Explanation: In the above example the verification questions focused only on the ANSWER_ENTITY (name of the writer) and QUESTION_ENTITY (name of book) based on the template and substitutes entity values from the baseline response.
Similarly you need to focus on the ANSWER_ENTITY and QUESTION_ENTITY from the actual question and substitute the entity values from the baseline response to generate verification questions.

Actual Question: {query}
Baseline Response: {base_response}
Verification Question Template: {verification_question_template}

Final Verification Questions:"""


# Chain to generate the verification questions
verification_question_generation_prompt_template = PromptTemplate.from_template(VERIFICATION_QUESTION_PROMPT)
verification_question_generation_chain = verification_question_generation_prompt_template | llm | StrOutputParser()
# 第6步：执行验证问题
# 这里我们将使用外部搜索工具代理来执行验证问题。 该代理是使用LangChain的代理和工具模块以及DuckDuckGo搜索模块构建的。
# 注意 – 搜索代理有时间限制，请谨慎使用，因为由于请求之间的时间限制，多个请求可能会导致错误

from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain.tools import DuckDuckGoSearchResults

#create search agent
search = DuckDuckGoSearchResults()
tools = [search]
custom_system_message = "Assistant assumes no knowledge & relies on internet search to answer user's queries."
max_agent_iterations = 5
max_execution_time = 10

chat_agent = ConversationalChatAgent.from_llm_and_tools(
    llm=llm, tools=tools, system_message=custom_system_message
)
search_executor = AgentExecutor.from_agent_and_tools(
    agent=chat_agent,
    tools=tools,
    return_intermediate_steps=True,
    handle_parsing_errors=True,
    max_iterations=max_agent_iterations,
    max_execution_time = max_execution_time
)

# chain to execute verification questions
verification_chain = RunnablePassthrough.assign(
    split_questions=lambda x: x['verification_questions'].split("n"), # each verification question is passed one by one factored approach
) | RunnablePassthrough.assign(
    answers = (lambda x: [{"input": q,"chat_history": []} for q in x['split_questions']])| search_executor.map() # search executed for each question independently
) | (lambda x: "n".join(["Question: {} Answer: {}n".format(question, answer['output']) for question, answer in zip(x['split_questions'], x['answers'])]))# Create final refined response
# 第 7 步：生成最终的改进响应
# 现在我们将生成最终的精确答案，并为其定义提示模板和 llm 链。

FINAL_ANSWER_PROMPT= """Given the below `Original Query` and `Baseline Answer`, analyze the `Verification Questions & Answers` to finally provide the refined answer.
Original Query: {query}
Baseline Answer: {base_response}

Verification Questions & Answer Pairs:
{verification_answers}

Final Refined Answer:"""


# Chain to generate the final answer
final_answer_prompt_template = PromptTemplate.from_template(FINAL_ANSWER_PROMPT)
final_answer_chain = final_answer_prompt_template | llm | StrOutputParser()
# 第8步：将所有链条放在一起
# 现在，我们将之前定义的所有链放在一起，以便它们一次性按顺序运行。

chain = RunnablePassthrough.assign(
    base_response=baseline_response_chain
) |  RunnablePassthrough.assign(
    verification_question_template=verification_question_template_chain
) | RunnablePassthrough.assign(
    verification_questions=verification_question_generation_chain
) | RunnablePassthrough.assign(
    verification_answers=verification_chain
) | RunnablePassthrough.assign(
    final_answer=final_answer_chain
)

response = chain.invoke({"query": "Who wrote the book 'Economics of Small Things' ?"})
print(response)
#output of response
# {'query': "Who wrote the book 'Economics of Small Things' ?", 'base_response': 'Sanjay Jain', 'verification_question_template': 'Was book [Economics of Small Things] written by [writer]? If not who wrote [Economics of Small Things] ?', 'verification_questions': '1. Was Economics of Small Things written by Sanjay Jain? If not who wrote Economics of Small Things ?', 'verification_answers': 'Question: 1. Was Economics of Small Things written by Sanjay Jain? If not who wrote Economics of Small Things ? Answer: The Economics of Small Things was written by Sudipta Sarangi n', 'final_answer': 'Sudipta Sarangi'}
