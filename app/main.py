from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from app.vectorstore import get_vectorstore

QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are FinFriend, a helpful assistant that gives financial insights based on news and social media.

Context:
{context}

Question:
{question}

Answer in a friendly, clear tone with references if possible.
"""
)



def get_chat_engine():
    vectorstore = get_vectorstore()
    llm = ChatOpenAI(temperature=0.4, model_name="gpt-4")

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type="stuff",
        chain_type_kwargs={"prompt": QA_PROMPT},
        return_source_documents=True,
    )
    return qa_chain
