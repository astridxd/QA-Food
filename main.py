from LLMModel.CodeLLM import CodeLLM
from LLMModel.AnswerLLM import AnswerLLM
import io
import sys
import pandas as pd

def clean_code(text):
    # Remove all occurrences of ```python and ``` 
    text = text.replace("```python", "").replace("```", "").strip()
    return text

def main():
    # Set the mode: Developer or User. The Developer mode will also showcase the code the LLM is trying to execute, not just the final answer.
    is_dev_mode = input("Enter mode ('dev' for Developer Mode, 'user' for User Mode): ").strip().lower() == "dev"
    
    # Load the data and convert the numeric columns so they are treated as numbers
    df = pd.read_csv("trydata2.csv", sep=",")
    df.iloc[:, 10:] = df.iloc[:, 10:].apply(pd.to_numeric, errors='coerce')
    
    # Display full data in prints of dfs
    pd.set_option('display.max_rows', None)  
    pd.set_option('display.max_columns', None)
    
    code_model = CodeLLM()
    answer_model = AnswerLLM()
    
    while True:
        # Keep answering questions unitll the user says "stop"
        question = input("Enter a question (type 'stop' to quit): ")
        
        if question.lower() == "stop":
            print("Exiting NutriBot. Goodbye!")
            break
        
        try:
            if is_dev_mode:
                print("Generating database query...")
            
            outputs = []
            # Generate 3 code outputs to improve consistency
            for _ in range(3):
                code = code_model.generate(question=question)
                code = clean_code(code)
                
                if is_dev_mode:
                    print("\nGenerated Code:")
                    print(code)
                
                # Set this up to capture output of the generated code
                output_capture = io.StringIO()
                original_stdout = sys.stdout
                sys.stdout = output_capture

                # Execute the code in a try block to catch exceptions
                try:
                    exec(code)
                except Exception as e:
                    if is_dev_mode:
                        print(f"Generated Code Error: {str(e)}")
                finally:
                    sys.stdout = original_stdout
                    
                # Capture the output
                output = output_capture.getvalue()

                if is_dev_mode:
                    print("\nCode Output:")
                    print(output)
                
                outputs.append(output)

            # Generate the final answer based on the question and the 3 outputs
            answer = answer_model.generate(question=question, outputs=outputs)
            print("-" * 50)
            print("Answer:")
            print(answer)
            print("-" * 50)

        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

