from RAG import retrieval,parameters,utils
import streamlit as st
import asyncio
from typing import Dict

# Initialize the new pipeline components
model = utils.GenResponse(api_key=parameters.GEMINI_KEY, base_url=parameters.GEMINI_BASE_URL)
retrieval_pipe = retrieval.RetrievalPipeline()

def main():
    st.set_page_config(page_title="Chat with PDF Bot", layout="wide")
    
    st.sidebar.title("Upload PDF")
    uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")
    
    # Initialize session state variables
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "model" not in st.session_state:
        st.session_state.model = model
    if "retrieval" not in st.session_state:
        st.session_state.retrieval = retrieval_pipe
    
    # Process the uploaded PDF
    if uploaded_file is not None:
        with st.sidebar:
            st.write("Processing PDF...")
            try:
                # Save the uploaded file temporarily
                pdf_path = f"temp_{uploaded_file.name}"
                with open(pdf_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Extract text from the PDF
                text = asyncio.run(retrieval.convert_document_to_markdown(pdf_path))
                # Create chunks
                df = asyncio.run(retrieval.process_and_save_chunks(text, "train_data.xlsx"))

                # Create vector database
                st.session_state.retrieval.train(train=True)

                if not isinstance(df, dict):
                    st.success("PDF processed successfully! You can now chat with the bot.")
                else:
                    st.error("Failed to process the PDF. Please try again.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    
    st.title("Chat with PDF Bot")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**Bot:** {message['content']}")
    
    # User input for chat
    user_input = st.text_input("Enter your query:", key="user_input")
    
    # Handle user input and get bot response
    if user_input and st.session_state.model:
        # Add user input to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Get bot response
        response_container = st.empty()
        bot_response = ""
        
        async def get_response():
            nonlocal bot_response
            try:
                # Run retrieval and query expansion pipeline

                # selects only last 3 turn 
                if len(st.session_state.chat_history)>6:
                    st.session_state.chat_history = st.session_state.chat_history[-6:]
                chunks, rephrased_query, system = await utils.retrieval_with_query_expansion(
                    user_message=user_input,
                    prev_conversation=st.session_state.chat_history,
                    retrieval=st.session_state.retrieval,
                    llm_handler=st.session_state.model
                )
                
                # Get response from the model
                response = await st.session_state.model.get_response(
                    system=system,
                    model_id='gemini-1.5-flash',
                    query=user_input,
                    chat_history=st.session_state.chat_history,
                    temperature=0.5,
                    max_tokens=2000
                )
                
                if isinstance(response, Dict):
                    raise Exception(response)
                
                bot_response = response.choices[0].message.content.replace("```html", "").replace("```", "")
                
                # Add assistant response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
                
                # response
                response_container.markdown(f"**Bot:** {bot_response}")
            except Exception as e:
                response_container.markdown(f"**Bot:** Facing some issues: {e}")
        
        asyncio.run(get_response())

if __name__ == "__main__":
    main()