import csv


def clean_entry(entry):
    """
    Clean unnecessary white space in entry data
    """
    if entry["ActionType"] != "Type":
        entry["Data"] = entry["Data"].strip()
    if entry["ActionType"] in ["Trigger", "BranchTrigger", "Click", "RClick", "Jump", "Drag", "MouseAction", "Value", "MoveTo", "Scroll"]:
        entry["Data"] = entry["Data"].replace(" ", "")
    return entry


def read_data(file_name="test_data.csv"):
    with open(file_name, 'r') as file:
        # Remove white line and comment line
        csv_data = []

        for line in file:
            line = line.strip()
            if line != "" and not line.startswith('#'):
                csv_data.append(line)

        csv_reader = csv.DictReader(csv_data)
        csv_data = list(csv_reader)

        i = 0
        while i < len(csv_data):
            entry = clean_entry(csv_data[i])
            print(entry)
            if entry["ActionType"] == "File":
                other_data = read_data(entry["Data"].strip())
                del csv_data[i]
                csv_data[i:i] = other_data
            i += 1
        return csv_data


def write_date(data, file_name="test_write_data.csv"):
    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)
