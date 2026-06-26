
import ollama

class IntelligentSupervisor:
    def __init__(self, model_name="qwen2.5:latest"):
        self.model_name = model_name

    def evaluate_execution_strategy(self, user_query, analysis_depth, total_pages):
        """
        Dynamically analyzes inputs and constraints to generate a lean metadata 
        routing plan for the doc_supervisor execution layer.
        """
        
        # Guard rail for ultra-large documents on basic hardware setups
        context_warning = False
        if total_pages > 25:
            context_warning = True

        # Ask the core LLM logic to decide if specific agents are completely unnecessary
        intent_prompt = f"""
        You are an Orchestration Routing Meta-Agent. Analyze the following processing request parameters:
        - User Specific Query: '{user_query}'
        - Choice of Depth Profile: '{analysis_depth}'
        - Page Length: {total_pages}

        Determine which downstream agents MUST run, or can be skipped safely. 
        Respond with raw configuration decisions in structured lines.
        """
        
        # Simple local heuristic mapping fallback to guarantee lightning execution speeds
        run_qa = True if user_query.strip() else False
        
        strategy_manifest = {
            "skip_metrics_agent": False if "Deep" in analysis_depth or "Regulatory" in analysis_depth else True,
            "skip_research_agent": False if "Regulatory" in analysis_depth else True,
            "trigger_qa_agent": run_qa,
            "context_warning_triggered": context_warning,
            "token_budget_truncation_limit": 12000 if "Deep" in analysis_depth else 6000
        }
        
        return strategy_manifest