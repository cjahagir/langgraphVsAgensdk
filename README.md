Intro: 
AI chatbot, which is a multi-agent structure having user data context with LLM knowledge base and web search ability.
For the sake of assessment, I have hard coded user data and skipped the part of Database pipeline and fetching user resume from AWS S3 bucket.
You can run both code files by just updating it with the working openAI API key and installing all required dependencies.

Going ahead with the comparison between langGraph and opneAI agent SKD:

Pros of langGraph:
Ease of resolutions for any blockers as it is having a more matured user base and many projects in production (which uses langGraph) to take inspiration from.
Deep customizations are possible on an architectural level like setting graph flow, rules for delegating tasks to different agents.

Pros of openAI agent SDK:
More human readable code due to multiple abstractions provided out of the box.
Using different tools is more simple as all tools and agent structure is inside a single framework.


Detailed analysis of why openAI agent SDK can be a better choice as compared to langGraph:
There cannot be one size fit all for any project obviously, so it clearly depends on exact use case.
Architecture design: 
OpenAI agen SDK required the developer to learn about a few major components/ fundamental topics like agents, tools, handoffs, Guardrails and runners. To start working with agents SDK is pretty straightforward, whereas in the langGraph framework, there are some complex topics like state management, nodes, edges which might be a little overwhelming for new developers.
Multiple inbuilt tools are available out of the box with agent SDK like  FileSearchTool, ComputerTool etc
Ease of use:
Code written in agent SDK is more readable and easy to maintain as developers do not have to worry about defining custom graph nodes(agents) and edges (rules).
Working with agent SDK feels more like working with advanced lego blocks, where developers need to correct tools as per requirement and integrate it seamlessly. 
I personally had never worked on agent SDK apart from watching a few youtube videos but it took me just a couple of trial and error to make my code work.

Performance: 
 Dependencies required while using agent SDK is also very minimal, for example in my code, where it took 12 lines code for dependency while using langGraph, but took only 5 lines code when using agent SDK. 
Even though the scope of this code is very straightforward and minimal, the difference is very stark, as a result it directly impacts on performance and efficiency of the AI agents created.
Cost:
Tools are available for both frameworks, but agen SDK provides in build tools, this thing not only seamlessly integrates while working but the major thing is the cost. Users do not have to pay for each new tool they want to use.


Future proof:
 There is no enterprise level support for langGraph as it is open source, while for agent SDK it is backed by openAI which provides long‑term stability making our projects using agent SDK more future proof.
Tracking agents and our LLM model responses is possible in both(agent SDK and langGraph) but very straightforward for agent SDK. In agent SDK we just need to go to openAI dashboard and you can see all traces in detail

There are many additional features in agent SDK like ‘Traces’ which provides in depth information to users about each agent (info regarding API call for each agent), which is one of the standout features. Even though langGraph provides the same tool for this which is ‘langSmith’ but it requires the user to additionally integrate it in the code which is altogether another complex task. 
Support from openAI guarantees that the improvements in future will surely come for tools and other features.
Delegating tasks to different specialized agents is very straightforward in agen SDK, which reduces the work to manage complex state management. But if the project requirement is complex and needs changes and modification at the granular level, then langGraph might be a better choice. 

Improvements we can make in code:
We can add more agents to handle different tasks like agent to take user assessment, agency to create in detail career guidance plan which user can download like a PDF etc.
We can add guardrails to keep a check on the results being generated and also use ‘Agent Output’ for keeping a check on the output format of the agents.
We can also improve the prompts and hangoff logic, right now it is POC level, but we can surely improve it.
