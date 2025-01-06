from typing import List, Dict, Union, Any, Optional,AsyncGenerator
from CustomException import handle_exception
from RAG import parameters,retrieval
import asyncio
import re
import json
from openai import AsyncOpenAI
import google.generativeai as genai

# meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo
# "https://api.deepinfra.com/v1/openai"

genai.configure(api_key=parameters.GEMINI_KEY)

class GenResponse:
    # default model ID
    DEFAULT_MODEL_ID = "meta-llama/Llama-3.2-3B-Instruct"

    def __init__(self, api_key: str,base_url : str):
        if not api_key or not isinstance(api_key, str):
            raise ValueError("API key is required and must be a string.")

        if not base_url or not isinstance(base_url, str):
            raise ValueError("Base Url is required and must be a string.")

        self.key = api_key
        self.client = AsyncOpenAI(
            api_key=self.key,
            base_url = base_url,
        )

    async def get_response(
        self,
        query: str,
        system: str,
        chat_history: Optional[List[Dict]] = None,
        model_id: Optional[str] = DEFAULT_MODEL_ID,
        temperature: float = 0.5,
        max_tokens: int = 500,
        top_p: float = 0.95,
        top_k: int = 500,
        frequency_penalty: float = 0,
        presence_penalty: float = 0,
        stop: Optional[List[str]] = None,
        response_format: Optional[Dict] = None,
        tools: Optional[List[Dict]] = None,
    ) -> Union[str, Dict[str, Any]]:

        # required inputs
        if not query or not isinstance(query, str):
            raise ValueError("Query is required and must be a string.")
        if not system or not isinstance(system, str):
            raise ValueError("System is required and must be a string.")
        if chat_history is not None and not isinstance(chat_history, list):
            raise TypeError("Chat history must be a list of dictionaries.")

        # chat history if not provided
        if chat_history is None:
            chat_history = []


        messages = [
            {"role": "system", "content": system},
            *chat_history,
            {"role": "user", "content": query},
        ]

        try:

            response = await self.client.chat.completions.create(
                model=model_id,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                response_format=response_format,
                messages=messages,
            )

            return response



        except Exception as e:
          error = await handle_exception(e)
          return error

    async def get_stream_response(
        self,
        query: str,
        system: str,
        chat_history: Optional[List[Dict]] = None,
        model_id: Optional[str] = DEFAULT_MODEL_ID,
        temperature: float = 0.5,
        max_tokens: int = 500,
        top_p: float = 0.95,
        top_k: int = 1000,
        stop: Optional[List[str]] = None,
        response_format: Optional[Dict] = None,
    ) -> AsyncGenerator:

        # required inputs
        if not query or not isinstance(query, str):
            raise ValueError("Query is required and must be a string.")
        if not system or not isinstance(system, str):
            raise ValueError("System is required and must be a string.")
        if chat_history is not None and not isinstance(chat_history, list):
            raise TypeError("Chat history must be a list of dictionaries.")

        # chat history if not provided
        if chat_history is None:
            chat_history = []


        messages = [
            {"role": "system", "content": system},
            *chat_history,
            {"role": "user", "content": query},
        ]

        try:

            response = await self.client.chat.completions.create(
                model=model_id,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                messages=messages,
                stream=True,
            )

            full_content = ''
            async for event in response:
              if event.choices[0].finish_reason:
                print(event.choices[0].finish_reason)
                yield full_content

              else:
                print(event.choices[0].delta.content)
                full_content += event.choices[0].delta.content

                yield event.choices[0].delta.content


        except Exception as e:
          error = await handle_exception(e)
          yield error

    async def format_sse(self,data: str, event: Optional[str] = None) -> str:
      """Formats the data into a Server-Sent Events (SSE) format.

      Args:
        data (str): The data to be formatted.
        event (Optional[str]): The event type (e.g., 'event' or 'body'). Defaults to None.

      Returns:
        str: The formatted SSE data.

      Example:
        >>> await format_sse("Hello, world!", "text")
        'event: text\ndata: "Hello, world!"\n\n'
         """
      formatted_data = f'data: {json.dumps(data)}\n\n'

      if event:
        formatted_data = f'event: {event}\n{formatted_data}'

      return formatted_data

    async def extract_xml(self,text: str, tag: str) -> str:
      """
      Extracts the content of the specified XML tag from the given text. Used for parsing structured responses
      Args:
        text (str): The text containing the XML.
        tag (str): The XML tag to extract content from.
      Returns:
        str: The content of the specified XML tag, or an empty string if the tag is not found.
      """
      match = re.search(f'<{tag}>(.*?)</{tag}>', text, re.DOTALL)
      return match.group(1) if match else None

    async def get_json(self, text: str) -> Dict:
      """
      Extracts the JSON content from the given text.
      Args:
        text (str): The text containing the JSON.
      Returns:
        Dict: The JSON content as a Python dictionary.
      """
      try:
        json_content = json.loads(text)
        return json_content
      except Exception as e:
        error = await handle_exception(e)
        return error
     

def embedding_model(user_message: str) -> List[float]:
    """
    Generates an embedding for the given user message using the Gemini text-embedding model.

    Args:
        user_message (str): The input text message to generate an embedding for.

    Returns:
        List[float]: A list of floats representing the embedding vector.
    """
    try:
        # Generate the embedding
        embedding = genai.embed_content(
            model="models/text-embedding-004",
            content=user_message
        )
        return embedding['embedding']
    except Exception as e:
        raise(str(e))


async def generative_prompt(all_chunks : List[str],system :str) -> str:
    """This function will return final system_prompt for bot,which can be directly used without any modification.

    Args:
        all_chunks (List[str]): List of chunks retrieved from vector database

    Returns:
        str: Final System Bot Prompt
    """
    if not isinstance(all_chunks,list):
        raise ValueError("all_chunks must be a string")

    if len(all_chunks)>0:
        knowledge_source = ''
        for i,doc in enumerate(all_chunks):
            knowledge_source += f"content_{i}: {doc} \n\n"
    else:
        knowledge_source = "NO DATA"

    system_prompt = system.format(knowledge_source = knowledge_source)
    return system_prompt


async def get_expanded_query(
    user_message: str,
    chat_history: List[Dict],
    llm_handler : GenResponse 
) -> str:
    """
    Asynchronously generates an expanded query based on the user message and chat history.

    It constructs a prompt using the provided parameters, sends it to the LLM, and processes the response to
    generate an expanded query. If the LLM fails to generate a valid response, the original user
    message is returned as the fallback.

    Args:
        user_message (str): The user's input message.
        chat_history (List[Dict]): The history of the conversation as a list of dictionaries.

    Returns:
        str: The expanded query in the format ``Ques : expanded_query``. If the LLM fails or
             returns an invalid response, the original user message is returned as the fallback.

    Raises:
        Any exceptions raised by the LLM or JSON parsing are caught and logged, but the function
        does not raise them further. Instead, it returns an empty string or the original message.
    """
    try:
        # Construct the prompt for query expansion

        chats = ''
        for chat in chat_history:
          if chat['role'] == 'user':
            chats += f"user: {chat['content']}\n"
          elif chat['role'] == 'assistant':
            chats += f"Bot: {chat['content']}\n"
        prompt = parameters.EXPAND_QUERY_PROMPT.format(
            prev_conv = chats,
            query = user_message
        )

        # Call the LLM to generate the expanded query
        response_text = await llm_handler.get_response(
            system = " ",
            model_id = 'gemini-1.5-flash',
            query = prompt,
            chat_history = [],
            temperature = .5,
            max_tokens = 300,
            response_format = {"type": "json_object"}
        )
        # Process the rephrased query
        if not isinstance(response_text,Dict):
          # Parse the LLM response
          response_text = await llm_handler.get_json(response_text.choices[0].message.content)
          response_text = response_text['rephrased_query']
          print(response_text)
          if isinstance(response_text, list):
            # If the response is a non-empty list, use the first item
            if response_text:
                  user_mes_expanded = response_text[0]
            else:
                  user_mes_expanded = user_message
          else:
                # If the response is a string, use it directly
                user_mes_expanded = response_text
        else:
            # If no rephrased query is returned, use the original message
            user_mes_expanded = user_message

    except Exception as e:
      error = await handle_exception(e)
      print(error)
      # Fallback to an empty string if an exception occurs
      user_mes_expanded = ""

    print("Query Expanded:\n", user_mes_expanded)

    return user_mes_expanded


import asyncio

async def retrieval_with_query_expansion(
    user_message: str,
    prev_conversation: List[Dict],
    retrieval: retrieval.RetrievalPipeline,
    llm_handler : GenResponse
) -> tuple:
    """
    Performs retrieval with query expansion to enhance search results.

    This function generates an expanded query using the user's message and conversation history,
    retrieves relevant chunks from a knowledge base using both the expanded and original queries,
    and constructs a system prompt based on the retrieved chunks.

    Args:
        user_message (str): The user's input message.
        prev_conversation (List[Dict]): The history of the conversation as a list of dictionaries.
        retrieval (RetrievalPipeline): The retrieval pipeline used to fetch chunks.

    Returns:
        tuple: A tuple containing:
            - all_chunks (List[str]): A list of unique retrieved chunks, limited to a maximum of 5.
            - expanded_query (str): The expanded query generated from the user message and chat history.
            - system_prompt (str): The final system prompt constructed from the retrieved chunks.

    Raises:
        Exception: If an error occurs during retrieval, query expansion, or prompt generation.
    """
    try:
        # Generate expanded query using the user message and conversation history
        expanded_query = await get_expanded_query(
            user_message=user_message,
            chat_history=prev_conversation,
            llm_handler = llm_handler
        )

        # Retrieve chunks using the expanded query if it is not empty
        if len(expanded_query)>0:
            retrieval_task1 = asyncio.create_task(
                retrieval.retrieve_chunks(
                    user_message=expanded_query,
                )
            )
        else:
            retrieval_task1 = None

        # Retrieve chunks using the original user message
        retrieval_task2 = asyncio.create_task(
            retrieval.retrieve_chunks(
                user_message=user_message,
            )
        )

        # Gather results from both retrieval tasks
        retrieval_results = await asyncio.gather(retrieval_task1, retrieval_task2)

        # Process results from the expanded query retrieval
        retrieved_chunks1 = []
        if retrieval_task1:
            semantic_search_result1 = retrieval_results[0]
            if 'error' not in semantic_search_result1:
                retrieved_chunks1 = semantic_search_result1

        # Process results from the original query retrieval
        semantic_search_result2 = retrieval_results[1]
        if 'error' not in semantic_search_result2:
            retrieved_chunks2 = semantic_search_result2
        else:
            retrieved_chunks2 = []

        # Combine and deduplicate chunks from both retrievals
        all_chunks = retrieved_chunks1.copy()
        for chunk in retrieved_chunks2:
            if chunk not in all_chunks:
                all_chunks.append(chunk)

        # Limit the number of chunks to 5
        if len(all_chunks) > parameters.MAX_RETRIEVE:
            all_chunks = all_chunks[:parameters.MAX_RETRIEVE]

        # Generate the final system prompt using the retrieved chunks
        system_prompt = await generative_prompt(all_chunks=all_chunks,system = parameters.SYSTEM_BOT)

        return all_chunks, expanded_query, system_prompt

    except Exception as e:
        error = await handle_exception(e)
        print(error)
        return error, error, error