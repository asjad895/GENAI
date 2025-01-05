import google.generativeai as genai
import RAG.parameters as parameters
import CustomException
from google.generativeai import caching
import datetime
from typing import List,Dict,Union,Tuple,Generator,AsyncGenerator
import io
import httpx
import io
import httpx
import datetime

async def setup_model_with_pdf(pdf_path):
    """
    Sets up a generative model with a PDF file as context.

    Args:
        pdf_path (str): Path to the PDF file (can be a URL or local path).
    Returns:
        genai.GenerativeModel: Configured generative model with the PDF as context.
    """
    try:
        genai.configure(api_key=parameters.GEMINI_KEY)
        document = genai.upload_file(
            pdf_path
        )
        print(genai.list_models())
        cache = caching.CachedContent.create(
            model = parameters.MODEL,
            display_name='papers',
            system_instruction=parameters.SYSTEM_BOT,
            contents=[document],
            ttl=datetime.timedelta(minutes=40),
        )
        
        # Create the generative model from the cached content
        model = genai.GenerativeModel.from_cached_content(
            cached_content=cache,
            generation_config=genai.GenerationConfig(
                max_output_tokens = parameters.MAX_TOKENS,
                temperature = parameters.TEMPERATURE,
            )
        )
        
        return model
    
    except Exception as e:
        error = await CustomException.handle_exception(e)
        return error


async def get_chat_response(chat_history :List, user_input :str,chat:object ,model)->AsyncGenerator:
    """
    Generates a response from the chat model based on the provided chat history and user input.

    Args:
        chat_history (list): A list of dictionaries representing the chat history. Each dictionary should have 
                             'role' (either 'user' or 'model') and 'parts' (the message content) as keys.
        user_input (str): The user's input message to be sent to the chat model.

    Returns:
        str: The model's response to the user input.
    """
    try:
        if not chat:
            chat = model.start_chat(history=chat_history)
        
        response = chat.send_message(user_input, stream=True)
        
        response_text = ""
        for chunk in response:
            response_text += chunk.text
            yield chunk

        chat_history.append({"role": "user", "parts": user_input})
        chat_history.append({"role": "model", "parts": response_text})
        
        yield {
            'chat_history':chat_history,
            'chat':chat
        }
    
    except Exception as e:
        error = await CustomException.handle_exception(e)

        yield error
