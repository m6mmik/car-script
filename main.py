from bs4 import BeautifulSoup
import requests
import re
import discord
import os
from discord.ext import commands

def laoautod():
    url="https://www.topauto.ee/et/uued-laoautod?id=2313&windowType=&ok=1&mark_id=147&model_id=&gearbox_id=0&fuel_id=10&bridge_id=0&price_min=&price_max=" #pistikhübriid
    #url="https://www.topauto.ee/et/uued-laoautod?id=2313&windowType=&ok=1&mark_id=147&model_id=&gearbox_id=0&fuel_id=0&bridge_id=0&price_min=&price_max=" # kõik
    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text

    # Parse the html content
    soup = BeautifulSoup(html_content, "lxml")
    #print(soup.prettify()) # print the parsed data of html

    #cars_list = soup.find('div', class_='importedCarsListContainer usedCarsList wrap')

    cars_list = soup.find_all("div", class_="car")


    for car_div in cars_list:
        onclick_value = car_div.get('onclick')
        link_match = re.search(r"document\.location='(.*?)'", onclick_value)
        car_link = link_match.group(1) if link_match else None

        # Extract the car name
        car_name = car_div.find('h2').text.strip()

        # Extract fuel type, gearbox, power, fuel consumption, CO2 emissions
        info_divs = car_div.find_all('div', class_=re.compile('icon icon.*'))
        info_values = [info.text.strip() for info in info_divs]
        fuel_type = info_values[0] if len(info_values) > 0 else 'N/A'
        gearbox = info_values[1] if len(info_values) > 1 else 'N/A'
        wheel_drive = info_values[2] if len(info_values) > 2 else 'N/A'
        power = info_values[3] if len(info_values) > 3 else 'N/A'
        fuel_consumption = info_values[4] if len(info_values) > 4 else 'N/A'
        co2 = info_values[5] if len(info_values) > 5 else 'N/A'

        # Extract the price
        price = car_div.find('div', class_='priceInfo').text.strip()

        # Extract the monthly payment info
        monthly_payment = car_div.find('div', class_='mounthlyPaymentInfo').text.strip()

        # Print the extracted information
        print(f"Car Name: {car_name}")
        print(f"Link: {car_link}")
        print(f"Fuel Type: {fuel_type}")
        #print(f"Gearbox: {gearbox}")
        #print(f"Wheel Drive: {wheel_drive}")
        print(f"Power: {power}")
        #print(f"Fuel Consumption: {fuel_consumption}")
        #print(f"CO2 Emissions: {co2}")
        print(f"Price: {price}")
        #print(f"Monthly Payment: {monthly_payment}")
        print("\n")
        send_message(car_name + " "+ car_link)
    #print(cars_list)

def formentor_pistik():
    url="https://www.topauto.ee/et/cupra-formentor-uus-hinnad"

    html_content = requests.get(url).text

    # Parse the html content
    soup = BeautifulSoup(html_content, "lxml")
    #print(soup.prettify()) # print the parsed data of html

    cars_list = soup.find('table', class_='responsive priceList')
    send_message("FORMENTOR PISTIKHÜBRIID = "+str(cars_list.text.__contains__("pistikhübriid")))
    print("FORMENTOR PISTIKHÜBRIID = "+str(cars_list.text.__contains__("pistikhübriid")))

def leon_pistik():
    url="https://www.topauto.ee/et/cupra-cupra-leon-sportstourer-uus-hinnad"

    html_content = requests.get(url).text

    # Parse the html content
    soup = BeautifulSoup(html_content, "lxml")
    #print(soup.prettify()) # print the parsed data of html

    cars_list = soup.find('table', class_='responsive priceList')
    send_message("LEON PISTIKHÜBRIID = "+str(cars_list.text.__contains__("pistikhübriid")))
    print("LEON PISTIKHÜBRIID = "+str(cars_list.text.__contains__("pistikhübriid")))

def scan():
    

    print("__LAOAUTOD__")
    laoautod()
    print("__LAOAUTOD__"+"\n")

    formentor_pistik()
    leon_pistik()


def send_message(MESSAGE):
    # Replace with your bot token
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')

    # Replace with the user ID of the person you want to message
    USER_ID = 355234522582876162  # User ID as an integer

    # Initialize bot
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')

        # Fetch user by ID
        user = await bot.fetch_user(USER_ID)
        
        if user:
            try:
                # Send the message to the user
                await user.send(MESSAGE)
                print(f"Message sent to {user.name}")
            except Exception as e:
                print(f"Failed to send message: {e}")
        else:
            print("User not found")

        # Close the bot once the message is sent
        await bot.close()

    # Run the bot
    bot.run(TOKEN)

scan()


