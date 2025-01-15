from LLMModel.LLMModel import LLMModel

# LLM class that will generate the code to query the nutritional database
class CodeLLM:
    
    def __init__(self, model_name="Qwen/Qwen2.5-Coder-3B-Instruct"):
        
        self.llm_model = LLMModel(model_name)
        
    
    def _create_prompt(self, question):
        return f"""
            You are a smart assistant and a have a lot of knowledge about food nutrition.
            You are looking at a pandas dataframe that contains nutritional information about different types of food products, pay attention to the header information in the dataframe: and how colums are named. Be very sure to distinguish between vegetables and fruits when answering. And make sure you focus on all aspects of the question and be mindful that some parts might be in Dutch instead of English.
            [  'Food group', 'NEVO-code', 'Dutch food name', 'Food name', 'Synoniem', 'Quantity', 'Opmerking', 'Contains traces of', 'Is fortified with', 'ENERCJ (kj)', 'ENERCC (kcal)', 'WATER', 'PROT', 'PROTPL', 'PROTAN', 'NT', 'TRP', 'FAT', 'FACID', 'FASAT', 'FAMSCIS', 'FAPU', 'FAPUN3', 'FAPUN6', 'FATRS', 'CHO', 'SUGAR', 'STARCH', 'POLYL', 'FIBT', 'ALC', 'OA', 'ASH', 'CHORL', 'NA', 'K', 'CA', 'P', 'MG', 'FE', 'HAEM', 'NHAEM', 'CU', 'SE', 'ZN', 'ID', 'VITA_RAE', 'VITA_RE', 'RETOL', 'CARTBTOT', 'CARTA', 'LUTN', 'ZEA', 'CRYPXB', 'LYCPN', 'VITD', 'CHOCALOH', 'CHOCAL', 'ERGCAL', 'VITE', 'TOCPHA', 'TOCPHB', 'TOCPHD', 'TOCPHG', 'VITK', 'VITK1', 'VITK2', 'THIA', 'RIBF', 'VITB6', 'VITB12', 'NIAEQ', 'NIA', 'FOL', 'FOLFD', 'FOLAC', 'VITC']          
            Sample data:
            Fruits,33,Rozijnen gedroogd,Raisins dried,0,per 100g,0,LUTN,0.0,1378,325,16.8,3.1,3.1,0.0,0.0,0.0,0.5,0.3,0.1,0.0,0.1,0.0,0.1,0.0,71.7,69.0,2.7,0.0,3.7,0.0,4.7,0.0,0.0,25.0,800.0
            Potatoes and tubers,1,Aardappelen rauw,Potatoes raw,0,per 100g,0,0,0.0,371,88,77.0,2.0,2.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,19.0,1.0,18.0,0.0,1.8,0.0,0.0
            Vegetables,17,Cantharel rauw,Mushrooms chanterelle raw,0,per 100g,0,CARTA,0.0,68,16,90.0,1.8,1.8,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,1.0,0.0,2.5,0.0,0.0,1.5,0.0,5.0,500.0
           
            Generate python code that finds the needed data from this database and calculates the answer for this question, make sure to handle na values:
            {question}
    
            If you think you can not answer this question with the database, for questions asking about daily intake requirements for example, just say "print("error")"
            Be careful that when looking in Dutch for foods like 'Aardappelen rauw' you will have to look in the 'Dutch food name' column.
            When checking if something contains something else, you should use str.contains() method.
            
            Pandas has already been imported DO NOT: "import pandas as pd". The data is already in a pandas dataframe called df. 
            Add a print statement to print the result of the data query. Output only python code without comments and print the result, nothing else.
        """
        
    
    def generate(self, question):
        return self.llm_model.generate(self._create_prompt(question))
    