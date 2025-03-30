team_email_map = {
    "Credit Cards": "b120061@iiit-bh.ac.in",
    "Debit Cards": "b120061@iiit-bh.ac.in",
    "Netbaking": "b120061@iiit-bh.ac.in",
    "Cheques": "b120061@iiit-bh.ac.in",
    "Accounts": "b120061@iiit-bh.ac.in",
    
}

def get_team_email_id(category):
    team_email = team_email_map.get(category)
    
    if team_email:
        return team_email
    else:
        return "b120061@iiit-bh.ac.in"