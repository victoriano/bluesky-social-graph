# Bluesky Relationship Connections Script

This script retrieves follower or following relationships for a specified Bluesky user, finds mutual connections, and saves the data in CSV format.

## Features

- **Retrieve followers or following lists** for a given user.
- **Find mutual connections** between your network and the users in the retrieved list.
- **Customize the number of users** to process.
- **Output data in CSV format**, with mutual connections formatted as per specific requirements.

## Setup

1. **Install the required dependencies:**

   ```bash
   pip install atproto python-dotenv
   ```

   Or if you're using Poetry:

   ```bash
   poetry add atproto python-dotenv
   ```

2. **Create a `.env` file in the project directory with your Bluesky credentials:**

   ```
   BLUESKY_USERNAME=your_bluesky_handle
   BLUESKY_PASSWORD=your_app_password
   ```

   Replace `your_bluesky_handle` and `your_app_password` with your actual Bluesky credentials.

3. **Ensure you have the following files in your project directory:**

   - `main.py`
   - `.env`
   - `pyproject.toml` (if using Poetry for dependency management)

## Usage

1. **Open a terminal and navigate to the project directory.**

2. **Run the script:**

   ```bash
   python main.py
   ```

   By default, the script will:

   - Retrieve information about your **following** relationships.
   - Process **10** users.

3. **Optional Parameters:**

   - **Specify the number of users to retrieve (`-n` or `--number`):**

     ```bash
     python main.py -n 50
     ```

     This command processes 50 users instead of the default 10.

   - **Specify the relationship type (`-r` or `--relationship`):**

     - To retrieve **followers**:

       ```bash
       python main.py -r followers
       ```

     - To retrieve **following** (default behavior):

       ```bash
       python main.py -r following
       ```

   - **Combine both options:**

     ```bash
     python main.py -n 50 -r followers
     ```

4. **The script will generate an output file:**

   - `following_connections.csv` or `follower_connections.csv`, depending on the relationship type specified.

   The CSV file contains the following columns:

   - **Relationship Type**: Indicates whether the user is a 'Follower' or 'Following'.
   - **Username**: The handle of the user.
   - **Mutual Connections**: A list of mutual connections in a specific format.

## Output Format

- The **`Mutual Connections`** field in the CSV file is formatted as:

  ```
  ["username1","username2","username3"]
  ```

  - **Each username inside the array is enclosed in double quotes**.
  - **The entire field is enclosed in double quotes** due to CSV formatting conventions.

- **Note on Double Quotes:**

  - Because of CSV escaping rules, double quotes inside fields are represented by two consecutive double quotes (`""`).
  - So, in the CSV file, the `Mutual Connections` field will appear as:

    ```
    "[""username1"",""username2"",""username3""]"
    ```

  - This is normal and expected when fields contain double quotes.

- **Example Entry:**

  ```csv
  "Following","alice.bsky.sh","[""bob.bsky.social"",""charlie.bsky.social""]"
  ```

## Notes

- **Bluesky Credentials:** Ensure your Bluesky account has the necessary permissions to fetch user data and follower/following information.

- **Environment Variables:** The script uses `python-dotenv` to load environment variables from the `.env` file.

- **Error Handling:** The script raises a `ValueError` if `BLUESKY_USERNAME` and `BLUESKY_PASSWORD` are not set.

- **Progress Monitoring:** The script prints a message to the console each time it processes a new user.

- **Output Files Named According to Relationship Type:**

  - The output CSV file is named based on the relationship type:

    - If retrieving **followers**, the output file is `follower_connections.csv`.
    - If retrieving **following**, the output file is `following_connections.csv`.

- **Rate Limit Considerations:**

  - Fetching followings for each user may result in a large number of API calls.
  - Be mindful of any rate limits imposed by the Bluesky API.
  - If processing a large number of users, consider implementing rate limiting or exception handling for rate limit exceptions.

## Sample Output

**Partial Content of `following_connections.csv`:**

```
"Following","alice.bsky.sh","[""bob.bsky.social"",""charlie.bsky.social""]"
```

- **Explanation:**

  - **`Relationship Type`**: Indicates the relationship type selected (`Following` in this example).
  - **`Username`**: The handle of the user being processed.
  - **`Mutual Connections`**: A list of mutual connections with the user, formatted as specified.

## Example

1. **Set up your `.env` file:**

   ```
   BLUESKY_USERNAME=your_bluesky_handle
   BLUESKY_PASSWORD=your_app_password
   ```

2. **Run the script to retrieve 20 followers:**

   ```bash
   python main.py -n 20 -r followers
   ```

3. **The script will:**

   - Process each user, printing progress messages to the console.
   - Save the results to `follower_connections.csv`.

4. **Open the CSV file to view the results.**

## Important

- **Keep your `.env` file secure and avoid committing it to version control systems or sharing it publicly.**

- **Be cautious when sharing the output CSV files if they contain sensitive or personal information.**

---

If you have any questions or need further assistance, feel free to reach out!