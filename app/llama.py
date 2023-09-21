"""
This file contains the LLMWrapper class, which is a wrapper for the LlamaCpp class. The LLMWrapper class is used to query the LLM based on the content found in the PDF documents.

"""
from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])


TEMPLATE = """[INST] <<SYS>>
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
<</SYS>>
Context: {context}
# Based on Context provide me answer for following question
# Question: {question}

# Tell me the information about the fact. The answer should be from context only
# do not use general knowledge to answer the query
[/INST]"""


prompt = PromptTemplate(template=TEMPLATE, input_variables=["question", "context"])


class LLMWrapper:
    """
    Wrapper for the LlamaCpp class.
    """

    def __init__(self, model_path: str):
        self.model_path: str = model_path
        self.temperature = 0.8
        self.max_length = 2500
        self.top_p = 1
        self.llm = LlamaCpp(
            model_path=self.model_path,
            temperature=self.temperature,
            max_tokens=self.max_length,
            callback_manager=callback_manager,
            top_p=self.top_p,
            n_ctx=4096,
            n_gpu_layers=4,
            n_batch=512,
            f16_kv=True,
            verbose=True,
        )
        self.chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
        )

    def query_llm(self, question: str, context: str):
        """
        Query the LLM based on the content found in the PDF documents.
        """
        final_prompt = prompt.format(question=question, context=context)
        return self.chain.run(final_prompt)

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
