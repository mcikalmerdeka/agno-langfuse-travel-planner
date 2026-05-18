"""Pydantic schemas for structured outputs."""
from pydantic import BaseModel, Field

# Destination Info Schema
class DestinationInfo(BaseModel):
    destination: str = Field(..., description="Name of the destination city or region")
    top_attractions: str = Field(..., description="List of top 3-5 must-visit attractions")
    best_time_to_visit: str = Field(..., description="Best season or months to visit with weather context")
    local_tips: str = Field(..., description="Practical tips for travelers (etiquette, safety, transport)")
    weather_info: str = Field(..., description="Current weather conditions and forecast")


# Accommodation Options Schema
class AccommodationOptions(BaseModel):
    destination: str = Field(..., description="Name of the destination")
    hotel_recommendations: str = Field(..., description="List of 3-5 specific hotel names with brief details")
    budget_range: str = Field(..., description="Estimated price range per night (e.g., $100-$200)")
    booking_tips: str = Field(..., description="Advice on when and where to book for best rates")


# Activities Info Schema
class ActivitiesInfo(BaseModel):
    destination: str = Field(..., description="Name of the destination")
    recommended_activities: str = Field(..., description="List of specific activities or tours to do")
    transportation_options: str = Field(..., description="Best ways to get around (metro, taxi, walking)")
    local_experiences: str = Field(..., description="Unique cultural experiences or food options")
    estimated_costs: str = Field(..., description="Estimated costs for activities and transport")


# Daily Itinerary Schema
class DailyItinerary(BaseModel):
    destination: str = Field(..., description="Name of the destination")
    trip_duration: str = Field(..., description="Duration of the trip (e.g., '5 days')")
    day_by_day_plan: str = Field(..., description="Detailed markdown formatted itinerary, organized by day")


# Critique Result Schema
class CritiqueResult(BaseModel):
    is_approved: bool = Field(..., description="True if the plan is ready for the user, False if it needs revision")
    overall_assessment: str = Field(..., description="Brief summary of the critique")
    specific_feedback: str = Field(..., description="Detailed feedback on what is good and what needs improvement")
    improvement_suggestions: str = Field(..., description="Actionable steps to fix the identified issues")

