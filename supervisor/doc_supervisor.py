

from agents.summary_agent import SummaryAgent
from agents.qa_agent import QAAgent
from agents.metrics_agent import MetricsAgent
from agents.action_agent import ActionAgent
from agents.research_agent import ResearchAgent

class DocSupervisor:
    def __init__(self, chat_model):
        # Dynamic dependency injection
        self.summary_agent = SummaryAgent(chat_model)
        self.qa_agent = QAAgent(chat_model)
        self.metrics_agent = MetricsAgent(chat_model)
        self.action_agent = ActionAgent(chat_model)
        self.research_agent = ResearchAgent(chat_model)

    def orchestrate_analysis(self, doc_data, user_query, analysis_depth):
        raw_text = doc_data["raw_text"]
        tables = doc_data["tables"]
        
        summary_result = self.summary_agent.execute(raw_text, context_prompt=analysis_depth)
        qa_result = self.qa_agent.execute(raw_text, user_query)
        metrics_result = self.metrics_agent.execute(raw_text, tables)
        action_result = self.action_agent.execute(raw_text)
        research_result = self.research_agent.execute(raw_text)
        
        return {
            "summary": summary_result,
            "qa": qa_result,
            "metrics": metrics_result,
            "actions": action_result,
            "research": research_result,
            "page_count": doc_data["page_count"]
        }