from collection import collectSubtoursFast

edges = [
    ("hi", "there"),
    ("there", "guy"),
    ("short", "one"),
    ("guy", "hi"),
    ("one", "short"),
]

print(collectSubtoursFast(edges, len(edges))) 
