import streamlit as st
import asyncio
from typing import Dict
from ToolClassifier import parameters, tools, model

tool_model = model.GenResponse(
    api_key=parameters.OPENAI_KEY,
    base_url=" ",  # not usable,
    openai=True
)


def main():
    st.set_page_config(page_title="Tool Selection", layout="wide")
    st.title("Tool Selection System")
    st.write("Enter your query below:")

    query = st.text_input("Query")

    if st.button("Submit Query"):
        if query:
            st.write(f"**Query:** {query}")

        
            with st.spinner("Processing your query..."):
                try:
                    # Format system
                    system = asyncio.run(
                        tools.get_formatted_tools()
                    )
                    print(system)

                    # Run the async function in the event loop
                    tool_sel = asyncio.run(
                        tool_model.get_response(
                            system=system,
                            chat_history=[],
                            query=query,
                            model_id=parameters.MODEL_ID,
                            temperature=parameters.TEMPERATURE,
                            max_tokens=parameters.MAX_TOKENS,
                            response_format={"type": "json_object"},
                        )
                    )

                    # Error case
                    if isinstance(tool_sel, Dict):
                        st.error(f"Error: {tool_sel}")
                    else:
                        # Display the content of the response
                        response = asyncio.run(tool_model.get_json(tool_sel.choices[0].message.content))
                        if 'error' not in response:
                            st.write(f"**Tool:** {response.get('tool')}")
                            st.write(f"**Params:** {response.get('arguments')}")
                        # print(response)
                        st.write(f"**Response Content:** {tool_sel.choices[0].message.content}")

                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a query before submitting.")


if __name__ == "__main__":
    main()