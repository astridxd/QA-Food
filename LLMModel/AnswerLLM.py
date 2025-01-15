from LLMModel.LLMModel import LLMModel
from LLMModel.web_search import web_search
import re

# LLM class for generating the final answer either based on code output or a web search as a fallback
class AnswerLLM:
    
    def __init__(self, model_name="microsoft/Phi-3.5-mini-instruct"):
        
        self.llm_model = LLMModel(model_name)
        
    
    def _create_prompt(self, question, outputs, search_results=""):
        if not search_results:
            return f"""
                Answer the following question about the NEVO-Online 2023 food nutrition database:
                {question}
                
                Here are three proposed solutions, pick the one that you think fits best:
                
                Solution 1:
                {outputs[0]}
                
                Solution 2:
                {outputs[1]}
                
                Solution 3:
                {outputs[2]}
                
                Do not mention anything about specific solutions like "Solution 1", the end user does not know about these, they are just for to give a better asnwer. 
                Do not omit any data of the best answer that you pick. Mention that the data in your answer comes from the NEVO-Online 2023 food nutrition database.
                If none of the answers make sense, try your best to answer the question based on your own knowledge instead and be clear about that that is your own knowledge.
            """
        else:
            return f"""
                Answer the following question:
                {question}
                Where you can use these google search results along with your own knowledge to answer the question.
                Make sure to mention the sources you used information from.
                Search results:
                {search_results}
            """
        
    
    # If the generated code results in errors, nan or nothing 2 out of 3 times, resort to a web search for information
    def generate(self, question, outputs):
        search_results = ""
        if not outputs or sum(
            1 for output in outputs if 
            not output.strip() or
            'error' in output.lower() or  
            re.search(r'\bnan\b', output.lower())
        ) >= 2:
            search_results = web_search(question)
            
        return self.llm_model.generate(self._create_prompt(question, outputs, search_results))
    