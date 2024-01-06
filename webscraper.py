import requests
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os 
""" import time
from urllib.parse import urlparse """
import re
import base64
#import bs4

driver = webdriver.Chrome()

# Creating a directory to save images
folder_name = 'pokemon_images'
if not os.path.isdir(folder_name):
    os.makedirs(folder_name)

def download_image(url, folder_name, num):
    try:
        if url.startswith("data:image"):
            # If it's a data URL, extract the image data
            _, image_data = url.split(",", 1)
            image_data = base64.b64decode(image_data)
        else:
            # If it's a regular URL, make a request to download the image
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses
            image_data = response.content

        # Ensure the folder exists
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        with open(os.path.join(folder_name, f"{num}.jpg"), 'wb') as file:
            file.write(image_data)

        print(f"Image {num} downloaded successfully to {folder_name}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image {num}: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

""" def download_image(url, folder_name, num):
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(folder_name, f"{num}.jpg"), 'wb') as file:
                file.write(response.content)
 """

# List of Generation 6 Pokemon names
pokemon_names = [
    "Chespin", "Quilladin", "Chesnaught", "Fennekin", "Braixen", "Delphox", "Froakie", "Frogadier", "Greninja",
    "Bunnelby", "Diggersby", "Fletchling", "Fletchinder", "Talonflame", "Scatterbug", "Spewpa", "Vivillon", 
    "Litleo", "Pyroar", "Flabébé", "Floette", "Florges", "Skiddo", "Gogoat", "Pancham", "Pangoro", "Furfrou",
    "Espurr", "Meowstic", "Honedge", "Doublade", "Aegislash", "Spritzee", "Aromatisse", "Swirlix", "Slurpuff",
    "Inkay", "Malamar", "Binacle", "Barbaracle", "Skrelp", "Dragalge", "Clauncher", "Clawitzer", "Helioptile",
    "Heliolisk", "Tyrunt", "Tyrantrum", "Amaura", "Aurorus", "Sylveon", "Hawlucha", "Dedenne", "Carbink",
    "Goomy", "Sliggoo", "Goodra", "Klefki", "Phantump", "Trevenant", "Pumpkaboo", "Gourgeist", "Bergmite",
    "Avalugg", "Noibat", "Noivern", "Xerneas", "Yveltal", "Zygarde", "Diancie", "Hoopa", "Volcanion"
]

# Set the total number of images to download
total_images = 7200

# Creating folders for each Pokemon
for pokemon_name in pokemon_names:
    folder_name = f'pokemon_images/{pokemon_name}'
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)


# Search and download images for each Pokemon until the total is reached
for i, pokemon_name in enumerate(pokemon_names):
    search_url = f"https://www.google.com/search?q={pokemon_name} Pokemon&source=lnms&tbm=isch"
    driver.get(search_url)

    try:
        # Wait for the search results to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.isv-r.PNCib.ViTmJb.BUooTd')))
    except TimeoutException:
        print(f"Timed out waiting for search results for {pokemon_name}")
        continue

    # Get the image URLs from the search results
    image_elements = driver.find_elements(By.CSS_SELECTOR, '.isv-r.PNCib.ViTmJb.BUooTd')

    for j, image_element in enumerate(image_elements[:100]):  # Change the number based on the number of images you want to download per Pokemon
        try:
            # Click on the image to open the preview
            image_element.click()
            
            # Wait for the preview to load
            preview_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'jlTjKd'))
            )

            # Find the img tag within the preview element
            # sFlh5c.pT0Scc.iPVvYb
            #img_element = preview_element.find_element(By.CLASS_NAME, 'sFlh5c.pT0Scc.iPVvYb')
            
            try:
                img_element = preview_element.find_element(By.TAG_NAME, 'img')
                # Extract the high-resolution image URL
                image_url = img_element.get_attribute('src')
            except Exception as e:
                print(f"Error getting src attribute")
            
            try:
                # Download the image
                download_image(image_url, f'pokemon_images/{pokemon_name}', i * 10 + j + 1)
            except Exception as e:
                print(f"Error in download function method call")
            
            print(f"Downloaded image {i * 10 + j + 1} for {pokemon_name}")
        except Exception as e:
            print(f"Skipping invalid image for {pokemon_name}")


# Close the browser
driver.quit()

""" try:
    while True:
        # Keep the script running
        time.sleep(1)
except KeyboardInterrupt:
    # Close the browser when you press Ctrl+C
    driver.quit() """
