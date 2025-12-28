"""Utility functions for agent observation and wrapping."""
from agno.agent import Agent
from langfuse import observe

# Function to make an agent observable for Langfuse tracing
def make_agent_observable(agent: Agent, agent_name: str) -> None:
    """
    Wraps an agent's run and arun methods with Langfuse @observe decorator.
    
    This function uses 'Monkey Patching' to dynamically modify the agent's behavior
    at runtime without changing its source code class definition.
    """
    
    # 1. Capture the ORIGINAL run method before we modify it.
    #    We store this function reference so we can call it later.
    original_run_method = agent.run
    
    # 2. Define a new wrapper function that adds the @observe decorator.
    #    This wrapper acts as a "middleman" that connects Langfuse tracing.
    @observe(as_type="agent", name=agent_name)
    def run_with_observation(*args, **kwargs):
        # IMPORTANT: We call the original method exactly ONCE here.
        # This ensures the agent performs its task only one time.
        # The return value is passed back up through the wrapper.
        
        # NOTE: We need this synchronous wrapper because the 'Manager' (critique_agent)
        # in workflows/critique_logic.py is called using .run() inside a sync step.
        return original_run_method(*args, **kwargs)
    
    # 3. Replace the agent's .run method with our new observed wrapper.
    #    Now, whenever agent.run() is called, run_with_observation() runs instead.
    agent.run = run_with_observation  # type: ignore[method-assign]
    
    # Repeat the same process for the asynchronous method (.arun)
    original_arun_method = agent.arun
    
    @observe(as_type="agent", name=agent_name)
    async def arun_with_observation(*args, **kwargs):
        # IMPORTANT: Original async method is awaited exactly ONCE.
        # No double-execution happens here.
        return await original_arun_method(*args, **kwargs)
    
    agent.arun = arun_with_observation  # type: ignore[method-assign]

