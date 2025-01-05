from RAG import response,retrieval
import streamlit as st 
import asyncio


retrieval_pipe = retrieval.RetrievalPipeline(

)
def main():
    st.set_page_config(page_title="Chat with PDF Bot", layout="wide")
    
    st.sidebar.title("Upload PDF")
    uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")
    
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "model" not in st.session_state:
        st.session_state.model = None
    if "chat" not in st.session_state:
        st.session_state.chat = None
    
    # Process the uploaded PDF
    if uploaded_file is not None:
        with st.sidebar:
            st.write("Processing PDF...")
            try:
                # Save 
                pdf_path = f"temp_{uploaded_file.name}"
                with open(pdf_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # extract contents
                text = asyncio.run(retrieval.convert_document_to_markdown(pdf_path))
                # create chunks
                df = asyncio.run(retrieval.process_and_save_chunks(text, "train_data.xlsx"))

                # create vector db
                retrieval_pipe.train(train=True)

                if not isinstance(df,dict):
                    # st.session_state.model = model
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
                st.markdown(f"**You:** {message['parts']}")
            else:
                st.markdown(f"**Bot:** {message['parts']}")
    
    # User input for chat
    user_input = st.text_input("Enter your query:", key="user_input")
    
    # Handle user input and get bot response
    if user_input and st.session_state.model:
        # Add user input to chat history
        st.session_state.chat_history.append({"role": "user", "parts": user_input})
        
        # Get bot response in streaming format
        response_container = st.empty()
        bot_response = ""
        
        # Use the async generator to stream the response
        async def stream_response():
            async for chunk in response.get_chat_response(
                chat_history=st.session_state.chat_history,
                user_input=user_input,
                chat=st.session_state.chat,
                model=st.session_state.model
            ):
                if isinstance(chunk, str):
                    bot_response += chunk
                    response_container.markdown(f"**Bot:** {bot_response}")
                elif isinstance(chunk, dict) and "chat_history" in chunk:
                    st.session_state.chat_history = chunk["chat_history"]
                    st.session_state.chat = chunk['chat']

                else:
                    response_container.markdown(f"**Bot:** Facing some issues....")
        

        asyncio.run(stream_response())


if __name__ == "__main__":
    main()