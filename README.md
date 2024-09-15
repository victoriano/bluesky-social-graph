# Bluesky Follower Connections Script

This script fetches follower connections for a specified Bluesky user and saves the data in CSV format.

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
   - `pyproject.toml` (if using poetry for dependency management)

## Usage

1. **Open a terminal and navigate to the project directory.**

2. **Run the script:**

   ```bash
   python main.py
   ```

   **Optionally**, you can limit the number of followers to process:

   ```bash
   python main.py -n 100
   ```

3. **The script will generate an output file:**

   - `follower_connections.csv`: Contains the follower connections data in CSV format.

## Notes

- **Bluesky Credentials:** Make sure you have a Bluesky account and have generated an app password. The script uses the `atproto` library to interact with the Bluesky API, so ensure your credentials have the necessary permissions to fetch user data and follower information.

- **Environment Variables:** The script uses `python-dotenv` to load environment variables from the `.env` file. Make sure this file is properly set up with your credentials.

- **Error Handling:** The script will raise a `ValueError` if the environment variables `BLUESKY_USERNAME` and `BLUESKY_PASSWORD` are not set in the `.env` file or as environment variables.

## Example

1. Set up your `.env` file:

   ```
   BLUESKY_USERNAME=victoriano.bsky.social
   BLUESKY_PASSWORD=your_app_password
   ```

2. Run the script:

   ```bash
   python main.py -n 50
   ```

This command runs the script to process 50 followers using the credentials from the `.env` file.

---

Make sure to keep your `.env` file secure and never commit it to version control systems.