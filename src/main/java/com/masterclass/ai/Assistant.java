package com.masterclass.ai;

import dev.langchain4j.service.SystemMessage;
import dev.langchain4j.service.UserMessage;
import io.quarkiverse.langchain4j.RegisterAiService;

@RegisterAiService(tools = TaskRepository.class)
public interface Assistant {

    @SystemMessage("""
        You are the NeuroTask Agent.
        Your primary role is to manage a database of tasks.

        CRITICAL INSTRUCTIONS:
        1. Always call 'listAllTasks' before answering questions about existing tasks.
        2. To create a task, you MUST have both a short 'title' and a longer 'description'.
        3. If the user asks to create a task but doesn't give a description, DO NOT create it yet. Ask them: "Please provide a description for this task."
        4. Once you have both the title and description, call the 'createTask' tool.

        Do not make up tasks. Use the tools.
        """)
    String chat(@UserMessage String message);
}
