#!/usr/bin/env python3

import json

def day_score(members, startday=1):
    result = []

    for day in range(startday, 26):
        result.append(([],[]))
        for part in range(2):
            this = []
            for member in members:
                time = member["completion_day_level"].get(str(day), {}).get(str(part+1), {}).get("get_star_ts", None)
                if time is not None:
                    this.append((time, member["id"]))
            this.sort()
            result[-1][part].extend(map(lambda x: x[1], this))

    return result

def scores(members, startday=1):
    result = []
    daily_scores = day_score(members, startday)

    for member in members:
        row = {"name": member["name"], "score": 0, "stars": []}

        for part1, part2 in daily_scores:
            if member["id"] in part1:
                row["score"] += len(members) - part1.index(member["id"])
                row["stars"].append(1)
            if member["id"] in part2:
                row["score"] += len(members) - part2.index(member["id"])
                row["stars"][-1] += 1

        result.append(row)

    result.sort(key=lambda x: x["score"], reverse=True)
    return result

def parse(filename, startday=1):
    with open(filename, "r") as fp:
        data = json.loads(fp.read())

    members = data["members"]
    return scores(members.values(), startday)

if __name__ == "__main__":
    print(parse("data/scores.json"))
