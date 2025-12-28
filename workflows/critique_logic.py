"""Custom function steps for critique and revision logic."""
from agno.workflow import Step
from agno.workflow.types import StepInput, StepOutput
from agno.run import RunContext
from agents.critique_agent import critique_agent
from core.schemas import CritiqueResult

# Function to critique and revise the presented travel plan
def critique_and_revise(step_input: StepInput, run_context: RunContext) -> StepOutput:  # type: ignore[arg-type]
    """
    Manager reviews the itinerary and provides feedback.
    Updates session_state with critique results for the team lead to access.
    """
    # Ensure session_state is initialized
    if run_context.session_state is None:
        run_context.session_state = {}
    
    # Get the current draft from previous step
    current_draft = step_input.previous_step_content or ""
    
    # Store the current draft in session state for next revision
    run_context.session_state["previous_draft"] = current_draft
    
    # Get current iteration
    iteration = run_context.session_state.get("revision_iteration", 0)
    
    print(f"\n🔍 Manager Review - Review #{iteration + 1}/2")
    
    # Build critique prompt
    critique_prompt = f"""
    You are the Manager reviewing a travel plan prepared by your team lead.
    
    TRAVEL PLAN TO REVIEW (Draft #{iteration + 1}):
    {current_draft}
    
    {"This is the FINAL review - approve if it's reasonably good." if iteration >= 1 else "This is the initial review - provide constructive feedback."}
    
    Evaluate the plan for:
    1. Completeness - Does it cover all aspects (destination info, hotels, activities, itinerary)?
    2. Coherence - Does the day-by-day plan flow logically?
    3. Practicality - Are the activities feasible within the timeframe?
    4. Budget alignment - Do recommendations match the stated budget?
    
    Provide your structured assessment with specific improvement suggestions if needed.
    """
    
    # Run critique agent with session_state
    response = critique_agent.run(
        critique_prompt,
        session_state=run_context.session_state
    )
    
    # Parse the critique result
    is_approved = False
    feedback_text = ""
    
    if response.content:
        try:
            # Try to get structured output
            critique_data = getattr(response, 'response_model', None)
            
            if critique_data and isinstance(critique_data, CritiqueResult):
                is_approved = critique_data.is_approved
                feedback_text = f"{critique_data.overall_assessment}\n\nSpecific Feedback:\n{critique_data.specific_feedback}\n\nSuggestions:\n{critique_data.improvement_suggestions}"
            else:
                # Fallback: parse from content
                content_lower = str(response.content).lower()
                is_approved = ("approved" in content_lower or "good" in content_lower) and "not approved" not in content_lower
                feedback_text = str(response.content)
            
        except Exception as e:
            print(f"   ⚠️ Error parsing critique: {e}")
            # Auto-approve after 2 iterations
            is_approved = iteration >= 1
            feedback_text = str(response.content) if response.content else "Critique completed"
    else:
        # Default: approve if we've done 2 iterations
        is_approved = iteration >= 1
        feedback_text = "Critique completed"
    
    # Update session state with critique results
    run_context.session_state["is_approved"] = is_approved
    run_context.session_state["manager_feedback"] = feedback_text
    run_context.session_state["revision_iteration"] = iteration + 1
    
    status = "✅ APPROVED" if is_approved else "🔄 NEEDS REVISION"
    print(f"   Manager Decision: {status}")
    
    return StepOutput(
        content=feedback_text,
        success=True
    )


# Custom step for critique
critique_step = Step(
    name="Manager Review",
    executor=critique_and_revise,  # type: ignore[arg-type]
    description="Manager reviews the travel plan and provides approval or revision feedback"
)


def revision_approved_condition(run_context: RunContext) -> bool:  # type: ignore[arg-type]
    """
    End condition for the revision loop between team lead and manager.
    Returns True to BREAK the loop (when approved or max iterations reached), False to continue.
    
    Checks session_state for approval status set by the critique agent.
    """
    # Ensure session_state is initialized
    if run_context.session_state is None:
        run_context.session_state = {}
    
    # Get approval status and iteration from session state
    is_approved: bool = run_context.session_state.get("is_approved", False)
    iteration: int = run_context.session_state.get("revision_iteration", 0)
    
    if is_approved:
        print(f"\n✅ Travel plan APPROVED by Manager after {iteration} iteration(s)!")
        return True
    
    if iteration >= 2:
        print(f"\n⚠️ Max iterations reached ({iteration}). Finalizing plan.")
        return True
    
    print(f"\n🔄 Team Lead revising based on Manager feedback...")
    return False

