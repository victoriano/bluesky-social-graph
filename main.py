from dotenv import load_dotenv
import os
import argparse
import csv
from atproto import Client

# Load the .env file
load_dotenv()

# Your Bluesky handle and app password
USERNAME = os.environ.get('BLUESKY_USERNAME')
PASSWORD = os.environ.get('BLUESKY_PASSWORD')

if not USERNAME or not PASSWORD:
    raise ValueError("BLUESKY_USERNAME and BLUESKY_PASSWORD must be set in the .env file or as environment variables")

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Retrieve follower connections.')
parser.add_argument('-n', '--number', type=int, help='Limit the number of followers to process')
args = parser.parse_args()

N = args.number  # N will be None if not specified

# Initialize the client and log in
client = Client()
client.login(USERNAME, PASSWORD)

# Get your Decentralized Identifier (DID)
params = {'actor': USERNAME}
profile = client.app.bsky.actor.get_profile(params=params)
my_did = profile.did  # Accessing the 'did' attribute

# Retrieve your followers
def get_all_followers(client, did, limit=None):
    followers = []
    cursor = None

    while True:
        response = client.app.bsky.graph.get_followers(params={'actor': did, 'cursor': cursor})

        # Access the 'followers' list from the response
        followers.extend(response.followers)

        # If a limit is set and we've reached it, truncate the list and break
        if limit is not None and len(followers) >= limit:
            followers = followers[:limit]
            break

        # Access the 'cursor' attribute from the response
        cursor = response.cursor

        if not cursor:
            break

    return followers

followers = get_all_followers(client, my_did, limit=N)

# Map follower DIDs to their handles
follower_did_to_handle = {follower.did: follower.handle for follower in followers}

# Initialize a dictionary to store connections
follower_connections = {}

# Function to get followings of a follower
def get_followings(client, did):
    followings = []
    cursor = None

    while True:
        try:
            response = client.app.bsky.graph.get_follows(params={'actor': did, 'cursor': cursor})

            # Access the 'follows' list from the response
            followings.extend(response.follows)

            # Access the 'cursor' attribute from the response
            cursor = response.cursor

            if not cursor:
                break
        except Exception as e:
            print(f"Error retrieving followings for DID {did}: {e}")
            break

    return followings

# Retrieve followings for each follower and find mutual connections
for follower in followers:
    follower_did = follower.did
    follower_handle = follower.handle
    print(f"Processing follower: {follower_handle}")

    followings = get_followings(client, follower_did)
    following_dids = {following.did for following in followings}

    # Find mutual followers
    mutual_followers = following_dids & set(follower_did_to_handle.keys())
    mutual_handles = [follower_did_to_handle[did] for did in mutual_followers]

    follower_connections[follower_handle] = mutual_handles

# Save the connections to a CSV file manually
with open('follower_connections.csv', 'w', encoding='utf-8') as file:
    # Write the header
    file.write('Follower,Mutual Connections\n')
    for follower, connections in follower_connections.items():
        # Format connections as per required format
        connections_str = '[' + ', '.join(f'"{c}"' for c in connections) + ']'
        line = f'{follower},{connections_str}\n'
        file.write(line)

print("Follower connections have been saved to 'follower_connections.csv'.")