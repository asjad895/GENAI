## Pipeline Overview

### Indexing Pipeline
1. **Load PDF**: Load the PDF document for processing.  
2. **Extract Markdown Content**: Extract structured markdown content from the PDF.  
3. **Create Chunks**: Split the extracted content into smaller, manageable chunks.  
4. **Create Vectors**: Convert the chunks into vector representations using an embedding model.  
5. **Store in ChromaDB**: Save the vectors in ChromaDB for efficient retrieval.  

### Generation Pipeline
1. **Query Input**: Receive a user query.  
2. **Check Chat History**: If chat history exists, rephrase the query using an LLM for better context understanding.  
3. **Generate Retrieval Queries**: Create new queries optimized for retrieval.  
4. **Concurrent Search**: Perform a concurrent search in the vector database (ChromaDB) using the generated queries.  
5. **Retrieve Unique Chunks**: Fetch unique and relevant chunks from the database.  
6. **Create System Prompt**: Construct a system prompt by incorporating the retrieved chunks as context.  
7. **Generate Response**: Use the LLM to generate a response to the original query based on the context.  



## Notes:

first time i am using google generative ai. so not aware too much.

I am going with the standard RAG pipeline.

- **Drawback of the Current Method:**
  - Loss of image content from the PDF.
  - Retention of tables and other elements.

- **Alternative Approach:**
  - Directly upload the PDF and use the `genai.generate_content` function for chat interactions.

- **Considerations:**
  - Potential increase in token count when using direct PDF upload.
  - If token count is not an issue, this approach can be adopted.

  - As per google documentation , prompts and PDFs can be directly input into `genai.generate_content`.
  - This could streamline the process and eliminate the need for the current pipeline.

