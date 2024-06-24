# Serif Health Takehome Challenge

This project is designed to parse a large JSON index file and extract relevant machine-readable file URLs representing Anthem PPO network in New York state.

## Sample Output

You can go to the `output/` folder to look at a sample output of URLs corresponding to Anthem's PPO.

## Setup Instructions

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/bnkc/serif-challenge.git
    cd serif-challenge
    ```
2. **Create virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
 
3. **Install Dependencies:**
    ```sh
    pip install -e .
    ```

4. **Download Anthem machine readable index file:**
    ```sh
    python setup.py install
    ```
    **NOTE:** This will take awhile, if you already have the data installed, create a `downloads/2024-06-01_anthem_index.json.gz` in the root directory.



3. **Run the Script:**
    ```sh
    python main.py
    ```
    The output will be a JSON file containing the list of relevant URLs, saved in the `output/` directory. The script can take *~100 seconds* to run.


## Breakdown

...

## Time Taken

- **Development Time:** ~2 hours
- **Execution Time:** Depends on the file size

## Tradeoffs

- Used `ijson` for efficient streaming of large JSON files to handle memory constraints.
- Assumed URLs containing "ANTHEM" and "PPO" in their plan names are relevant.

## Future Improvements

- Expand test coverage.
- Handle more complex schemas and additional edge cases.
- Optimize performance further for even larger datasets.
