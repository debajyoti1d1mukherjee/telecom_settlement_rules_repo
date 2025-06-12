from crewai.tools import tool


# Attempt to import necessary libraries, providing guidance if they are missing.
try:
    from docx import Document
    import pandas as pd
    from PyPDF2 import PdfReader
except ImportError as e:
    print(f"Note: Some libraries for file processing might be missing. Ensure 'python-docx', 'pandas', 'openpyxl', and 'PyPDF2' are installed. Error: {e}")

class FileReadingToolkit():
    name: str = "File Reading Toolkit"
    description: str = "A toolkit capable of reading text, docx, xlsx, and pdf files."

    @staticmethod
    @tool("read_txt_file_tool")
    def read_txt_file_tool(file_path: str) -> str:
        """Reads a .txt file and returns its content as a string."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            return f"Error reading TXT file {file_path}: {str(e)}"

    @staticmethod
    @tool("read_docx_file_tool")
    def read_docx_file_tool(file_path: str) -> str:
        """Reads a .docx file and returns its text content as a string."""
        try:
            from docx import Document
            doc = Document(file_path)
            full_text = [para.text for para in doc.paragraphs]
            return "\n".join(full_text)
        except ImportError:
            return "Error: python-docx library is not installed. Please install it using 'pip install python-docx'."
        except Exception as e:
            return f"Error reading DOCX file {file_path}: {str(e)}"

    @staticmethod
    @tool("read_xlsx_file_tool")
    def read_xlsx_file_tool(file_path: str) -> str:
        """Reads an .xlsx file and returns content from all sheets as a string."""
        try:
            import pandas as pd
            xls = pd.ExcelFile(file_path)
            content = []
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name, header=None) # Read without assuming headers
                # Convert entire sheet to string, trying to capture all data
                sheet_content = df.to_string(index=False, header=False)
                content.append(f"Sheet: {sheet_name}\n{sheet_content}\n\n")
            return "".join(content)
        except ImportError:
            return "Error: pandas and openpyxl libraries are not installed. Please install them using 'pip install pandas openpyxl'."
        except Exception as e:
            return f"Error reading XLSX file {file_path}: {str(e)}"

    @staticmethod
    @tool("read_pdf_file_tool")
    def read_pdf_file_tool(file_path: str) -> str:
        """Reads a .pdf file and returns its text content as a string."""
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text
        except ImportError:
            return "Error: PyPDF2 library is not installed. Please install it using 'pip install PyPDF2'."
        except Exception as e:
            return f"Error reading PDF file {file_path}: {str(e)}"