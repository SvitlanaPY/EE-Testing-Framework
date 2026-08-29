parametersList = [
    ("07450", "Ridgewood", "NJ", "flooranddecor"),
    ("77450", "Katy", "TX", "flooranddecor"),
    ("47025", "Lawrenceburg", "IN", "flooranddecor"),
    ("96001", "Redding", "CA", "flooranddecor"),
    ("30030", "Decatur", "GA", "flooranddecor"),
    ("50050", "Churdan", "IA", "flooranddecor"),
    ("9255700", "Moreno Valley", "CA", "flooranddecor")
]

parametersListNegative = [
    ("35001", "flooranddecor"),
    ("00000", "flooranddecor"),
    ("47o25", "flooranddecor"),
    ("", "flooranddecor"),
    ("4702", "flooranddecor")
    # ("77450", "flooranddecor")  #щоб негативний тест не пройшов, а впав з помилкою
]
