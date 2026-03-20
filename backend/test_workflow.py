from workflow.langgraph_flow import graph

alert = {
    "alert": "Multiple failed login attempts detected",
    "system": "authentication-server"
}

result = graph.invoke(alert)

print(result)