"""Main entry point for the Travel Planning Workflow."""
from langfuse import observe, propagate_attributes

# Import configuration (initializes Langfuse and OpenLIT)
from core.config import langfuse
from core.utils import make_agent_observable

# Import agents
from agents.research_agents import destination_researcher, hotel_finder, activities_researcher
from agents.planner_agent import itinerary_planner
from agents.critique_agent import critique_agent

# Import workflow
from workflows.travel_workflow import travel_planning_workflow

# Import Gradio interface
from frontend import create_gradio_interface


# Apply Langfuse observation to all agents
make_agent_observable(destination_researcher, "destination-researcher")
make_agent_observable(hotel_finder, "hotel-finder")
make_agent_observable(activities_researcher, "activities-researcher")
make_agent_observable(itinerary_planner, "itinerary-planner")
make_agent_observable(critique_agent, "critique-agent")


@observe(as_type="span", name="Travel Planning Pipeline")
async def plan_trip(query: str):
    """
    Run the travel planning workflow with Langfuse tracing.
    
    Workflow Structure:
    ==================
    Travel Planning Pipeline (span)
    └── travel-planning-workflow (agent)
        ├── Research Team Phase ⚡ (runs ONCE only)
        │   ├── destination-researcher (agent) → tavily-web-search
        │   ├── hotel-finder (agent) → tavily-web-search
        │   └── activities-researcher (agent) → tavily-web-search
        │
        ├── Team Lead <-> Manager Revision Loop (max 2 iterations)
        │   ├── Iteration 1:
        │   │   ├── itinerary-planner (team lead) → creates initial report
        │   │   └── critique-agent (manager) → reviews and approves/requests revision
        │   └── Iteration 2 (if Manager requested revision):
        │       ├── itinerary-planner (team lead) → revises report based on Manager feedback
        │       └── critique-agent (manager) → final approval
        │
        └── Present Final Report 📋
            └── itinerary-planner (team lead) → presents Manager-approved plan to user
    
    Benefits:
    - Research agents (Tavily tool calls) run ONLY ONCE at the start
    - Only itinerary planner revises in loop, no redundant research calls
    - Maximum 2 loop iterations = 1 revision opportunity
    - Mimics real org structure: Research Team → Team Lead → Manager approval
    - Final output is from itinerary planner (natural language), not critique (structured)
    """
    with propagate_attributes(
        # Change these attributes to your own
        trace_name="travel-planning-trace",
        user_id="cikalmerdeka",
        session_id="travel-planning-pipeline-001",
        tags=["travel", "planning", "workflow", "manager-approval"],
        version="1.0.0",
        metadata={
            "experiment": "travel_planning_pipeline",
            "environment": "development",
            "execution_mode": "parallel_once_then_revision_loop"
        }
    ):
        result = await travel_planning_workflow.arun(query)
        
        # Update trace with final input/output
        langfuse.update_current_trace(
            input=query,
            output=result.content if result else None,
        )
        
        return result


if __name__ == "__main__":
    print("=" * 70)
    print("🌏 TRAVEL PLANNING WORKFLOW - WEB INTERFACE")
    print("=" * 70)
    print("\n🚀 Starting Gradio interface...")
    print("📊 Langfuse tracing is enabled for all workflows")
    print("=" * 70)
    
    # Create and launch the Gradio interface
    interface = create_gradio_interface(plan_trip)
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        quiet=False
    )

