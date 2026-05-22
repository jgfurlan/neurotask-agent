# UI Context: OceanCompass & API Interfaces

This document defines the interface standards, design tokens, and endpoint structures for guest-facing tools in the Carnival ecosystem.

## Design Tokens (Oceanic Theme)

Applications interacting with the OceanCortex Agent (such as the OceanCompass mobile app or stateroom portal) must adopt the following color palette to match the company identity:

| Token | Hex | Usage |
|-------|-----|-------|
| `ocean-blue` | `#0A3161` | Primary branding, buttons, headers |
| `seafoam` | `#00D2C4` | Success status, interactive highlights, active states |
| `coral` | `#FF6F61` | Alerts, destructive actions, cancel buttons |
| `gold` | `#FFC72C` | Warnings, premium tier branding, loyalty badges |
| `sand` | `#F4F1EA` | Background body color (light mode surfaces) |
| `navy-dark` | `#111E38` | Text color, dark mode surface panels |

## API Boundaries & Interfaces

The backend exposes REST endpoints for stateroom screens, tablets, and mobile devices.

### REST Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/ocean/chat` | Chat with the multi-agent network (routes via Supervisor) |
| `GET` | `/ocean/guest/profile` | Retrieves current guest Medallion state and preferences |
| `GET` | `/ocean/health/live` | Liveness check (ECS orchestration) |
| `GET` | `/ocean/health/ready` | Readiness check (Snowflake Cortex connectivity verification) |
| `GET` | `/ocean/metrics` | Micrometer metrics for agent reward performance monitoring |

### Chat Payload Example

`POST /ocean/chat`
```json
{
  "message": "Order a cold pina colada to my current sunbed on Deck 9",
  "medallion_id": "MED-99381-A2"
}
```

**Response:**
```json
{
  "response": "I've placed your order for a Piña Colada! It will be delivered to you at Deck 9, Sunbed 42 shortly.",
  "action_taken": "order_delivery",
  "status": "success"
}
```

## UX Paradigms

1. **Anticipatory Feedback**:
   - The UI should not just display raw logs. If a guest is near a crowded dining room, the agent suggests booking a table at a specialty restaurant on the opposite deck.
2. **Contactless Confirmation**:
   - Every agent execution must display clear visual confirmation (a green checkmark or order code) so the guest knows the task was executed safely without requiring a physical card swipe.
3. **Accessibility (WCAG 2.2 AA)**:
   - High contrast ratios (4.5:1 minimum for body text).
   - Clear focus rings for keyboard navigation.
   - Screen reader attributes (`aria-live`, `aria-label`) on all dynamic chat bubbles.
