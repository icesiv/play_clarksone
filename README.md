# HOW TO RUN THIS SCRAPER

1. Download Python 3.6+ from [here](https://www.python.org/downloads/) and install [pip](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/) and [virtualenv](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/).

2. Run the file `setup.bat` by double clicking it.

3. Download [chromedriver](https://chromedriver.chromium.org/) for the current version of your chrome instance and place the unzipped executable in the same folder level as `setup.bat`.

4. Copy the contents of `config_template.json` into a new file called `config.json` (must be on the same level as `config_template.json`). Input the corresponding values in this file. More info [below](#config-file-settings-explained).

5. (Optional) You can choose to discard the `config_template.json` once above is completed.

6. Run the file `run_scraper.bat` by double clicking it to start the scraper.

7. Program outputs will be generated in a folder named `output_data`

# Config File Contents Explained

- `USERNAME` - Username used for login on the website https://sanukus.deckersb2b.deckers.com/#/login

- `PASSWORD` - Password used for login on the website https://sanukus.deckersb2b.deckers.com/#/login

- `DELETE_DB_RECORD_OLDER_THAN_DAYS` - Ensures the database records older than these number of days are deleted from record. (Note: Excel ouptut files will remain unchanged)

- `UPDATE_INVENTORY_HOURS` - Ensures the records fetched for the Excel output report should be no older than these hours old
