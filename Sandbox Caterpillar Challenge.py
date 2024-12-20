import requests 

# GET request
url = "https://challenge.sandboxnu.com/s/PMRGIYLUMERDU6ZCMVWWC2LMEI5CE53BNYXGY2LTIBXG64TUNBSWC43UMVZG4LTFMR2SELBCMR2WKIR2GE3TGNBXGU3TCOJZFQRGG2DBNRWGK3THMURDUISDMFZHA33PNQRH2LBCNBQXG2BCHIRDETLQOM3USL2NLFWEMVSQNZLDMT3HIU6SE7I="
response = requests.get(url)
data = response.json()

def calculate_average_location(grid, ids):
    total_x, total_y, count = 0, 0, 0
    for y, row in enumerate(grid):
        for x, id in enumerate(row):
            if id in ids:
                total_x += x
                total_y += y
                count += 1
    if count == 0:
        return {"x": 0, "y": 0}
    return {"x": total_x // count, "y": total_y // count}


def calculate_manhattan_distance(loc1, loc2):
    return abs(loc1["x"] - loc2["x"]) + abs(loc1["y"] - loc2["y"])

def groups(data):
    pickupLocations = data["pickupLocations"]
    dropoffLocations = data["dropoffLocations"]
    requests = data["requests"]

    # initializes groups
    groups = {}

    # creates groups based on accepted requests
    for request in requests:
        if request["accepted"]:
            riderId = request["rider"]
            driverId = request["driver"]
            if driverId not in groups:
                groups[driverId] = {"driverId": driverId, "riderIds": []}
            groups[driverId]["riderIds"].append(riderId)

    # calculates average pickup/dropoff locations for each group
    groupStats = []
    for driverId, group in groups.items():
        group_member_ids = [driverId] + group["riderIds"]
        avg_pickup = calculate_average_location(pickupLocations, group_member_ids)
        avg_dropoff = calculate_average_location(dropoffLocations, group_member_ids)

        # adds group statistics
        groupStats.append({
            "driverId": driverId,
            "riderIds": group["riderIds"],
            "averagePickup": avg_pickup,
            "averageDropoff": avg_dropoff
        })

    # Sort groups by Manhattan distance
    groupStats.sort(key=lambda g: calculate_manhattan_distance(g["averagePickup"], g["averageDropoff"]))
    return groupStats

for group in groups(data):
    print(group)

# POST request
requests.post(url, json = groups(data))