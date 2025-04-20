# pip install langchain-openai langchain-community langchain-core langgraph typing-extensions faiss-cpu tavily-python
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated
from typing import List
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain.schema.runnable import Runnable
from typing import List, TypedDict, Annotated


os.environ["TAVILY_API_KEY"] = "give your API key"
os.environ["OPENAI_API_KEY"] =" give your API key"

user_id = "test_user_123"
documents = [
    """User Profile:
Current Role: Gen AI Software Developer
Years of Experience: 4
Current Salary: 10 LPA
Current Company: Xcube labs
Career Aspiration: Work on latest tech and stay up to date
Dream Role: CTO
Certifications: AWS certified
Education: Msc in IT""",
    """Assessment Summary:
Assessment Score: 82
Evaluation: Strong technical skills and good communication; needs better product understanding"""
]


class State(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]


def create_runnable_graph(documents: List[str]) -> Runnable:
    embedding = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(documents, embedding=embedding)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)

    
    base_prompt = ChatPromptTemplate.from_messages([
        ("system", """
You are a friendly career advisor with expertise in realistic career transitions, growth planning, and skill development.
Use the following context to inform your advice:
{context}
        """),
        MessagesPlaceholder(variable_name="messages"),
    ])


    def llm_agent(state: State) -> dict:
        query = state["messages"][-1].content
        docs = retriever.invoke(query)
        context = "\n\n".join(
            [f"--- Document {i+1} ---\n{doc.page_content}" for i, doc in enumerate(docs)]
        ) if docs else "No relevant context found."
        
        prompt_input = {"context": context, "messages": state["messages"]}
        prompt = base_prompt.invoke(prompt_input)
        response = llm.invoke(prompt)
        return {"messages": [response]}

    
    def web_search_agent(state: State) -> dict:
        query = state["messages"][-1].content
        search_tool = TavilySearchResults()
        results = search_tool.run(query)
        context = f"Here are some relevant results from the web:\n\n{results}"

        prompt_input = {"context": context, "messages": state["messages"]}
        prompt = base_prompt.invoke(prompt_input)
        response = llm.invoke(prompt)
        return {"messages": [response]}

    
    router_prompt = ChatPromptTemplate.from_messages([
        ("system", """
You are a router deciding which expert should answer the question. 
Respond with ONLY the word 'llm' if the question can be answered from known context or career data. 
Respond with ONLY the word 'web' if the question needs real-time information like job trends, salaries, or in-demand skills.

No extra words. Just say: llm OR web.
        """),
        MessagesPlaceholder(variable_name="messages"),
    ])

    


    def route_decision(state: State) -> str:
        prompt = router_prompt.invoke({"messages": state["messages"]})
        decision = llm.invoke(prompt).content.strip().lower()
        return "web_search_agent" if "web" in decision else "llm_agent"


    def router_node(state: State) -> State:
        return state



    graph = StateGraph(State)
    graph.add_node("llm_agent", llm_agent)
    graph.add_node("web_search_agent", web_search_agent)
    graph.add_node("router", router_node)
    graph.add_conditional_edges("router", route_decision, {
        "llm_agent": "llm_agent",
        "web_search_agent": "web_search_agent"
    })

    graph.set_entry_point("router")
    graph.add_edge("llm_agent", END)
    graph.add_edge("web_search_agent", END)

    return graph.compile()


if __name__ == "__main__":
    
    graph = create_runnable_graph(documents)

    
    chat_history = []

    print("Career Coach Chatbot 🧠💼 (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting. Goodbye!")
            break

        
        chat_history.append(HumanMessage(content=user_input))

        
        state = {"messages": chat_history}

        
        result = graph.invoke(state)

        
        response_msg = result["messages"][-1]
        chat_history.append(response_msg)

        
        print(f"Coach: {response_msg.content}\n")


