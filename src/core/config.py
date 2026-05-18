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
# Handle API differences across openlit versions (some deployments omit 'tracer' support)
try:
    openlit.init(tracer=langfuse._otel_tracer, disable_batch=True)
except TypeError:
    # Fallback for older openlit versions that don't accept 'tracer'
    openlit.init(disable_batch=True)

