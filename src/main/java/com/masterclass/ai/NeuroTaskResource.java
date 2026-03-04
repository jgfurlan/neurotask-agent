package com.masterclass.ai;

import jakarta.inject.Inject;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;

@Path("/neurotask")
public class NeuroTaskResource {

    @Inject
    Assistant assistant;

    @POST
    @Path("/chat")
    public String chat(String message) {
        return assistant.chat(message);
    }
}
