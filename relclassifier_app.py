import streamlit as st
import asyncio
from RelClassifier import utils,classifier  
import RelClassifier.parameters as parameters
import RelClassifier.utils as utils
 

DEEPINFRA_TOKEN = parameters.DEEPINFRA_TOKEN
DEEP_INFRA_BASE_URL = parameters.DEEP_INFRA_BASE_URL
system = parameters.SYSTEM
# Initialize the model
model = utils.GenResponse(api_key=DEEPINFRA_TOKEN, base_url=DEEP_INFRA_BASE_URL)

def main():
    st.set_page_config(page_title="Research Paper Relevance Classification", layout="wide")
    
    st.title("Research Paper Relevance Classification with AI")
    
    # User inputs
    st.header("Input Parameters")
    query = st.text_input("Enter your query:", placeholder="e.g., What is tabular chain of thought?")
    title = st.text_input("Enter the paper title:", placeholder="e.g., Tab-CoT: Zero-shot Tabular Chain of Thought")
    abstract = st.text_area("Enter the paper abstract:", placeholder="Paste the abstract here...")
    
    
    if st.button("Classify Paper"):
        if query and title and abstract:
            with st.spinner("Classifying the paper..."):
                try:
                    
                    # Classify
                    result = asyncio.run(
                        classifier.classify_paper(
                            query=query,
                            system=system,
                            title=title,
                            abstract=abstract,
                            llm_handler=model
                        )
                    )
                    
                    # result
                    st.success("Classification completed!")
                    st.subheader("Analysis")
                    st.write(result['analysis'])
                    
                    st.subheader("Justification")
                    st.write(result['justification'])
                    
                    st.subheader("Relevance Level")
                    st.write(result['relevance_level'])
                
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please fill in all the fields (query, title, and abstract).")


if __name__ == "__main__":
    main()