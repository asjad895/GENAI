import chromadb
import pandas as pd
from CustomException import handle_exception
import RAG.utils as utils
from chonkie import LateChunker
from docling.document_converter import DocumentConverter
from typing import List, Dict, Union, Any, Optional,AsyncGenerator,Tuple


max_results = 5

class RetrievalPipeline(object):
    """
    Manages all the fuction related to retrival and vector database
    """
    class MyEmbeddingFunction(chromadb.EmbeddingFunction):
        """
        This is a custom function that generates embeddings for text data using the given model.
        """
        def __call__(self, Docs: chromadb.Documents) -> chromadb.Embeddings:
            """
            This function generates embeddings for a list of text documents using the given model.
            Args:
                Docs (chromadb.Documents): A list of text documents.
            Returns:
                chromadb.Embeddings: A list of embeddings (numerical representations) for the input text documents.
            """
            embeddings = [utils.embedding_model(chunk) for chunk in Docs]
            return embeddings

    def __init__(
            self,
            chromadb_path:str = 'chromadb/',
            train_data_path:str = 'train_data.xlsx',
            collection_name : str = 'contexts'
        ) -> None:

        self.client = chromadb.PersistentClient(path=chromadb_path)
        self.training_data_path = train_data_path
        self.collection_name = collection_name

    def train(self, train:bool = False) -> None:
        if train or not self.client.list_collections():

            self.client.get_settings().allow_reset=True

            self.client.reset()
            print("All the collections has been removed")

            excel_data = pd.read_excel(self.training_data_path)
            print(excel_data.shape)

            print(f"Starting training for {self.collection_name}")

            collection = self.client.create_collection(
                name= self.collection_name,
                embedding_function=self.MyEmbeddingFunction(),
                metadata={"hnsw:space": "cosine"}
                )
            print("Collection has been created")
            collection.add(
                documents=excel_data['chunks'].to_list(),
                ids=excel_data.index.astype(str).to_list()

                )
            print("Data has been loaded succesfully")



    async def retrieve_chunks(
            self,
            user_message : str,
            )->Tuple[str,Dict]:
        """
        """
        try:
            collection_name = self.collection_name

            vectordb = self.client.get_collection(collection_name)
            results = vectordb.query(query_texts = user_message, n_results = max_results)

            chunks = results['documents'][0]
            return chunks

        except Exception as e:
          error = await handle_exception(e)
          return error
        


async def process_and_save_chunks(text: str, df_path: str) -> pd.DataFrame:
    """
    Processes the input text using LateChunker, saves the chunks into a DataFrame,
    and exports the DataFrame to an Excel file.

    Args:
        text (str): The input text to be processed.
        df_path (str): The file path where the DataFrame will be saved as an Excel file.

    Returns:
        pd.DataFrame: A DataFrame containing the chunks in the 'chunks' column.

    Raises:
        Exception: If an error occurs during processing or saving.
    """
    try:
        # Initialize the LateChunker
        chunker = LateChunker(
            embedding_model="all-MiniLM-L6-v2",
            mode="sentence",
            chunk_size=512,
            min_sentences_per_chunk=1,
            min_characters_per_sentence=12,
            delim=['\\n', '##']
        )

        # Generate chunks 
        chunks = chunker(text)

        # Create a DataFrame 
        df = pd.DataFrame({"chunks": chunks})

        # Save the DataFrame 
        df.to_excel(df_path, index=False)

        print(f"DataFrame saved successfully at {df_path}")
        return df

    except Exception as e:
        error = await handle_exception(e)
        return error
# process_and_save_chunks(text, "train_data.xlsx")



async def convert_document_to_markdown(doc_source: str) -> str:
    """
    Converts a document (e.g., PDF) to Markdown text using DocumentConverter.

    Args:
        doc_source (str): The file path of the document to be converted.

    Returns:
        str: The converted Markdown text.

    Raises:
        FileNotFoundError: If the document file is not found.
        Exception: If any other error occurs during conversion.
    """
    try:
        # Initialize DocumentConverter and convert the document
        doc = DocumentConverter().convert(source=doc_source).document

        # Export the document to Markdown
        markdown_text = doc.export_to_markdown()

        return markdown_text

    except Exception as e:
        error = handle_exception(e)

        return error
