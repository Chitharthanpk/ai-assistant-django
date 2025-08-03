def searchIntegrationFunction(user_message):
    if "calendar" in user_message.lower():
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_calendar_events",
                    "description": "Get user's Google Calendar events for today",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    },
                    "required": []
                }
            }
        ]
    return []

def callIntegrationFunction(params):
    return {"events": ["Meeting with team", "Doctor appointment"]}
