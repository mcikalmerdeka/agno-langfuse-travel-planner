"""Critique agent (manager) for reviewing travel plans."""
from textwrap import dedent
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from core.schemas import CritiqueResult

# Critique Agent
critique_agent = Agent(
    id="critique-agent",
    name="Manager - Travel Plan Reviewer",
    role="Manager who reviews and approves travel plans",
    description="You are a manager who evaluates travel plans for quality and completeness before final approval.",
    instructions=dedent("""\
        You are reviewing a travel plan prepared by your team lead (itinerary planner)
        The team lead has already synthesized research from the team (destination, hotel, activities researchers)
        Your role is to provide managerial-level feedback:
        
        CURRENT REVIEW STATUS:
        - Review iteration: {revision_iteration}
        - Previous feedback given: {manager_feedback}
        
        Evaluate the plan for:
        1. Completeness - Does it cover all essential aspects?
        2. Coherence - Does the itinerary flow logically?
        3. Practicality - Are activities realistic within the timeframe?
        4. Value - Does it align with the budget and traveler preferences?
        
        Decision criteria:
        - On FIRST review (iteration 0): Be thorough but constructive. Approve if solid, or request specific improvements
        - On SECOND review (iteration 1): Be more lenient and approve if reasonably good
        
        When requesting revisions:
        - Focus on how the REPORT should be improved (structure, clarity, completeness)
        - Don't ask for new research - work with existing team data 
        - Give specific, actionable feedback the team lead can implement
    """),
    model=OpenAIChat(id="gpt-4.1-nano"),  # Using more capable model for managerial-level critique
    output_schema=CritiqueResult,
    # Enable session state for tracking review iterations and feedback
    session_state={
        "revision_iteration": 0,
        "manager_feedback": "No feedback yet",
        "is_approved": False,
    },
    add_session_state_to_context=True,
    markdown=True,
)

