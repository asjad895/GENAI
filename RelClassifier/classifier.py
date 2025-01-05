import RelClassifier.parameters as parameters
import RelClassifier.utils as utils
 
from typing import List, Dict

async def classify_paper(
    query: str,
    system: str,
    title :str,
    abstract: str,
    llm_handler : utils.GenResponse ,
    )->Dict:

    # system formatting
    system = system.format(
      title = title,
      abstract = abstract,
    )
    response = await llm_handler.get_response(
        system = system,
        query = f"<query>{query}</query>",
        chat_history = [],
        temperature = parameters.TEMPERATURE,
        max_tokens = parameters.MAX_TOKENS,
        response_format = {"type": "json"}
        )

    if isinstance(response,Dict):
      return response
    # json validate
    json_response = await llm_handler.get_json(response.choices[0].message.content)
    # try with feedback
    if 'error' in json_response:
       print("Feedback")
       feedback = f"This is json parsing error in your last response :\n{json_response['error']}.\nLast Response :\n{response.choices[0].message.content}.\n Correct it and make sure all the keys and values are present in valid json format."
       chat_history = [
           {"role": "system", "content": system},
          {"role": "user", "content": f"<query>{query}</query>"},
          {"role": "assistant", "content": response.choices[0].message.content}
           ]
       response = await llm_handler.get_response(
          system = system,
          query = f"<feedback>{feedback}</feedback>",
          chat_history = chat_history,
          temperature = .5,
          max_tokens = 1000,
          response_format = {"type": "json"}
          )
       json_response = await llm_handler.get_json(response.choices[0].message.content)
    return json_response
