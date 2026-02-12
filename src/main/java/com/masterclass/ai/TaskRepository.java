package com.masterclass.ai;

import dev.langchain4j.agent.tool.Tool;
import io.smallrye.common.annotation.RunOnVirtualThread;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.transaction.Transactional;
import java.util.List;

@ApplicationScoped
public class TaskRepository {

    @Tool("Save a new task to the database")
    @Transactional // Required for writing data
    @RunOnVirtualThread // Masterclass: Database wait happens on a Virtual Thread
    public void persistTask(String title, String description) {
        Task task = new Task();
        task.title = title;
        task.description = description;
        task.completed = false;
        task.persist(); // Panache magic
    }

    @Tool("List all current tasks")
    @RunOnVirtualThread
    public List<Task> listAllTasks() {
        return Task.listAll();
    }
}
