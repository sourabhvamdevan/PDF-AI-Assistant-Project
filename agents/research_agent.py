

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class ResearchAgent:
    def __init__(self, chat_model):
        self.chat_model = chat_model
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Compliance & Fact-Checking Research Agent. Highlight potential operational risks."),
            ("user", "Document Text:\n{text_content}")
        ])
        self.chain = self.prompt | self.chat_model | StrOutputParser()

    def execute(self, text_content):
        try:
            return self.chain.invoke({"text_content": text_content[:12000]})
        except Exception as e:
            return f"Research Agent Error: {str(e)}"