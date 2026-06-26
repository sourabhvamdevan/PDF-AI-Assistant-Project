

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class PDFReportGenerator:
    @staticmethod
    def generate_report(analysis_results, output_path="reports/analysis_report.pdf"):
  
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        
       
        title_style = ParagraphStyle(
            'DocTitle', parent=styles['Heading1'], fontSize=22, spaceAfter=15
        )
        section_style = ParagraphStyle(
            'SectionHeader', parent=styles['Heading2'], fontSize=14, spaceBefore=12, spaceAfter=6
        )
        body_style = ParagraphStyle(
            'BodyTextCustom', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=8
        )
        
        story = []
        
       
        story.append(Paragraph("AI Multi-Agent Document Intelligence Report", title_style))
        story.append(Paragraph(f"Processed Document Volume: {analysis_results['page_count']} Pages", body_style))
        story.append(Spacer(1, 15))
        
     
        story.append(Paragraph("1. Executive Summary", section_style))
        story.append(Paragraph(analysis_results["summary"].replace("\n", "<br/>"), body_style))
        
   
        story.append(Paragraph("2. Action Items & Timeline Deliverables", section_style))
        story.append(Paragraph(analysis_results["actions"].replace("\n", "<br/>"), body_style))
      

        story.append(Paragraph("3. Extracted KPIs & Structural Data", section_style))
        story.append(Paragraph(analysis_results["metrics"].replace("\n", "<br/>"), body_style))
        
       
        story.append(Paragraph("4. Research & Fact-Validation Notes", section_style))
        story.append(Paragraph(analysis_results["research"].replace("\n", "<br/>"), body_style))
        
       
        story.append(Paragraph("5. Direct Q&A Investigation Response", section_style))
        story.append(Paragraph(analysis_results["qa"].replace("\n", "<br/>"), body_style))
   
        doc.build(story)
        return output_path