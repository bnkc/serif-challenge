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


## Data Exploration

I chose to write this project in **Python** to enable rapid development. Given more time, I would have preferred to rewrite it in **Go** for performance benefits.

During data exploration, I quickly noticed numerous duplicates, varying URL structures, and inconsistent descriptions. I started by examining the `reporting_plans`. According to the [CMS' transparency in coverage repository](https://github.com/CMSgov/price-transparency-guide/tree/master/schemas/table-of-contents), reporting plans within the same list share the same in-network negotiated rates. Some plan names included keywords like **ANTHEM** and **PPO**, so I filtered the `in_network_files` by ensuring that `reporting_plans` contained at least one plan with these keywords. For example, `PPO - JOHNSTONE MOYER INC - ANTHEM`.

Next, I examined the `in_network_files`. The descriptions often contained references to various businesses and regions. Initially, I searched for `in_network_files/locations` where the descriptions included keywords like **"PPO"** and **"New York"**. This yielded results such as `Highmark BS Northeastern NY: Highmark Blue Shield of Northeastern New York - PPO`.

However, further investigation revealed that Highmark and Anthem are distinct entities. Although both operate under the Blue Cross Blue Shield brand, they have separate policies, networks, and plan offerings. Consequently, I decided to focus solely on Anthem plans, excluding those from other states and networks.

This led me to the `In-Network Negotiated Rates` Files. These files frequently appeared, and their URL structure typically follows this pattern: `https://anthembcca.mrf.bcbs.com/{date}_{???}_{plan_code}_in-network-rates_{part}.json.gz?&Expires={expiration_date}&Signature={signature}&Key-Pair-Id={key_pair}`. Through the Anthem EIN lookup, I discovered that the ??? represents a state code. For New York, this code starts with **39**, such as **39D0**, **39X0**, and **39B0**. Due to time constraints, I couldn't explore this further, but I decided to filter based on these digits and validate the links by checking the expiration date. The part indicates that these files are segments of a larger in-network file.

Despite encountering duplicates across various plan_id's, I noticed that the Transparency in Coverage repository also reflects this issue. Therefore, I created a hashset of these location URLs to manage duplicates. If given more time, I would have delved deeper into the data before finalizing my approach.

## Time Taken

- **Development Time:** ~2 hours
- **Execution Time:** ~100 seconds

## Tradeoffs

- Used `ijson` package for efficient streaming of large JSON files to handle memory constraints.
- Used `gzip` to read directly from the zipped file to avoid uncompressing it.
- Decided that `in_network_files/descriptions` are **NOT** useful for reasons listed above
- **No Tests:** Ideally with more time, I would like to spin up a test suite to ensure we handle failures gracefully
- **More logging:** I introduced some basic logging but it would be nice to have more thorough logging by using something like [tqdm](https://github.com/tqdm/tqdm) for a progress bar.
- **Latency**: At this time, the script can be rather slow (~100 s). we can drastically speed this up with concurrency, and a compiled language.
- **Storage**: For now we are saving to outputs to a JSON file. In a real application, we might store the output in a Document Store, or a relational database. We would also need to store the Index somewhere such as S3, or our own storage.
- **Robustness**: I am using [Pydantic](https://github.com/pydantic/pydantic) for data validation. Ideally we have response schemas too, if this were an API. additionally, it would be nice to have more thorough error handling.

## Future Improvements

- Expand test coverage.
- Handle more complex schemas and additional edge cases.
- Optimize performance further for even larger datasets.
- Do a much deeper dive on the data itself for a broader understanding of the problem.
