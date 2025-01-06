from ToolClassifier import parameters

chat_with_pdf = {
  "type": "function",
  "function": {
    "name": "chat_with_pdf",
    "description": """This tool is for Interact with a PDF file to perform various operations such as answering questions, summarizing sections, explaining highlighted text, recommending related papers, or taking notes.""",
    "parameters": {
      "type": "object",
      "properties": {
        "pdf_file_url": {
          "type": "string",
          "description": "The URL or path to the PDF file. Required to perform any operation on the PDF."
        },
        "query": {
          "type": "string",
          "description": "A question or search query to find specific answers or sections in the PDF. Can be left blank if performing a general operation."
        },
        "operation": {
          "type": "string",
          "enum": ["get_citation_answers", "get_summary", "highlight_explanation", "get_related_papers", "take_notes"],
          "description": "The specific operation to perform on the PDF, such as answering questions, summarizing, or finding related papers."
        },
        "section": {
          "type": "string",
          "description": "The specific section of the PDF to target (e.g., 'Introduction', 'Methods', 'Conclusion'). Leave blank for the entire document."
        },
        "highlighted_text": {
          "type": "string",
          "description": "Specific text from the PDF to get a simplified explanation or find related papers. Required for 'highlight_explanation' and 'get_related_papers' operations."
        },
        "language": {
          "type": "string",
          "description": "The language in which the response should be provided. Default is 'English'. Supports 75+ languages.",
          "default": "English"
        },
        "note": {
          "type": "string",
          "description": "Text for the note to be added. Used in the 'take_notes' operation to store custom annotations."
        },
        "output_format": {
          "type": "string",
          "enum": ["plain_text", "json", "markdown"],
          "description": "The desired format for the output of the operation.",
          "default": "plain_text"
        },
        "citation_style": {
          "type": "string",
          "enum": ["APA", "MLA", "Chicago", "Harvard"],
          "description": "The citation style for answers backed by citations. Used in 'get_citation_answers' operation.",
          "default": "APA"
        },
        "related_paper_limit": {
          "type": "integer",
          "description": "The maximum number of related papers to fetch. Only used in 'get_related_papers' operation.",
          "default": 5
        }
      },
      # "required": ["pdf_file_url"]
    }
  },
  "strict" :True
}

ai_writer = {
    "type": "function",
    "function": {
        "name": "ai_writer",
        "description": """An AI-powered tool to assist in writing research papers with confidence by providing citation discovery, text autocompletion, note management, and export functionality.
User's can create new notebook, edit old and do a lot of ai powered assistant within notebook in realtime.""",
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "description": "The type of operation to perform. Options include 'find_citations', 'autocomplete', 'save_notes', 'export_paper'.",
                    "enum": ["find_citations", "autocomplete", "save_notes", "export_paper"]
                },
                "query": {
                    "type": "string",
                    "description": "The specific query for citation discovery or text completion. For example, a topic, phrase, or context for writing."
                },
                "citation_source": {
                    "type": "string",
                    "description": "Optional. A specific citation database or source for finding references. If omitted, the default SciSpace database is used.",
                    "default": "SciSpace"
                },
                "note_content": {
                    "type": "string",
                    "description": "Optional. Content of the note to save. Required for 'save_notes' operation.",
                },
                "file_format": {
                    "type": "string",
                    "description": "Optional. Format to export the paper in. Required for 'export_paper' operation. Supported formats: 'PDF', 'DOCX'.",
                    "enum": ["PDF", "DOCX"]
                },
                "output_format": {
                    "type": "string",
                    "description": "Optional. Format of the response output. Options include 'text', 'json', 'markdown'. Default is 'text'.",
                    "enum": ["text", "json", "markdown"],
                    "default": "text"
                },
                "language": {
                    "type": "string",
                    "description": "Optional. Language for autocomplete suggestions or saved notes. Default is English.",
                    "default": "English"
                }
            },
            "required": ["operation"]
        }
    }
}

literature_review = {
    "type": "function",
    "function": {
        "name": "literature_review",
        "description": "Discover new research papers and perform a quick AI-powered literature survey with semantic similarity, concise reviews, and customizable features in your own language.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The research topic or keywords or concise search query for discovering and reviewing relevant papers."
                },
                "language": {
                    "type": "string",
                    "description": "Language for the review output. Default is English.",
                    "default": "English"
                }
            },
            "required": ["query"]
        }
    }
}

find_topics = {
    "type": "function",
    "function": {
        "name": "find_topics",
        "description": "Extract insightful topics from research papers and get grounded, summarized answers for top semantically similar topics in multiple languages.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The research topic or keywords to extract and summarize related topics."
                },
            },
            "required": ["query"]
        }
    }
}

extract_data = {
    "type": "function",
    "function": {
        "name": "extract_data",
        "description": "This Tool Extract summaries, conclusions, and findings from multiple research papers and provide them in a structured format. Features :Semantic Search, Extract & Compare information,Citation-backed insights\
        multiple Language support, Paper Summary, Export in multiple formats",
        "parameters": {
            "type": "object",
            "properties": {
                "files": {
                    "type": "list",
                    "description": "Optional,The list of files url path"
                },
            }
        }
    }
}


paraphraser = {
    "type": "function",
    "function": {
        "name": "paraphraser",
        "description": "Paraphrase input text into different tones or personas with grammatical correctness in multiple languages.",
        "parameters": {
            "type": "object",
            "properties": {
                "input_text": {
                    "type": "string",
                    "description": "The text to be paraphrased."
                },
                "tone": {
                    "type": "string",
                    "description": "The tone or persona for paraphrasing, such as 'Academic', 'Fluent', 'Formal', 'Creative', etc."
                }
            },
        }
    }
}

citation_generator= {
    "type": "function",
    "function": {
        "name": "citation_generator",
        "description": "Generate citations in various formats (APA, MLA, and 2300+ styles) from a title or URL and export them in BibTeX format.",
        "parameters": {
            "type": "object",
            "properties": {
                "input_data": {
                    "type": "string",
                    "description": "The title or URL of the source to generate the citation."
                },
            },
            "required": ["input_data"]
        }
    }
}


academic_ai_detector=  {
    "type": "function",
    "function": {
        "name": "academic_ai_detector",
        "description": "Detect AI-generated content (e.g., GPT-4, ChatGPT, Jasper) in scholarly documents or text input.",
        "parameters": {
            "type": "object",
            "properties": {
                "input_data": {
                    "type": "string",
                    "description": "The input data to analyze for AI-generated content. Can be a URL to a PDF file or plain text."
                },
            },
        }
    }
}

pdf_to_video = {
    "type": "function",
    "function": {
        "name": "pdf_to_video",
        "description": "Convert research PDFs into engaging videos with voice-over, subtitles, and transitions.",
        "parameters": {
            "type": "object",
            "properties": {
                "pdf_url": {
                    "type": "string",
                    "description": "The URL or file path of the research PDF to convert into a video."
                },
                
            },
            "required": ["pdf_url"]
        }
    }
}


async def get_formatted_tools()->str:
    tools = [
       chat_with_pdf,ai_writer,find_topics,pdf_to_video,academic_ai_detector,citation_generator,paraphraser,
       extract_data,literature_review,ai_writer]
    tools_str = ''
    
    for tool in tools:
        tools_str += f"title: {tool['function']['name']}\nDescription: {tool['function']['description']}\nparameters: {tool['function']['parameters']}\n\n"
        # print(tools_str)

    system = parameters.SYSTEM.format(
        tools_all = tools_str
    )

    return system