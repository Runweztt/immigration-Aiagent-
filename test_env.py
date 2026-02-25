import os
import sys
from dotenv import load_dotenv

def test():
    print("Python version:", sys.version)
    print("CWD:", os.getcwd())
    
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    print("API Key present:", bool(api_key))
    if api_key:
        print("API Key prefix:", api_key[:10])
        print("API Key length:", len(api_key))
    
    print("LLM Provider:", os.getenv("LLM_PROVIDER"))
    
    try:
        import crewai
        print("CrewAI imported successfully")
    except Exception as e:
        print("Error importing CrewAI:", e)
        
    try:
        import langchain
        print("LangChain imported successfully")
    except Exception as e:
        print("Error importing LangChain:", e)

if __name__ == "__main__":
    test()
