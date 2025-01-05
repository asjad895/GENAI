from typing import List, Dict, Union, Any, Optional,AsyncGenerator
from openai import AsyncOpenAI
import json
import re
from CustomException import handle_exception


# meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo
# "https://api.deepinfra.com/v1/openai"


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
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=stop,
                response_format=response_format,
                tools=tools,
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