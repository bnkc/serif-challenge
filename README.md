# Serif Health Takehome Interview

## Project Description

This project is designed to parse a large JSON index file and extract relevant machine-readable file URLs representing Anthem PPO network in New York state.

## Setup Instructions

1. **Clone the Repository:**
    ```sh
    git clone <your_repo_url>
    cd serif_health_takehome
    ```

2. **Install Dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the Script:**
    ```sh
    python main.py
    ```

## File Structure

- `data/`: Directory for input data files.
- `src/`: Directory for source code.
- `tests/`: Directory for test cases.
- `README.md`: Project documentation.
- `requirements.txt`: Python dependencies.
- `setup.py`: Setup script for the project.
- `main.py`: Entry point for running the script.

## Output

The output will be a JSON file containing the list of relevant URLs, saved in the `output` directory.

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
