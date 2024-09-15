from dotenv import load_dotenv
import os
import argparse
from atproto import Client

# Load the .env file
load_dotenv()

# Your Bluesky handle and app password
USERNAME = os.environ.get('BLUESKY_USERNAME')
PASSWORD = os.environ.get('BLUESKY_PASSWORD')

if not USERNAME or not PASSWORD:
    raise ValueError("BLUESKY_USERNAME and BLUESKY_PASSWORD must be set in the .env file or as environment variables")

# Set up argument parsing
parser = argparse.ArgumentParser(description='Retrieve follower or following relationships.')
parser.add_argument(
    '-n', '--number',
    type=int,
    default=10,
    help='Number of users to retrieve (default: 10)'
)
parser.add_argument(
    '-r', '--relationship',
    choices=['followers', 'following'],
    default='following',
    help='Type of relationship to retrieve (followers or following)'
)
args = parser.parse_args()

N = args.number  # N will be 10 if not specified

# Initialize the client and log in
client = Client()
client.login(USERNAME, PASSWORD)

# Get your Decentralized Identifier (DID)
params = {'actor': USERNAME}
profile = client.app.bsky.actor.get_profile(params=params)
my_did = profile.did  # Accessing the 'did' attribute

# Function to get all followers up to a limit
def get_all_followers(client, did, limit=None):
    followers = []
    cursor = None

    while True:
        response = client.app.bsky.graph.get_followers(params={'actor': did, 'cursor': cursor})
        followers.extend(response.followers)

        # If a limit is set and reached, truncate and break
        if limit is not None and len(followers) >= limit:
            followers = followers[:limit]
            break

        cursor = response.cursor
        if not cursor:
            break

    return followers

# Function to get all followings up to a limit
def get_all_followings(client, did, limit=None):
    followings = []
    cursor = None

    while True:
        response = client.app.bsky.graph.get_follows(params={'actor': did, 'cursor': cursor})
        followings.extend(response.follows)

        # If a limit is set and reached, truncate and break
        if limit is not None and len(followings) >= limit:
            followings = followings[:limit]
            break

        cursor = response.cursor
        if not cursor:
            break

    return followings

# Retrieve relationships based on the specified type
if args.relationship == 'followers':
    relationships = get_all_followers(client, my_did, limit=N)
    relationship_type = 'Follower'
else:
    relationships = get_all_followings(client, my_did, limit=N)
    relationship_type = 'Following'

# Set the output filename based on the relationship type
output_filename = f"{relationship_type.lower()}_connections.csv"

# Map follower DIDs to their handles
follower_did_to_handle = {follower.did: follower.handle for follower in relationships}

# Function to get followings of a user (used later to find mutual connections)
def get_followings(client, did):
    followings = []
    cursor = None

    while True:
        try:
            response = client.app.bsky.graph.get_follows(params={'actor': did, 'cursor': cursor})
            followings.extend(response.follows)
            cursor = response.cursor
            if not cursor:
                break
        except Exception as e:
            print(f"Error retrieving followings for DID {did}: {e}")
            break

    return followings

# Open the CSV file and write data
with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
    # Write the header manually
    csvfile.write('Relationship Type,Username,Mutual Connections\n')
    
    for person in relationships:
        # Print progress for each username
        print(f"Processing username: {person.handle}")

        # Get the followings of the person
        person_followings = get_followings(client, person.did)

        # Find mutual connections
        mutual_connections = set()
        for following in person_followings:
            if following.did in follower_did_to_handle:
                mutual_connections.add(follower_did_to_handle[following.did])

        # Convert the set to a sorted list for consistency
        mutual_connections_list = sorted(list(mutual_connections))

        # Enclose each username in double quotes
        mutual_connections_list_with_quotes = [f'"{username}"' for username in mutual_connections_list]

        # Format mutual connections with commas inside brackets
        mutual_connections_str = '[' + ', '.join(mutual_connections_list_with_quotes) + ']'

        # Build the CSV line
        line = f"{relationship_type},{person.handle},{mutual_connections_str}\n"

        # Write the line to the CSV file
        csvfile.write(line)

        # Flush data to disk after each write
        csvfile.flush()

print(f"Connections have been saved to '{output_filename}'.")