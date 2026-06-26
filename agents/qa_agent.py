

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class QAAgent:
    def __init__(self, chat_model):
        self.chat_model = chat_model
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a specialized Document Q&A Agent. Answer based strictly on the context provided."),
            ("user", "Question: {query}\n\nContext:\n{text_content}")
        ])
        self.chain = self.prompt | self.chat_model | StrOutputParser()

    def execute(self, text_content, user_query):
        if not user_query:
            return "No custom user query was submitted."
        try:
            return self.chain.invoke({"query": user_query, "text_content": text_content[:12000]})
        except Exception as e:
            return f"Q&A Agent Error: {str(e)}"