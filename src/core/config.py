"""Configuration and initialization for Langfuse and OpenLIT."""
from dotenv import load_dotenv
from langfuse import get_client
import openlit


# Load environment variables
load_dotenv()

# Initialize Langfuse client
langfuse = get_client()

# Verify connection
if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")

# Initialize OpenLIT instrumentation
openlit.init(tracer=langfuse._otel_tracer, disable_batch=True)

