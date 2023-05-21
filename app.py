import os
import streamlit as st

from knowledge_base import load_knowledge_base
from chain import AIDMChain

def main():

    knowledge_base = load_knowledge_base()
    chain = AIDMChain()

    st.set_page_config(page_title='aidm')
    st.header('aidm')

    if knowledge_base is not None:
        question = st.text_input('Ask a question')

        if question:
            docs = knowledge_base.similarity_search(question)
            response = chain.run(docs, question)

            st.write(response)


if __name__ == '__main__':
  main()
