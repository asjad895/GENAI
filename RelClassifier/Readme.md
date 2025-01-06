### Propmt engineering Technique used:

1. Role prompting, or persona prompting.

Giving clear role and backstory or persona helps llm to be consistent and get best response .
Given role : Expert in Analysis of Research paper

2. SimToM (Simulated Theory of Mind)

We can use emotion techniques to constrain model which i have used like "respond will be use by automated system" for constraining json output.

3. RaR,R2e

read again and rephrase before analysis so that it should analyze input in multiple aspect before jumping next step.

4. Cot

Step by step reasoning with proper guidelines to be consistent and expected behavior.
Query Decomposition and Analysis:

As Analyzing First understanding user intent , multi aspect, looking for verarching topics which will translate topics to broader aspect, finding keywords , topic. This is how a human will also analyze.

Title Relevance Analysis:

After query Analyzing title whatever we have found in query analysis we have to find degree of alignment(no fix).
Give a score which will eventually at the end help llm to give final relevance score. In Reasoning Giving score on multiple subject then at the end give relative score will increase reasoning utility.

Abstract Relevance Analysis:

In same as title but look for little more related content which user is looking which helps whether this paper will help to answer larger topic of user intent.

Rule for Score 

<relevance_level>

1 (Low Relevance): The paper title and abstract have no direct connection to the user query. The topic, keywords, and context do not align.

2 (Moderate Relevance): The paper title or abstract contains some related keywords or concepts, but the connection is weak or tangential. The paper may touch on a broader topic without addressing the specific query.

3 (High Relevance): The paper title and abstract align well with the user query. The topic, keywords, and context are closely related, and the paper likely provides useful insights or answers to the query.

4 (Very High Relevance): The paper title and abstract are highly aligned with the user query. The topic, keywords, and context are directly relevant, and the paper is likely to provide a comprehensive answer or solution to the query.

</relevance_level>

5. Analysis -> relevance -> justification

First it should analyze as per guide lines , then give relevance as per analysis score , then justification. this will maintain coherence and improve reasoning performance.

6. clear Input, Output, Task

using xml tag for clear separation between inputs , json output for consistent output. Then Defining Concise and target goal/Task which helps model why they have to do  a lot of things.

7. feedback handling

If Llm will not respond in json then again pass feedback with parsing error to rectify previous issues in output without any changes json data.

8. Zero -shot 

As Llama3.2 has been trained on scientific Data.https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/MODEL_CARD.md



## Result
![Alt text](results/Screenshot%20from%202025-01-06%2011-27-51.png)
![Alt text](results/Screenshot%20from%202025-01-06%2011-30-50.png)
![Alt text](results/Screenshot%20from%202025-01-06%2011-33-12.png)
![Alt text](results/Screenshot%20from%202025-01-06%2011-54-07.png)
![Alt text](results/Screenshot%20from%202025-01-06%2011-55-59.png)
![Alt text](results/Screenshot%20from%202025-01-06%2011-56-56.png)



## Run

Go to GENAI
1. install:
   ```bash
   pip install -r requirements.txt

2. Run:
   ```bash
   streamlit run relclassifier_app.py

3. Access Url
