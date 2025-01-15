🥑 NutriBot: Your Friendly Food Q&A Assistant <br />
"Because sometimes you just need to know how many calories are in that midnight snack!"

🛠️ Behind the Curtain <br />
This project is a Question Answering (QA) system designed to provide information about food nutritional values. <br />
The system uses 2 Large Language Models (Qwen2.5-Coder-3B-Instruct and Phi-3.5-mini-instruct)
to generate code and answers based on a nutritional database. <br />
The origincal data comes from the National Institute for Public Health and the Environment and it can be found via this link: https://www.rivm.nl/documenten/nevo-online-2023-achtergrondinformatie <br />
Data cleanup/prepocessing was necessary and you can find the updated version in the trydata2.csv (some prepocessing steps required include: replace the original dividers "|" with ",", indicate that some 
columns need to be understood as numbers rather than text etc.) 

⚙️ Setup and Usage <br />
Install the required dependencies: pip install pandas transformers newspaper3k <br />
Run the main script: python main.py  (when first running this script the 2 LLMs will autumatically start downloading, this will take a while since they are quite big >= 4GB)

Key Components: <br />
    main.py<br />
        Loads the nutritional data CSV into a pandas DataFrame <br />
        Initializes the LLMModel<br />
        Processes questions and generates answers -> Here you can input your desired question(s) in the questions dictionary.
    LLMModel.py<br />
        Manages two language models: one for code generation and another for answer generation<br />
        Creates prompts for code and answer generation<br />
        Executes the generated code and captures the output <br />

External Tools and APIs:
    Pandas: Used for data manipulation and analysis of the nutritional database.
    Hugging Face Transformers: Utilized for loading and running the language models.
    Language Models: Code Generation: "Qwen/Qwen2.5-Coder-3B-Instruct" || Answer Generation: "microsoft/Phi-3.5-mini-instruct"


🎬 Quick Demo
Here's a real conversation with NutriBot:
You: Calculate the average fat content (in grams) for all foods in the 'Groente' (vegetables) category.
--------------------------------------------------
NutriBot: The average fat content for all foods in the 'Groente' (vegetables) category is approximately 0.465 grams. This value is calculated based on the available data
in the food nutrition database. It represents the mean amount of fat found in various vegetables, providing a general understanding of the fat content within this category.
Please note that this value may vary depending on the specific vegetables included in the calculation and their respective fat contents. For a more accurate representation,
it is recommended to consider the fat content of individual vegetables and their proportions within the 'Groente' category.
--------------------------------------------------

You: What is the energy content (in kcal) of 100 grams of 'Aardappelen rauw' (raw potatoes)?
--------------------------------------------------
NutriBot:
The energy content (in kcal) of 100 grams of 'Aardappelen rauw' (raw potatoes) is 88 kcal. This information comes from the NEVO-Online 2023 food nutrition database.
--------------------------------------------------


📐Project Architecture

The main functionality loop is managed in the main() function, if this project were to be used in other context I would put the main model in a QAMachine class for encapsulated use.
The main() function uses a CodeLLM object to generate database queries and an AnswerLLM object to generate the final answer given the code outputs or a web search as a fallback method.
These CodeLLM and AnswerLLM classes have an LLMModel object which actually contains the model they use to generate. This contains functionality that both LLM classes use for generation.
The prompts are made in the CodeLLM and AnswerLLM classes. There are two utility functions, load_llm_model() and web_search(), which load an LLM model and search a question on the web respectively.

                                                                Project Architecture Graph
                                                                        main()
                                                                CodeLLM   <      >  AnswerLLM
                                                    LLMModel  <        web_search()  <  >    LLMModel
                            Qwen-Coder-2.5-Instruct    <                                         >   Phi-3.5-mini-instruct

🎯 The Journey



🌱 Future Garden
Ideas I'm excited to grow:
Better models on servers that can handle them
Handling g > mg calculations better
Adding more safety when running generated code
Custom dietary preference profiles
Integration with meal planning

🎨 Design Philosophy
Try your best to answer from the provided database, when in doubt, query the internet.
Always provide context, not just facts

🤝 Let's Connect
I'd love to hear your thoughts on making this even better! Feel free to reach out at iliescu.astrid@yahoo.com

Built with ❤️ and probably too much coffee ☕
