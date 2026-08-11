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


def write_github_output(status, message):
    github_output = os.environ.get("GITHUB_OUTPUT")
    if not github_output:
        return
    with open(github_output, "a") as f:
        f.write(f"status={status}\n")
        f.write(f"message={message}\n")


def main():
    year, value = fetch_latest_gdp_growth()
    previous = load_previous_state()

    if previous is None:
        status = "baseline"
        message = f"Baseline saved: {year} -> {value}"
    elif previous.get("value") == value and previous.get("year") == year:
        status = "nochange"
        message = f"No change ({year}: {value})"
    else:
        status = "changed"
        message = (
            f"Change detected: {previous.get('year')} = "
            f"{previous.get('value')} -> {year} = {value}"
        )

    print(message)
    save_state(year, value)
    write_github_output(status, message)


if __name__ == "__main__":
    main()
