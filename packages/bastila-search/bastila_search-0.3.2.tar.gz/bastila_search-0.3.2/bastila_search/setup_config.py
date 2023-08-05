# setup_config.py
import json

def main():
    bastila_key = input("Enter your BASTILA_KEY: ")
    block_on_failure = input("Should the hook block commits on failure? (true/false): ")

    config = {
        "BASTILA_KEY": bastila_key,
        "BLOCK_ON_FAILURE": block_on_failure
    }

    with open("config.json", "w") as file:
        json.dump(config, file)

    print("Configuration saved!")

if __name__ == "__main__":
    main()
