
# **ANON CHECKER**

## **Installation Instructions**

### 1. Install the required libraries:

You can install all the dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 2. Create a `nums.txt` file:

Create a `nums.txt` file with a list of numbers you want to check. The numbers must start with `+888` (e.g., `+888123456789`).

### 3. Fill in the API credentials:

- Go to [Telegram API](https://my.telegram.org/auth) to get your `api_id` and `api_hash`.
- Set them in the script or create a `.env` file to securely store them.

### 4. Run the script:

```bash
python anon_checker.py
```

---

## **Example Output**

- **Registered Numbers** are highlighted in **green**.
- **Non-registered Numbers** are highlighted in **red**.

---

## **Screenshots:**

### **Program in Action**
![Program in Action](https://i.imgur.com/ecqgs6Y.png)

### **Result Output**

After running the script, a `result.txt` file is generated with details on the registration status of the numbers.

---

## **Commands & Functions:**

- `fetch_html(session, number)`: Fetches the HTML content for a given phone number.
- `parse_html(html, number)`: Extracts the price and availability of the number from the HTML.
- `check_registration(client, number)`: Checks the registration status of the number on Telegram.
- `display_results(numbers_data)`: Displays the parsed results with styling.
- `write_results_to_file(registered_data, not_registered_data)`: Saves the results in a `result.txt` file.

---

## **Contribute:**

1. **Fork the repository.**
2. **Create a new branch** for your changes.
3. **Commit your changes** and **push** them to your fork.
4. **Submit a pull request** to the main repository.

---

## **License:**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## **Acknowledgments:**

- Thanks to the authors of the libraries used in this project.
- Special thanks to `pyrogram`, `beautifulsoup`, and `tqdm` for making this project possible!
