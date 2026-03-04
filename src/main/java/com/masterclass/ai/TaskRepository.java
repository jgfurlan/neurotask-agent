package com.masterclass.ai;
import dev.langchain4j.agent.tool.Tool; // IMPORTANT NEW IMPORT
import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.transaction.Transactional;

import java.util.List;

@ApplicationScoped
public class TaskRepository implements PanacheRepository<Task> {

    @Tool("Get the list of all tasks currently in the database") // Tell the AI what this does
    public List<Task> listAllTasks() {
        return listAll();
    }

    @Tool("Create a new task. Requires a short title and a detailed description")
    @Transactional // Ensures the task is actually saved to the database
    public void createTask(String title, String description) {
        Task task = new Task();
        task.title = title;
        task.description = description;
        task.persist();
    }

    @Tool("Delete a task from the database using its ID")
    @Transactional
    public void deleteTask(long id) {
        deleteById(id);
    }

    @Tool("Mark as completed a task from the database using its ID")
    @Transactional
    public void completeTask(long id) {
        // finding the task in the database
        Task task = findById(id);

        // setting the task as completed
        if (task != null) {
            task.completed = true;
            // With panache, modifications to persist fields
            //  are automatically saved at the end of the transaction
        }
    }
}
