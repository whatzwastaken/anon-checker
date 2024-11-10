import aiohttp
import asyncio
from bs4 import BeautifulSoup
from tqdm import tqdm
from pystyle import Colors, Colorate, Center
from pyrogram import Client, errors
from pyrogram.types import InputPhoneContact
import logging
import time
import os
import pyfiglet  


logging.basicConfig(level=logging.ERROR)


api_id = ''
api_hash = ''

def load_numbers(file_path):
    with open(file_path, "r") as file:
        return [line.strip()[4:] for line in file if line.startswith("+888")]
async def fetch_html(session, number):
    url = f"https://fragment.com/numbers?query={number}"
    async with session.get(url) as response:
        return await response.text()


def parse_html(html, number):
    soup = BeautifulSoup(html, "html.parser")
    row = soup.select_one("tbody.tm-high-cells tr.tm-row-selectable")

    if row:
        price = row.select_one("td.thin-last-col .table-cell-value").text.strip()
        status_text = row.select_one(".wide-last-col .table-cell-value").text.strip()
        status = "Available" if status_text == "For sale" else "Not available"
    else:
        price = "N/A"
        status = "Not available"

    return {
        "Number": f"+888{number}",
        "Price": price,
        "Status": status
    }


async def check_registration(client, number):
    retries = 3  
    for attempt in range(retries):
        try:
            contact = InputPhoneContact(phone=number, first_name="Test", last_name="User")
            result = await client.import_contacts([contact])
            contact_info = result.users[0] if result.users else None

            if contact_info:
                telegram_status = "Registered"
                user_id = contact_info.id
                username = contact_info.username if contact_info.username else "N/A"
            else:
                telegram_status = "Not registered"
                user_id = "N/A"
                username = "N/A"

            return telegram_status, user_id, username

        except errors.FloodWait as e:

            print(f"FloodWait Error: Telegram requests a wait of {e.value} seconds.")
            await asyncio.sleep(e.value)
            continue  

        except Exception as e:

            return f"Error: {e}", "N/A", "N/A"
    

    return "FloodWait Timeout", "N/A", "N/A"



def display_results(numbers_data):
    for item in numbers_data:

        status_color = Colors.green if item["Status"] == "Available" else Colors.red
        reg_color = Colors.green if item["Telegram"] == "Registered" else Colors.red
        number_color = Colors.cyan
        price_color = Colors.yellow


        output = (
            f"{Colors.cyan}Number: {item['Number']}\n"
            f"{Colors.yellow}Price: {item['Price']} FRG\n"
            f"{Colorate.Color(status_color, 'Status: ' + item['Status'], True)}\n"
            f"{Colorate.Color(reg_color, 'Telegram: ' + item['Telegram'], True)}\n"
            f"{Colors.green}User ID: {item['User_ID']}\n"
            f"{Colors.green}Username: @{item['Username']}"
        )
        print(Center.XCenter(output))
        print(f"{Colors.purple}-" * 40)


def write_results_to_file(registered_data, not_registered_data):
    with open("result.txt", "w") as file:
        file.write("Registered Accounts:\n")
        for item in registered_data:
            file.write(f"{item['Number']} - {item['Price']} FRG - {item['User_ID']} - {item['Username']}\n")

        file.write("\nNot Registered Accounts:\n")
        for item in not_registered_data:
            file.write(f"{item['Number']} - {item['Price']} FRG - {item['User_ID']} - {item['Username']}\n")


async def main():
    numbers = load_numbers("nums.txt")

    # Initialize Pyrogram client
    async with Client('anon', api_id=api_id, api_hash=api_hash) as client:
        async with aiohttp.ClientSession() as session:
            numbers_data = []
            registered_data = []
            not_registered_data = []

 
            intro1 = pyfiglet.figlet_format("@whatz1337", font='slant')
            print(Colorate.Horizontal(Colors.cyan_to_blue, intro1, 1))
            intro = pyfiglet.figlet_format("ANON CHECKER", font='slant')
            print(Colorate.Horizontal(Colors.purple_to_blue, intro, 1))

           
            with tqdm(total=len(numbers), desc="Checking numbers", bar_format="{l_bar}{bar}| {remaining}", 
                      ncols=100, 
                      dynamic_ncols=True, 
                      colour='cyan', 
                      position=0) as pbar:
                for number in numbers:
                    html = await fetch_html(session, number)
                    parsed_data = parse_html(html, number)

                    
                    telegram_status, user_id, username = await check_registration(client, f"+888{number}")
                    parsed_data["Telegram"] = telegram_status
                    parsed_data["User_ID"] = user_id
                    parsed_data["Username"] = username

                   
                    if telegram_status == "Registered":
                        registered_data.append(parsed_data)
                    else:
                        not_registered_data.append(parsed_data)

                    numbers_data.append(parsed_data)
                    pbar.update(1)
                    time.sleep(0.05)  

         
            print(Colorate.Horizontal(Colors.purple_to_blue, pyfiglet.figlet_format("Results", font='slant'), 1))
            display_results(numbers_data)

            
            write_results_to_file(registered_data, not_registered_data)
            print(f"\n{Colors.green}Results written to result.txt")
            os.system("start result.txt")

asyncio.run(main())
