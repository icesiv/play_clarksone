# ToDo
For the first bot you're working on. Have it look like this please few things have been changed. Bot scraps in to only 1 Excel file , Bat replaces old scrap with new scrap and runs automatically




The crawler should convert the data in to an Excel sheet with this information and format 3 times a day. 

Key Points before you start this project.

- Scraper needs to collect SKU , Style ,UPC , Quantity Availability , Title , Cost , MSRP. It doesn't hurt to add more information you can see the scrapper I sent you for reference.
- Scraper needs to convert the above to Excel sheet
- Scraper has to run twice a day
- Try to make it as similar as you can to our current scrapper.



# HOW TO RUN THIS SCRAPER

1. Download Python 3.6+ from [here](https://www.python.org/downloads/) and install [pip](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/) and [virtualenv](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/).

2. Run the file `setup.bat` by double clicking it.

3. Copy the contents of `config_template.json` into a new file called `config.json` (must be on the same level as `config_template.json`). Input the corresponding values in this file. More info [below](#config-file-settings-explained).

4. (Optional) You can choose to discard the `config_template.json` once above is completed.

5. Run the file `run_scraper.bat` by double clicking it to start the scraper.

6. Program outputs will be generated in a folder named `output_data`

# Config File Contents Explained

- `USERNAME` - Username used for login on the website https://sanukus.deckersb2b.deckers.com/#/login

- `PASSWORD` - Password used for login on the website https://sanukus.deckersb2b.deckers.com/#/login
