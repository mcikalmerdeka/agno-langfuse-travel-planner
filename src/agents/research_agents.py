"""Specialized research agents for travel planning."""
from textwrap import dedent
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools.web_search import web_search_tool
from core.schemas import DestinationInfo, AccommodationOptions, ActivitiesInfo

# Destination Researcher Agent
destination_researcher = Agent(
    id="destination-researcher",
    name="Destination Researcher",
    role="Expert at researching travel destinations",
    description="You are a travel expert who finds the best attractions, local tips, weather info, and cultural insights for destinations.",
    instructions=dedent("""\
        Search for top attractions and must-see places
        Find current weather conditions and best times to visit
        Discover local tips, cultural etiquette, and hidden gems
        Focus on practical, up-to-date information
    """),
    model=OpenAIChat(id="gpt-4.1-nano"),
    tools=[web_search_tool],
    output_schema=DestinationInfo,
    markdown=True,
)

# Hotel & Accommodation Finder Agent
hotel_finder = Agent(
    id="hotel-finder",
    name="Hotel & Accommodation Finder",
    role="Expert at finding the best hotels and accommodations",
    description="You are a travel accommodation specialist who finds the best places to stay based on budget and preferences.",
    instructions=dedent("""\
        Search for highly-rated hotels and accommodations
        Consider different budget ranges (budget, mid-range, luxury)
        Look for good locations near attractions
        Provide booking tips and best times to book
    """),
    model=OpenAIChat(id="gpt-4.1-nano"),
    tools=[web_search_tool],
    output_schema=AccommodationOptions,
    markdown=True,
)

# Activities & Experiences Researcher Agent
activities_researcher = Agent(
    id="activities-researcher",
    name="Activities & Experiences Researcher",
    role="Expert at finding local activities, transportation, and unique experiences",
    description="You are a travel activities specialist who finds the best things to do, local transportation options, and unique experiences.",
    instructions=dedent("""\
        Specify the destination name
        Search for popular activities and unique local experiences
        Find transportation options (public transit, car rental, walking routes)
        Discover food tours, cultural workshops, and authentic local experiences
        Provide estimated costs for activities and transportation
    """),
    model=OpenAIChat(id="gpt-4.1-nano"),
    tools=[web_search_tool],
    output_schema=ActivitiesInfo,
    markdown=True,
)

