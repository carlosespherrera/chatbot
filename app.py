import openai
#import pinecone
from flask import Flask, request, jsonify
#from langchain.vectorstores import Pinecone
#from langchain.embeddings.openai import OpenAIEmbeddings
#from langchain.chat_models import ChatOpenAI
#from langchain.chains import RetrievalQA
#from langchain.chains import RetrievalQAWithSourcesChain
#from langchain.prompts.chat import (
#    ChatPromptTemplate,
#    SystemMessagePromptTemplate,
#    HumanMessagePromptTemplate,
#s)

#from langchain.prompts import PromptTemplate
import asyncio
import sys
from flask import Flask, render_template
#from langchain.retrievers import TFIDFRetriever
#from langchain.memory import ConversationBufferMemory


datos=[]

app = Flask(__name__) 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/answer', methods=['POST'])
def flask_server():
    
    data = request.get_json()
    question = data['pregunta']
    datos.append(question)
    print(datos)
    retriever = TFIDFRetriever.from_texts(datos)
    
    # Configurar OpenAI
    openai.api_key = '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'
    embed_model = "text-embedding-ada-002"
    system_msg = """Responda la pregunta según el contexto (delimited by <ctx></ctx>) a continuación y también utilice el historial de conversación (delimitado por <hs>) para responder las preguntas. Si la pregunta no puede ser respondida según el contexto, por favor, responda "No sé" o "No tengo esa información registrada".
    ---
    <ctx>
    {context}
    </ctx>
    ---

    <hs>
    {history}
    </hs>

    ---
    Question: {question}
    Responde en español:"""
    PROMPT = PromptTemplate(
    template=system_msg, input_variables=["history","context", "question"]
    )

    #chain_type_kwargs = {"prompt": PROMPT}
    

    # Configurar Pinecone
    pinecone_api_key = '10a4e8a2-ec94-4535-acc7-06b2d04b3d83'
    pinecone_api_env = 'us-west4-gcp-free'
    index_name = "carlos"
    pinecone.init(api_key=pinecone_api_key, environment=pinecone_api_env)
    embed = OpenAIEmbeddings(
        model=embed_model,
        openai_api_key='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'
    )

    text_field = "text"
    index = pinecone.Index(index_name)
    vectorstore = Pinecone(
        index, embed.embed_query, text_field
    )

    query=question

    vectorstore.similarity_search(
        query,  # our search query
        k=3  # return 3 most relevant docs
    )

    llm = ChatOpenAI(
        openai_api_key='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',
        model_name='gpt-3.5-turbo',
        temperature=0.0
    )

    
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever() and retriever,
        chain_type_kwargs={"prompt": PROMPT,"memory": ConversationBufferMemory(memory_key="history",input_key="question")}
        
    )

    qa_with_sources = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
    )

    
    result = qa.run(query)
    datos.append(result)
    #result3 = qa({"query": query})
    result2=qa_with_sources(question)
    


    #answer =str( result3["result"])
    sources = result2['sources']

    filename = sources.replace("Reports\\", "")
    #filename=str(result3["source_documents"])

    resutl=result  + "\nFuente: " + filename

    
    response = jsonify(resutl)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    #return response

    return jsonify(resutl )

if __name__ == '__main__':
    
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        app.run(port=8080) 