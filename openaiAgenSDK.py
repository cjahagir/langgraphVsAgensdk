# pip install openai openai-agents
from openai import OpenAI
from agents import Agent, Runner, function_tool, RunContextWrapper, WebSearchTool
import asyncio
import os
from dataclasses import dataclass


openai_key = os.environ["OPENAI_API_KEY"] ="give yout API key"
client = OpenAI(api_key=openai_key)


@dataclass
class UserContext:
    user_id: str
    profile: str
    assessment: str

@function_tool
async def get_user_profile(wrapper: RunContextWrapper[UserContext]) -> str:
    return f"User Profile:\n{wrapper.context.profile}\n\nAssessment Summary:\n{wrapper.context.assessment}"


web_search_agent = Agent[UserContext](
    name="Web Search Agent",
    handoff_description="Handles real-time information queries using web search.",
    instructions="Use the web_search_preview tool to fetch up-to-date information and help user in career developmentand job search",
    tools=[WebSearchTool()]
)

general_agent = Agent[UserContext](
    name="General Agent",
    handoff_description="Handles general queries with access to user profile and assessment.",
    instructions="You are career coach who Provide responses using the LLM capabilities and user context.",
    tools=[get_user_profile]
)

triage_agent = Agent[UserContext](
    name="Triage Agent",
    instructions="Delegate tasks to the appropriate agent based on the query.",
    handoffs=[web_search_agent, general_agent]
)


async def main():
    user_context = UserContext(
        user_id="test_user_123",
        profile="""Current Role: Software Developer
Years of Experience: 4
Current Salary: 10 LPA
Current Company: ABC Tech
Career Aspiration: Move into a Product Manager role
Dream Role: Product Manager at a startup
Certifications: Scrum Master Certification
Education: B.Tech in Computer Science""",
        assessment="""Assessment Score: 82
Evaluation: Strong technical skills and good communication; needs better product understanding"""
    )

    print("Career Coach Chatbot 🧠💼 (type 'exit' to quit)\n")
    while True:
        user_input = input("\nYou: ")
        if user_input.strip().lower() == "exit":
            print("Goodbye!")
            break

        result = await Runner.run(
            starting_agent=triage_agent,
            input=user_input,
            context=user_context
        )
        print(f"\nACoach: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
