import os
from dotenv import load_dotenv

from PyPDF2 import PdfReader

from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter

load_dotenv()
DEFAULT_PDF_STORE = os.getenv('PDF_STORE')
DEFAULT_KB_PATH = os.getenv('KNOWLEDGE_BASE')

def _list_pdfs(path):
    files = os.listdir(path)
    pdfs = filter(lambda f: f.endswith('.pdf'), files)
    return list(pdfs)

def _make_chunks(pdf):
    if pdf is not None:
        pdf_reader = PdfReader(pdf)

        pages = []
        for page in pdf_reader.pages:
            try:
                pages.append(page.extract_text())
            except TypeError:
                print('Skipping 1 page')

        splitter = CharacterTextSplitter(
          separator='\n',
          chunk_size=1000,
          chunk_overlap=200,
          length_function=len
        )
        text = '\n\n'.join(pages)
        return splitter.split_text(text)
    return None

def _make_kb(chunks):
    if chunks and len(chunks) > 0:
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)
        return knowledge_base
    return None

def create_knowledge_base(pdf_path=DEFAULT_PDF_STORE, kb_path=DEFAULT_KB_PATH):
    chunks = []
    print('Creating knowledge base')
    print(f'Using PDFs in {pdf_path} and saving to {kb_path}')

    for pdf in _list_pdfs(pdf_path):
        print(f'Chunking {pdf}')
        chunks += _make_chunks(os.path.join(pdf_path, pdf))
    print(f'Making knowledge base from {len(chunks)} chunks')
    knowledge_base = _make_kb(chunks)

    print('Saving knowledge base')
    if knowledge_base is not None:
        knowledge_base.save_local(kb_path)
        return True
    return False

def load_knowledge_base(path=DEFAULT_KB_PATH):
    return FAISS.load_local(path, OpenAIEmbeddings())

if __name__ == '__main__':
    create_knowledge_base()
    
#"My PCs are about to enter the Ivory Triangle. What are the major factions and notable NPCs in that region, and how would they potentially impact the PCs as they travel through the region? Note down some political dynamics and some adventure hooks that might happen along the way."
#"Who were the champions of Rajaat? List the races each of them killed, their original names, where they came from, their number (e.g. first champion), and what happened to them ultimately."
