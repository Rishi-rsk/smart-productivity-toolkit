import re

def parse_query(query):
    query = query.lower()

    pattern = r"(\d+)\s*(usd|inr|eur|gbp)\s*(to)\s*(usd|inr|eur|gbp)"
    match = re.search(pattern, query)

    if match:
        amount = float(match.group(1))
        from_curr = match.group(2).upper()
        to_curr = match.group(4).upper()
        return amount, from_curr, to_curr

    return None