

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class MetricsAgent:
    def __init__(self, chat_model):
        self.chat_model = chat_model
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Data Metrics Extraction Agent. Present critical values as a clean key-value Markdown list."),
            ("user", "Tables Data:\n{tables}\n\nText Content:\n{text_content}")
        ])
        self.chain = self.prompt | self.chat_model | StrOutputParser()

    def execute(self, text_content, tables_data):
        try:
            return self.chain.invoke({"tables": str(tables_data), "text_content": text_content[:8000]})
        except Exception as e:
            return f"Metrics Agent Error: {str(e)}"