from context_agent import ContextAgent

agent1 = ContextAgent([])

agent1.start()

agent1.child_conn.send({"method": "post", "value": 5})

agent1.child_conn.send({"method": "get"})

print(agent1.child_conn.recv())
