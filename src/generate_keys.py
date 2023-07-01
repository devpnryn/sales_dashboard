import pickle
from pathlib import Path
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

names = ["Bhavya", "Mayank", "Govind", "Naryana"]
user_names = ["bv321", "mayan451", "govin763", "narayan213"]
passwords = ["bv#@!", "mayan$%!", "govin&^#", "narayan@!#"]
# password_hint:username_digits_shifted

# file_path = Path(__file__).parent / "hashed_pw.pkl"
file_path = Path(__file__).parent / "config.yaml"
with open('../config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    print(config)
    # yaml.dump(hashed_passwords, file, default_flow_style=False)
    # hashed_passwords, file)


print(hashed_passwords)
