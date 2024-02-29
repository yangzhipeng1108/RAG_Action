import pinecone
from langchain_community.vectorstores import Pinecone

from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers.document_compressors import EmbeddingsFilter

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

from langchain.document_transformers import EmbeddingsRedundantFilter
from langchain.retrievers.document_compressors import DocumentCompressorPipeline
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

pinecone.init(api_key="...", environment="...")
vectorstore = Pinecone.from_existing_index("rag-fusion", OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_kwargs={"k":2})
# 4.11 获取与查询匹配的相关上下文

embeddings = OpenAIEmbeddings()
llm = OpenAI()

api_key = ""
#




template ="""
<human>:
Context:{context}

Question:{question}

Use the above Context to answer the user's question.Consider only the Context provided above to formulate response.If the Question asked does not match with the Context provided just say 'I do not know thw answer'.
<bot>:

"""
prompt = PromptTemplate(input_variables=["context","question"],template=template)
chain_type_kwargs = {"prompt":prompt}


compressor = LLMChainExtractor.from_llm(llm=OpenAI(temperature=0.3,openai_api_key=api_key))
redundant_filter = EmbeddingsRedundantFilter(embeddings=embeddings)
relevant_filter = EmbeddingsFilter(embeddings=embeddings,k=5)
#
new_pipeline = DocumentCompressorPipeline(transformers=[compressor,redundant_filter,relevant_filter])
new_compression_retriever = ContextualCompressionRetriever(base_retriever=retriever,
                                                       base_compressor=new_pipeline)


###### RESPONSE ##########
# Document1:
#
# Coinsurance - The percentage of each health care bill a person must pay out of their own pocket. Coinsurance maximum - The most you will have to pay in coinsurance during a policy period (usually a year) before your health plan begins paying 100 percent of the cost of your covered health services.
# 实现问答链


qa = RetrievalQA.from_chain_type(llm=llm,
                                 chain_type="stuff",
                                 retriever=new_compression_retriever,
                                 chain_type_kwargs=chain_type_kwargs,
                                 return_source_documents=True,
                                 verbose=True)
#
response = qa("What is Coinsurance?")
print(response['result'].split("<|endoftext|>")[0])

##### RESPONSE #######
 #  Finished chain.
 # No, Coinsurance is the percentage of each health care bill a person must pay out of their own pocket.
