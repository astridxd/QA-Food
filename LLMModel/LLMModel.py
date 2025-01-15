from LLMModel.load_llm_model import load_llm_model
import os

# Base LLMModel class, loads a model by name and generates an output given a prompt
class LLMModel:

    def __init__(self, model_name, max_length=1000):
        
        self.max_length = max_length

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        models_dir = os.path.join(project_root, "models")

        self.model, self.tokenizer = load_llm_model(model_name, models_dir)
        
        
    def generate(self, prompt):
        messages = [
            {"role": "system", "content": "You are NutriBot, made for Passionfruit. You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
                
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=512
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response
    