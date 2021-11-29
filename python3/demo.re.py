import re

msg = """
[/EN#285227/people A man] in [/EN#285235/clothing shorts] leans over [/EN#285230/vehicles/scene the rail of a pilot boat] .
"""
ress = re.findall('\[/EN#(\d+)/([/\w]+)\s*(.+?)\]', msg) # parse the triplets from msg
print(ress)
ress = re.findall('\[/EN#(\d+)/(\w+)\s*(.+?)\]', msg) # parse the triplets from msg
print(ress)
