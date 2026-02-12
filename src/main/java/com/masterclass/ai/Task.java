package com.masterclass.ai;

import io.quarkus.hibernate.orm.panache.PanacheEntity;
import jakarta.persistence.Entity;
import java.time.LocalDateTime;

@Entity
public class Task extends PanacheEntity {
    public String title;
    public String description;
    public boolean completed;
    public LocalDateTime createdAt = LocalDateTime.now();
}
