
## Prompt Engineering Techniques

1. Given Clear Role,Persona
2. Concise task
3. Giving All tools Access before Logical Instruction help align reasoning with tools classificarion.
4. Tools Formatting:
   - As LLm Can select tool but when we have a lot of arguments then passing pydantic schema helps model to better understand all the requirements, with clear description of parameters, type of data etc.

   - Giving Tool name then Their rich Information Description (As of now , we should extensively test for refine)

   - Ex:
   ![tool formatting for system prompt](results/Screenshot%20from%202025-01-06%2012-56-38.png)

5. Think and planning Reasoning:
    - Breaking user input and predicting intents will help in finding overlapping tools.
    - Define Selection confidence scale (This will help llm om which basis it should consider, Lets say if we have many tools in that scenario directly selecting best tool may not be effective so 1st selecting 3 best tool as per rules.):
      - Certain: If the tool's title or description, along with its input parameters (if required), semantically matches up to 100% and there is no ambiguity with other tools.
      - High: If the tool's title, description, and input parameters (if required) show a semantic resemblance and there is no ambiguity with other tools.
      - Low: If there is ambiguity with other tools.
      - very Low: If there is little to no match with any tool's title or description.
    - Then Finally selects best matching tool as per user intent which help in recalling user input requirements.
    - As we are passing schema , then some arguemnts has default value , for reducing tokens size refraiming llm to only return ehich are present in user input.
    - Consistent output format with key value definition.




## Results
![Find Topics](results/Screenshot%20from%202025-01-06%2015-08-53.png)

![ChatPDF](results/Screenshot%20from%202025-01-06%2015-12-45.png)

![Find Topics](results/Screenshot%20from%202025-01-06%2015-13-52.png)

![ai writer](results/Screenshot%20from%202025-01-06%2015-17-08.png)

![literature review](results/Screenshot%20from%202025-01-06%2015-18-34.png)

![extract data](results/Screenshot%20from%202025-01-06%2015-21-21.png)

![paraphraser](results/Screenshot%20from%202025-01-06%2015-22-14.png)

v![citation generator](results/Screenshot%20from%202025-01-06%2015-23-06.png)

![academic ai detector](results/Screenshot%20from%202025-01-06%2015-25-21.png)

![pdf_to_video](results/Screenshot%20from%202025-01-06%2015-26-00.png)






## Run

Go to GENAI
1. install:
   ```bash
   pip install -r requirements.txt

2. Run:
   ```bashy
   streamlit run tool_sel_app.py

3. Access Url


## Experiments
check
```bash
Research/experiments.ipynb

