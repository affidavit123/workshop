import json
import os
import urllib.request

API_URL = (
    "https://api.worldbank.org/v2/country/MNG/indicator/"
    "NY.GDP.MKTP.KD.ZG?format=json&mrv=1"
)
STATE_FILE = "mini_state.json"


def fetch_latest_gdp_growth():
    with urllib.request.urlopen(API_URL) as response:
        data = json.loads(response.read().decode())

    # World Bank returns [metadata, [records]]
    record = data[1][0]
    return record["date"], record["value"]


def load_previous_state():
    if not os.path.exists(STATE_FILE):
        return None
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(year, value):
    with open(STATE_FILE, "w") as f:
        json.dump({"year": year, "value": value}, f, indent=2)


def main():
    year, value = fetch_latest_gdp_growth()
    previous = load_previous_state()

    if previous is None:
        print(f"Baseline saved: {year} -> {value}")
    elif previous.get("value") == value and previous.get("year") == year:
        print(f"No change ({year}: {value})")
    else:
        print(
            f"Change detected: {previous.get('year')} = "
            f"{previous.get('value')} -> {year} = {value}"
        )

    save_state(year, value)


if __name__ == "__main__":
    main()
