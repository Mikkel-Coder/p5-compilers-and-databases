from context_agent import ContextAgent
from argparse import ArgumentParser
from time import sleep

parser = ArgumentParser()
parser.add_argument('agentnum', type=int)
args = parser.parse_args()

context_agents = []

print("Making agents...")
for _ in range(args.agentnum):
    context_agents.append(ContextAgent(context_agents))

print("Starting agents...")
for agent in context_agents:
    agent.start()

sleep(10)
while True:
    for agent in context_agents:
        print(f"Getting data from {agent.name}...", end="")
        agent.child_conn.send({
            "method": "get"
        })
        data = agent.child_conn.recv()
        print(data)

    sleep(5)
