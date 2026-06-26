

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class SummaryAgent:
    def __init__(self, chat_model):
        self.chat_model = chat_model
        # Direct LangChain LCEL implementation
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert Summary Agent. Analyze the document context meticulously."),
            ("user", "Mode: {depth}\n\nDocument Text:\n{text_content}")
        ])
        self.chain = self.prompt | self.chat_model | StrOutputParser()

    def execute(self, text_content, context_prompt="Standard Summary"):
        try:
            return self.chain.invoke({
                "depth": context_prompt, 
                "text_content": text_content[:12000] # Safe token length limit
            })
        except Exception as e:
            return f"Summary Agent Error: {str(e)}"