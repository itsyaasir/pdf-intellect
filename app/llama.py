"""
This file contains the LLMWrapper class, which is a wrapper for the LlamaCpp class. The LLMWrapper class is used to query the LLM based on the content found in the PDF documents.

"""
from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain


TEMPLATE = """
<|SYSTEM|># Llama-LLM
- You are a helpful, polite, fact-based agent for answering questions about the content of PDF documents.
- Your answers include enough detail for someone to follow through on your suggestions.
<|USER|>

Please answer the following question using the context provided. If you don't know the answer, just say that you don't know. Base your answer on the context below. Say "I don't know" if the answer does not appear to be in the context below. The context is not always the same as the question, so please read the context carefully, and usually the context is composed of multiple text segments.

QUESTION: {question}
CONTEXT:
{context}

ANSWER: <|ASSISTANT|>
"""

template = PromptTemplate(template=TEMPLATE, input_variables=["question", "context"])


class LLMWrapper:
    """
    Wrapper for the LlamaCpp class.
    """

    def __init__(self, model_path):
        self.model_path = model_path
        self.temperature = 0.8
        self.max_length = 2500
        self.top_p = 1
        self.llm = LlamaCpp(
            model_path=self.model_path,
            temperature=self.temperature,
            max_tokens=self.max_length,
            top_p=self.top_p,
            n_ctx=4096,
            n_gpu_layers=1,
            n_batch=512,
            f16_kv=True,
            verbose=True,
        )
        self.chain = LLMChain(
            llm=self.llm,
            prompt=template,
        )

    def query_llm(self, question: str, context: str):
        """
        Query the LLM based on the content found in the PDF documents.
        """
        return self.chain.run(
            question=question,
            context=context,
        )

    def set_temperature(self, temperature):
        """
        Set the temperature for the LLM.
        """
        self.temperature = temperature

    def set_max_length(self, max_length):
        """
        Set the maximum length for the LLM.
        """

        self.max_length = max_length

    def set_top_p(self, top_p):
        """
        Set the top_p for the LLM.
        """
        self.top_p = top_p
