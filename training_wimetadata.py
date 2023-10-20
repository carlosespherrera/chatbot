import os
import getpass
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
import pinecone 
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm.auto import tqdm
from uuid import uuid4

#PINECONE_API_KEY = getpass.getpass('Pinecone API Key:')

#os.environ['OPENAI_API_KEY'] = getpass.getpass('OpenAI API Key:')
PINECONE_ENV = 'us-west4-gcp-free'

PINECONE_API_KEY='10a4e8a2-ec94-4535-acc7-06b2d04b3d83'

PINECONE_ENVIRONMENT='us-west4-gcp-free'


memory = ConversationBufferMemory( return_messages=True)


pdf_loader = DirectoryLoader('./Reports/', glob="**/*.pdf")
txt_loader = DirectoryLoader('./Reports/', glob="**/*.txt")
word_loader = DirectoryLoader('./Reports/', glob="**/*.docx")

loaders = [pdf_loader, txt_loader, word_loader]
documents = []
for loader in loaders:
    documents.extend(loader.load())





text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
)
chunks = text_splitter.split_documents(documents)





#embeddings = OpenAIEmbeddings()

embeddings = OpenAIEmbeddings(openai_api_key="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", model= 'text-embedding-ada-002')

pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_ENV  # next to api key in console
)

index_name = "carlos"

docsearch = Pinecone.from_documents(chunks, embeddings, index_name=index_name)
print(docsearch)

#modelsystem_msg = f"""Eres un ayudante asistente y tutor de aprendizaje automático. Responda las preguntas en función del contexto proporcionado o diga que no lo sé."."""chat = openai.ChatCompletion.create(model="gpt-4",messages=[{"role": "system", "content": system_msg},{"role": "user", "content": augmented_query}])

qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0,openai_api_key="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"), docsearch.as_retriever(), memory=memory)

"""
index = pinecone.Index(index_name)

vectors = []
for doc in documents:
    text = doc.text
    vector = embeddings.embed_text(text)
    vectors.append(vector)

# Realizar el indexado en Pinecone
index.upsert(vectors=vectors)"""

index = pinecone.Index(index_name)
vectors = []
batch_limit = 100


texts = []
metadatas = []


for i,record in enumerate(tqdm(documents)):
    
    i_end = min(len(documents), i+batch_limit)
    #metadata = documents[i:i_end]
    record_texts = text_splitter.split_documents(documents)
   
    metadata = {
        'Instructivo': str(record.metadata['source']),
        
    }
    record_metadatas = [{
        "chunk": j, "text": text, **metadata
    } for j, text in enumerate(record_texts)]
    #record_metadatas = [{
    #    "chunk": j, "text": text, **metadata
    #} for j, text in enumerate(record_texts)]
    texts.append(record_texts)
    metadatas.append(record_metadatas)
    #metadatas.extend(record_metadatas)
    if len(texts) >= batch_limit:
        ids = [str(uuid4()) for _ in range(len(texts))]
        
        embeds = embeddings.embed_documents(texts)
        
        
        
        index.upsert(vectors=(ids, embeds, metadatas))
        #texts = []
        #metadatas = []


print("modelo entrenado y vectorizado")
print("modelo entrenado y vectorizado")