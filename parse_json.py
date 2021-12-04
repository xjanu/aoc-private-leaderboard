#!/usr/bin/env python3

import json
from datetime import datetime, timedelta

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

def member_time(member, day, part):
    timestamp = int(member["completion_day_level"][str(day)][str(part)]["get_star_ts"])
    start = int(datetime(2021, 12, day).timestamp())
    delta = timestamp - start
    # Seconds
    time = [f"{delta % 60:0>2}"]
    # Minutes
    delta //= 60
    if delta != 0:
        time.append(f"{delta % 60:0>2}:")
    # Hours
    delta //= 60
    if delta != 0:
        time.append(f"{delta % 60:0>2}:")
    # Days
    delta //= 24
    if delta != 0:
        time.append(f"{delta}d ")
    time.reverse()
    return "".join(time)

def get_links():
    with open("data/links.txt", "r") as linkfile:
        return {line.split()[0]: line.split()[1] for line in linkfile.readlines()}

def scores(members, startday=1):
    result = []
    daily_scores = day_score(members.values(), startday)
    links = get_links()

    for member in members.values():
        row = {"name": member["name"], "score": 0, "stars": [], "link": None}
        row["link"] = links.get(member["id"], None)

        for part1, part2 in daily_scores:
            if member["id"] in part1:
                row["score"] += len(members) - part1.index(member["id"])
                row["stars"].append(1)
            if member["id"] in part2:
                row["score"] += len(members) - part2.index(member["id"])
                row["stars"][-1] += 1

        result.append(row)

    result.sort(key=lambda x: x["score"], reverse=True)

    daily = []
    for part1, part2 in daily_scores:
        day = []
        day_no = len(daily) + startday
        for m_id in part2:
            member = members[m_id]
            day.append((member["name"],
                        member_time(member, day_no, 1),
                        member_time(member, day_no, 2)))
        for m_id in part1:
            if m_id in part2:
                continue
            member = members[m_id]
            day.append((member["name"],
                        member_time(member, day_no, 1),
                        None))
        daily.append(day)

    print(*daily, sep="\n")
    return result, daily

def parse(filename, startday=1):
    with open(filename, "r") as fp:
        data = json.loads(fp.read())

    members = data["members"]
    return scores(members, startday)

if __name__ == "__main__":
    print(parse("data/scores.json", startday=1))
