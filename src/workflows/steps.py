"""Workflow step definitions."""
from agno.workflow import Step
from agents.research_agents import destination_researcher, hotel_finder, activities_researcher
from agents.planner_agent import itinerary_planner


# Initial parallel research steps
destination_step = Step(
    name="Research Destination",
    agent=destination_researcher,
    description="Research the destination's attractions, weather, and local tips"
)

hotel_step = Step(
    name="Find Accommodations",
    agent=hotel_finder,
    description="Find suitable hotels and accommodations based on budget"
)

activities_step = Step(
    name="Research Activities",
    agent=activities_researcher,
    description="Research activities, transportation, and local experiences"
)

# Itinerary planning step
itinerary_step = Step(
    name="Create Itinerary",
    agent=itinerary_planner,
    description="Create a comprehensive day-by-day travel itinerary"
)

# Final report step
final_report_step = Step(
    name="Present Final Report",
    agent=itinerary_planner,
    description="Team Lead presents the Manager-approved travel plan to the user"
)

