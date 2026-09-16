from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from vector_store import create_vector_store

from dotenv import load_dotenv
load_dotenv()

model = ChatGroq(
  model="openai/gpt-oss-20b",
  temperature=0
)

prompt = PromptTemplate(
    template="""
      You are a helpful assistant.
      Answer ONLY from the provided transcript context.
      If the context is insufficient, just sayI don't know based on this video.

      Conversation History:
      {chat_history}
      
      content:
      {context}
      Question: {question}
    """,
    input_variables = ['chat_history','context', 'question']
)

def ask_question(question : str, vectorstore, chat_history=None)->str:

  retriever = vectorstore.as_retriever(
  search_type="similarity",
  search_kwargs={"k":3}
  )

  docs = retriever.invoke(question)

  docs_with_scores = vectorstore.similarity_search_with_score(question,k=4)

  docs = [doc for doc,score in docs_with_scores]

  context = "\n\n".join(doc.page_content for doc in docs)

  formatted_prompt = prompt.invoke({
    "chat_history": chat_history or "",
    "context": context,
    "question": question
    })

  answer = model.invoke(formatted_prompt)
  
  return answer.content,docs




