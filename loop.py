# Quick hack to make the SQL insert

def assign_state(recipient):
    """
    Try to assign a state to the recipient. If not possible, return "NULL".
    States have alphabetical precedence.
    """
    states = [
        "Alabama", "Alaska", "Arizona",
        "Arkansas", "California", "Colorado",
        "Connecticut", "Delaware", "Florida",
        "Georgia", "Hawaii", "Idaho",
        "Illinois", "Indiana", "Iowa",
        "Kansas", "Kentucky", "Louisiana",
        "Maine", "Maryland", "Massachusetts",
        "Michigan", "Minnesota", "Mississippi",
        "Missouri", "Montana", "Nebraska",
        "Nevada", "New Hampshire", "New Jersey",
        "New Mexico", "New York", "North Carolina",
        "North Dakota", "Ohio", "Oklahoma",
        "Oregon", "Pennsylvania", "Rhode Island",
        "South Carolina", "South Dakota", "Tennessee",
        "Texas", "Utah", "Vermont",
        "Virginia", "Washington", "West Virginia",
        "Wisconsin", "Wyoming",
    ]
    for s in states:
        if s in recipient:
            return "'" + s + "'"
    return "NULL"

def donor_cause_area_url(area):
    if area == "Criminal Justice":
        return "'http://www.arnoldfoundation.org/initiative/criminal-justice/'"
    if area == "Education":
        return "'http://www.arnoldfoundation.org/initiative/education/'"
    if area == "Evidence-Based Policy and Innovation":
        return "'http://www.arnoldfoundation.org/initiative/evidence-based-policy-innovation/'"
    if area == "New Initiatives":
        return "'http://www.arnoldfoundation.org/initiative/venture-development/'"
    if area == "Research Integrity":
        return "'http://www.arnoldfoundation.org/initiative/research-integrity/'"
    if area == "Sustainable Public Finance":
        return "'http://www.arnoldfoundation.org/initiative/sustainable-public-finance/'"
    else:
        return "NULL"

with open("grants.tsv", "r") as f:
    for line in f:
        area, recipient, year, amount = line.strip().split("\t")

        print("""    ('Laura and John Arnold Foundation','{donee}',{amount},'{donation_date}-01-01','year','donation log','{cause_area}','http://www.arnoldfoundation.org/grants/',{donor_cause_area_url},'United States',{affected_states}),""".format(
                donee=recipient,
                amount=amount,
                donation_date=year,
                cause_area=area,
                donor_cause_area_url=donor_cause_area_url(area),
                affected_states=assign_state(recipient)
            ))
