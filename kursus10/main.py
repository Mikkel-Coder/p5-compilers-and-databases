from context_agent import ContextAgent
from argparse import ArgumentParser
from time import sleep

parser = ArgumentParser()
parser.add_argument('agentnum', type=int)
parser.add_argument('--waittime', type=int, default=6)
args = parser.parse_args()

context_agents = []

print(f"Making {args.agentnum} agents...")
for _ in range(args.agentnum):
    context_agents.append(ContextAgent(context_agents))

print("Starting agents...")
for agent in context_agents:
    agent.start()

print("Waiting for data population...")
for i in range(args.waittime, -1, -1):
    sleep(1)
    print(f"Time left: {i}", end="\r")

print()

print("\nGetting data from single agents...")
for agent in context_agents:
    print(f"Getting data from {agent.name}: ", end="")
    agent.child_conn.send({
        "method": "get",
        "scope": "host"
    })
    data = agent.child_conn.recv()
    print(data)

print("\nGetting data from network...")
for agent in context_agents:
    print(f"Getting network data by asking {agent.name}: ", end="")
    agent.child_conn.send({
        "method": "get",
        "scope": "network"
    })
    data = agent.child_conn.recv()
    print(data)
