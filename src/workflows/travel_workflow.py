"""Main travel planning workflow definition."""
from agno.workflow import Workflow, Parallel, Loop
from workflows.steps import (
    destination_step,
    hotel_step,
    activities_step,
    itinerary_step,
    final_report_step
)
from workflows.critique_logic import critique_step, revision_approved_condition

# Complete Travel Planning Workflow
travel_planning_workflow = Workflow(
    name="Travel Planning Workflow with Manager Approval",
    description="""
    A streamlined travel planning workflow:
    1. Research Team (destination, hotel, activities) runs in parallel ONCE
    2. Team Lead (itinerary planner) creates comprehensive report
    3. Manager (critique agent) reviews and provides feedback
    4. Loop (max 1 revision): Team Lead revises report based on Manager feedback
    5. Team Lead presents final Manager-approved report to user
    """,
    # Initialize session state for tracking workflow progress
    session_state={
        "revision_iteration": 0,
        "is_approved": False,
        "manager_feedback": "No feedback yet - this is the initial draft",
        "previous_draft": "No previous draft",
    },
    steps=[  # type: ignore[arg-type]
        # Step 1: Research Team - Parallel research phase (runs ONCE only)
        Parallel(
            destination_step,  # type: ignore[list-item]
            hotel_step,  # type: ignore[list-item]
            activities_step,  # type: ignore[list-item]
            name="Research Team Phase",
            description="Research team gathers destination, hotel, and activities data simultaneously"
        ),
        # Step 2: Team Lead + Manager Loop (max 2 iterations: initial + 1 revision)
        Loop(
            name="Team Lead <-> Manager Revision Loop",
            description="Itinerary planner (team lead) works with Manager to finalize the plan",
            steps=[
                itinerary_step,  # type: ignore[list-item] - Team Lead creates/revises report
                critique_step,  # type: ignore[list-item] - Manager reviews and approves/requests revision
            ],
            end_condition=revision_approved_condition,  # type: ignore[arg-type]
            max_iterations=2,  # Initial draft + 1 revision max
        ),
        # Step 3: Team Lead presents the final Manager-approved report
        final_report_step,  # type: ignore[list-item] - This becomes the final output to the user
    ],
)

