

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

import streamlit as st
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from supervisor.doc_supervisor import DocSupervisor
from agents.doc_processor_agent import DocProcessorAgent
from utils.pdf_generator import PDFReportGenerator

load_dotenv()

st.set_page_config(page_title="LangChain AI PDF Assistant", layout="wide")
st.title("LangChain AI PDF Assistant")

@st.cache_resource
def init_langchain_qwen():
    llm = HuggingFaceEndpoint(
        repo_id="Qwen/Qwen2.5-7B-Instruct",
        task="text-generation",
        max_new_tokens=512,
        temperature=0.2
    )
    return ChatHuggingFace(llm=llm)

chat_model = init_langchain_qwen()

analysis_depth = st.sidebar.radio("Analysis Mode", ["Executive Summary", "Deep Dive Audit", "Custom Query"])
uploaded_file = st.file_uploader("Upload your target PDF document", type=["pdf"])
user_query = st.text_input("Ask a specific question about the document:")

if uploaded_file is not None and st.button("Run Multi-Agent Analysis"):
    with st.spinner("Processing Model Agents Pipeline..."):
        
        processor = DocProcessorAgent()
        doc_data = processor.process(uploaded_file)
        
        supervisor = DocSupervisor(chat_model=chat_model)
        results = supervisor.orchestrate_analysis(doc_data, user_query, analysis_depth)
        
        report_out_path = "reports/final_analysis_report.pdf"
        PDFReportGenerator.generate_report(results, report_out_path)
        
        st.success("Analysis Complete!")
        
        with open(report_out_path, "rb") as pdf_file:
            st.download_button(
                label="Download Complete AI PDF Intelligence Report",
                data=pdf_file,
                file_name="AI_Document_Analysis_Report.pdf",
                mime="application/pdf"
            )
        
        st.markdown("---")
        st.subheader("Live Agent Pipeline Dashboard")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Processed Document Volume", value=f"{results['page_count']} Pages")
        with col2:
            action_count = len([line for line in results["actions"].split("\n") if "-" in line or "[" in line])
            st.metric(label="Detected Action Items", value=f"{action_count} Tasks")
        with col3:
            st.metric(label="Pipeline Engine", value="Qwen 2.5 (HF API)")

        st.markdown("---")

        tabs = st.tabs(["Executive Summary", "Actions and Tasks", "Extracted Key Metrics", "Research Insights", "Target Q&A Log"])
        
        with tabs[0]:
            st.markdown("#### Summary Agent Insights")
            short_summary = results["summary"].split("\n\n")[0]
            st.info(short_summary)
            with st.expander("Click to read full summary text"):
                st.write(results["summary"])
            
        with tabs[1]:
            st.markdown("#### Action Agent Operational Task List")
            action_lines = results["actions"].split("\n")
            if len(action_lines) > 5:
                st.write("\n".join(action_lines[:5]))
                with st.expander("View all remaining action items"):
                    st.write("\n".join(action_lines[5:]))
            else:
                st.write(results["actions"])
            
        with tabs[2]:
            st.markdown("#### Metrics Agent Discovered Structural Indicators")
            st.markdown(f"> {results['metrics'][:500]}...")
            with st.expander("View raw key-value structural data"):
                st.write(results["metrics"])
            
        with tabs[3]:
            st.markdown("#### Research Agent Deep Validation Overview")
            st.caption("Operational risks, definitions, and external reference matches:")
            with st.expander("Open detailed research compliance logs"):
                st.write(results["research"])
            
        with tabs[4]:
            st.markdown("#### Targeted Query Context Match")
            if user_query:
                st.info(f"Query Submitted: {user_query}")
                st.write(results["qa"])
            else:
                st.caption("No dynamic validation custom query was submitted for parsing.")
     