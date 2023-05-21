from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

class AIDMChain():

    def __init__(self):
        self._llm = OpenAI()
        self._chain = load_qa_chain(self._llm, chain_type='stuff')

    def run(self, docs, query):
        return self._chain.run(input_documents=docs, question=query)
