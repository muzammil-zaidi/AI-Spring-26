days = ["Mon", "Tue", "Wed", "Thu", "Fri"]

shirts = ["S1", "S2", "S3", "S4", "S5"]
pants = ["P1", "P2", "P3"]
sq = ["SQ1", "SQ2"]

def is_valid(schedule, day, outfit):
    if day in ["Mon", "Thu"] and "SQ" in outfit:
        return False
    if day == "Fri" and "SQ" not in outfit:
        return False

    for d in schedule:
        if schedule[d] == outfit:
            return False

    return True

def backtrack(schedule, s_used, p_used, sq_used, i):
    if i == len(days):
        print(schedule)
        return

    day = days[i]

    for s in shirts:
        for p in pants:
            if s not in s_used and p not in p_used:
                outfit = s + "+" + p
                if is_valid(schedule, day, outfit):
                    schedule[day] = outfit
                    backtrack(schedule, s_used+[s], p_used+[p], sq_used, i+1)
                    del schedule[day]

    for q in sq:
        if q not in sq_used:
            if is_valid(schedule, day, q):
                schedule[day] = q
                backtrack(schedule, s_used, p_used, sq_used+[q], i+1)
                del schedule[day]

backtrack({}, [], [], [], 0)
