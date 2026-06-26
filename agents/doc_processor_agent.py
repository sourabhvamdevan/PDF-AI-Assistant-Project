import pdfplumber

class DocProcessorAgent:
    def __init__(self):
        pass

    def process(self, pdf_file):
        """
        Extracts structural text and tables from the PDF binary.
        """
        full_text=""
        all_tables=[]
        
        with pdfplumber.open(pdf_file) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text:
                    full_text += f"\n--- PAGE {page_num} ---\n" + text
                
                tables = page.extract_tables()
                for table in tables:
                    if table:
                        all_tables.append({"page": page_num, "data": table})
                        
        return {
            "raw_text": full_text.strip(),
            "tables": all_tables,
            "page_count": len(pdf.pages)
        }