from typing import List, Dict, Union, Any, Optional
from CustomException import handle_exception
import RAG.parameters as parameters
import asyncio


def embedding_model(user_message : str) -> List[float]:
  embedding = genai.embed_content(
        model="models/text-embedding-004",
        content=user_message
        )
  return embedding['embedding']


async def generative_prompt(all_chunks : List[str]) -> str:
    """This function will return final system_prompt for bot,which can be directly used without any modification.

    Args:
        all_chunks (List[str]): List of chunks retrieved from vector database

    Returns:
        str: Final System Bot Prompt
    """
    if not isinstance(all_chunks,str):
        raise ValueError("all_chunks must be a string")

    if len(all_chunks)>0:
        knowledge_source = ''
        for i,doc in enumerate(all_chunks):
            knowledge_source += f"source {i}: {doc} \n\n"
    else:
        knowledge_source = "NO DATA"

    system_prompt = system_prompt.format(knowledge_source = knowledge_source)
    return system_prompt


async def get_expanded_query(
    user_message: str,
    chat_history: List[Dict],
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
        prompt = parameters.EXPAND_QUERY_PROMPT

        # Call the LLM to generate the expanded query
        response_text = await get_expanded_query(
            user_message = user_message,
            chat_history = chat_history,
        )

        # Parse the LLM response

        # Process the rephrased query
        if response_text:
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
      # Fallback to an empty string if an exception occurs
      user_mes_expanded = ""

    print("Query Expanded:\n", user_mes_expanded)
    return user_mes_expanded


async def retrieval_with_query_expansion(
    user_message: str,
    prev_conversation: List[Dict],
    retrieval,
    top1_chunk: Optional[List[str]] = None,
) -> tuple:
    """
    Perform retrieval with query expansion to enhance search results.

    This function takes a user message, previous conversation history, and optional parameters
    to generate an expanded query. It then retrieves relevant chunks from a knowledge base
    using both the expanded and original queries. Finally, it constructs a system prompt
    based on the retrieved chunks.

    Args:
        user_message (str): The user's input message.
        prev_conversation (List[Dict]): The history of the conversation as a list of dictionaries.

    Returns:
        tuple: A tuple containing:
            - all_chunks (List[str]): A list of unique retrieved chunks.
            - expanded_query (str): The expanded query generated from the user message.
            - system_prompt (str): The final system prompt constructed from the retrieved chunks.
    """
    if top1_chunk is None:
        top1_chunk = ['']

    # Generate expanded query using the user message and conversation history
    expanded_query = await get_expanded_query(
        user_message=user_message,
        chat_history=prev_conversation,
    )

    # Retrieve chunks using the expanded query if it is not empty
    if expanded_query:
        expanded_query_embedding = await embedding_model(expanded_query)
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
            retrieved_chunks1 = semantic_search_result1['documents'][0] + top1_chunk

    # Process results from the original query retrieval
    semantic_search_result2 = retrieval_results[1]
    if 'error' not in semantic_search_result2:
        retrieved_chunks2 = semantic_search_result2['documents'][0]
    else:
        retrieved_chunks2 = []

    # Combine and deduplicate chunks from both retrievals
    all_chunks = retrieved_chunks1.copy()
    for i, chunk in enumerate(retrieved_chunks2):
        if chunk not in all_chunks:
            all_chunks.append(chunk)

    # Limit the number of chunks to 5
    if len(all_chunks) > 5:
        all_chunks = all_chunks[:5]

    # Generate the final system prompt using the retrieved chunks
    system_prompt = await generative_prompt(all_chunks=all_chunks)

    return all_chunks, expanded_query, system_prompt