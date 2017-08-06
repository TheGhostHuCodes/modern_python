"""
Use k-means to locate voting clusters in the U.S. Congress.
"""
from kmeans import k_means, assign_data

from collections import defaultdict
import csv
import glob
from typing import Counter, DefaultDict, Dict, List, NamedTuple, Tuple

Senator = NamedTuple('Senator', [('name', str), ('party', str), ('state',
                                                                 str)])
VoteValue = int
VoteHistory = Tuple[VoteValue, ...]

NUM_SENATORS = 100

# Load votes which were arranged by topic and accumulate votes by senator.
vote_value: Dict[str, VoteValue] = {'Yea': 1, 'Nay': -1, 'Not Voting': 0}
accumulated_record: DefaultDict[Senator, List[VoteValue]] = defaultdict(list)
for filename in glob.glob('congress_data/*.csv'):
    with open(filename, encoding='utf-8') as f:
        reader = csv.reader(f)
        vote_topic = next(reader)
        header = next(reader)
        for person, state, district, vote, name, party in reader:
            senator = Senator(name, party, state)
            accumulated_record[senator].append(vote_value[vote])

# Transform the record into a plain dict that maps to a tuple of votes.
record = {
    senator: tuple(votes)
    for senator, votes in accumulated_record.items()
}  # type: Dict[Senator, VoteHistory]

# Use k-means to locate the cluster centroids from pattern of votes, assign
# each senator to the nearest cluster.
centroids = k_means(record.values(), k=3)
clustered_votes = assign_data(centroids, record.values())

# Build a reverse mapping from a vote history to a list of senators who voted
# that way.
votes_to_senators: DefaultDict[VoteHistory, List[Senator]] = defaultdict(list)
for senator, votehistory in record.items():
    votes_to_senators[votehistory].append(senator)
assert sum(len(cluster)
           for cluster in votes_to_senators.values()) == NUM_SENATORS

# Display the clusters and the members (senators) of each cluster.
for i, votes_in_cluster in enumerate(clustered_votes.values(), start=1):
    print(f"==================== Voting Cluster #{i} ====================")
    party_totals: Counter[str] = Counter()
    for votes in set(votes_in_cluster):
        for senator in votes_to_senators[votes]:
            party_totals[senator.party] += 1
            print(senator)
    print(party_totals)
