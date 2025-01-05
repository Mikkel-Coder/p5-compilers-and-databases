"""
python3 main.py 3
"""
from time import sleep
from argparse import ArgumentParser
from context_agent import ContextAgent

# Use the program from the CLI
parser = ArgumentParser() 

# agentnum: how many agents should participate i the Peer to Peer network?
parser.add_argument('agentnum', type=int, default=3)

# How long will you wait in-between asking the ContextAgent? in seconds
# The DataMaker generates data between 1-6 sec
parser.add_argument('--waittime', type=int, default=6)
args = parser.parse_args()


# Context agent are pregenerate so that each agent knows every other agent
context_agents = []
print(f"Making {args.agentnum} agents...")
for _ in range(args.agentnum):
    context_agents.append(ContextAgent(context_agents))

# Now start each context agent
# Each context agent then starts their own DataMaker Thread 
print("Starting agents...")
for agent in context_agents:
    agent.start()

# Now we wait for some data to be generated...
print("Waiting for data population...")
sleep(args.waittime)

# Continue in a while loop asking single and network agents
while True:
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
    
    sleep(args.waittime)
