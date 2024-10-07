import json
import os

# Default configuration to create if config.json doesn't exist
DEFAULT_CONFIG = {
    "servers": [
        {
            "guild_id": 987654321098765432,
            "channels": [
                123456789012345678,
                234567890123456789
            ]
        }
    ],
    "bot_mention_id": 922889525666144308,
    "target_server_id": 987654321098765432,
    "bot_token": "YOUR_DISCORD_SELFBOT_TOKEN",
    "codes_file": "sent_codes.json"
}

DEFAULT_CONFIG_WITH_COMMENTS = """
{
  // List of servers to monitor
  "servers": [
    {
      "guild_id": 987654321098765432,  // Server ID
      "channels": [
        123456789012345678,  // Channel IDs to monitor
        234567890123456789
      ]
    }
  ],
  "bot_mention_id": 922889525666144308,  // ID of the bot to mention
  "target_server_id": 987654321098765432,  // Server ID where the command will be sent
  "bot_token": "YOUR_DISCORD_SELFBOT_TOKEN",  // Bot token to authenticate the bot
  "codes_file": "sent_codes.json"  // JSON file for storing sent codes
}
"""

# Path to the configuration and sent codes files
CONFIG_FILE = 'config.json'
CODES_FILE = 'sent_codes.json'

def create_example_config():
    """Creates an example config.json file if it doesn't exist."""
    with open(CONFIG_FILE, 'w') as f:
        f.write(DEFAULT_CONFIG_WITH_COMMENTS)
    print(f"⚠️ {CONFIG_FILE} not found. An example configuration file has been created.")
    return False

def validate_config(config):
    """Validates the structure of the config file."""
    required_keys = ["servers", "bot_mention_id", "target_server_id", "bot_token", "codes_file"]

    # Check for all required keys
    for key in required_keys:
        if key not in config:
            print(f"❌ Error: Missing key '{key}' in config.json.")
            return False

    # Check if "servers" contains a list of servers with proper guild_id and channels
    if not isinstance(config['servers'], list) or not all('guild_id' in server and 'channels' in server for server in config['servers']):
        print("❌ Error: 'servers' must be a list of objects, each containing 'guild_id' and 'channels'.")
        return False

    return True

def load_config():
    """Loads the config.json file and validates it. If it doesn't exist, create an example one."""
    if not os.path.exists(CONFIG_FILE):
        return create_example_config()

    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)

        if not validate_config(config):
            print(f"❌ Invalid configuration in {CONFIG_FILE}. Please fix it and try again.")
            return None
        return config

    except json.JSONDecodeError:
        print(f"❌ Error: {CONFIG_FILE} contains invalid JSON.")
        return None

def load_sent_codes():
    """Loads the sent_codes.json file. If it doesn't exist, create an empty one."""
    if not os.path.exists(CODES_FILE):
        print(f"⚠️ {CODES_FILE} not found. Creating a new one.")
        with open(CODES_FILE, 'w') as f:
            json.dump([], f)
        return set()

    try:
        with open(CODES_FILE, 'r') as f:
            sent_codes = set(json.load(f))
        return sent_codes

    except json.JSONDecodeError:
        print(f"❌ Error: {CODES_FILE} contains invalid JSON. Creating a new empty file.")
        with open(CODES_FILE, 'w') as f:
            json.dump([], f)
        return set()

def save_sent_codes(sent_codes):
    """Saves the sent codes to sent_codes.json."""
    with open(CODES_FILE, 'w') as f:
        json.dump(list(sent_codes), f)
