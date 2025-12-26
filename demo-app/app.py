import csv
# demo change for CI test

TEST_FILE = "demo_app/test_keys.csv"

def load_test_keys():
    keys = []
    with open(TEST_FILE, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            keys.append(row)
    return keys

def main():
    test_keys = load_test_keys()
    print("Loaded test keys:\n")

    for item in test_keys:
        print(f"{item['type']} -> {item['key']}")

if __name__ == "__main__":
    main()
