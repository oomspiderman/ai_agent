import os
from dotenv import load_dotenv
from google import genai
import sys

# sys.argv
# The list of command line arguments passed to a Python script. 
# argv[0] is the script name (it is operating system dependent whether this is a full pathname or not). 
# If the command was executed using the -c command line option to the interpreter, argv[0] is set to the string '-c'. 
# If no script name was passed to the Python interpreter, argv[0] is the empty string.
# To loop over the standard input, or the list of files given on the command line, see the fileinput module.
# See also sys.orig_argv.
# Note On Unix, command line arguments are passed by bytes from OS. Python decodes them with filesystem encoding and 
# “surrogateescape” error handler. When you need original bytes, you can get it by [os.fsencode(arg) for arg in sys.argv].

if len(sys.argv) < 2:
    print("Error: prompt is required.")
    sys.exit(1)
else:
    print(f"Found the prompt: {sys.argv[1]}")

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=sys.argv[1]
)
print(response.text)
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
