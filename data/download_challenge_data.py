import os
import sys
import getpass
from pybis import Openbis

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} USERNAME")
    sys.exit(1)

# Get username from command line
USERNAME = sys.argv[1]

# Data to download (DO NOT CHANGE)
DATASET_PERM_ID = "20260819080658667-36"

# This will prompt you for your password in the console/Jupyter
o = Openbis("https://bs-dw114.ethz.ch/openbis/", verify_certificates=False)
password = getpass.getpass()
o.login(USERNAME, password, save_token=True)

try:
    print(f"Fetching dataset {DATASET_PERM_ID}...")
    dataset = o.get_dataset(DATASET_PERM_ID)

    destination = os.getcwd() + os.sep + 'data' + os.sep + 'challenge_data'
    os.makedirs(destination, exist_ok=True)

    print(f"Download started...")
    print(f"Downloading to: {destination}{os.sep}{DATASET_PERM_ID}")

    dataset.download(
        destination=destination,
        create_default_folders=False,
        wait_until_finished=True,
        workers=10
    )
    print(f"Successfully downloaded dataset to: {destination}{os.sep}{DATASET_PERM_ID}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    o.logout()
