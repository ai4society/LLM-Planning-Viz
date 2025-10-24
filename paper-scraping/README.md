# arXiv Paper Extraction

This folder contains scripts to perform arXiv paper extraction: automating the process of retrieving, filtering, and storing relevant academic papers from the arXiv database. The script is implemented in Python and utilizes components (details below) to ensure efficient and consistent operation.

## `arxiv_extractor_db.py`

This [arXiv](https://arxiv.org/) paper extraction script provides an automated, efficient solution for regularly updating a database of relevant academic papers. This tool significantly streamlines the process of staying updated with the latest research in specified fields of interest.

### Configuration Management

The script utilizes a JSON configuration file (`config.json`) and environment variables for flexible setup across different environments. This approach allows for easy customization and portability. The configuration includes:

- Log directory
- Output directory
- Database file location

An environment variable (`ARXIV_EXTRACTOR_BASE_DIR`) can be used to specify the base directory, enhancing flexibility for different deployment scenarios.

### CRON Scheduling

The script is designed to be run as a [CRON job](https://en.wikipedia.org/wiki/Cron), allowing for automated, periodic execution. This ensures regular updates to the paper database without manual intervention. The CRON job can be configured to run at specified intervals (e.g., daily or weekly). For example, to set the script to run every day at 2:00 AM, the following command in the crontab would suffice:

```shell
ARXIV_EXTRACTOR_BASE_DIR=/path/to/base/directory
0 2 * * * /usr/bin/python3 /path/to/arxiv_extractor.py
```

### Script Functionality

The script interacts with the arXiv API using the [`arxiv` Python package](https://pypi.org/project/arxiv/). It performs the following steps:

1. Executes predefined search queries targeting relevant categories and keywords.
2. Retrieves metadata for papers matching these queries.
3. Applies additional relevance filtering based on specified keywords.

This process ensures that only papers pertinent to the areas of interest (e.g., large language models and automated planning) are collected.

#### Database Management

A [SQLite database](https://docs.python.org/3/library/sqlite3.html) is employed for persistent storage of paper metadata. The database functionality includes:

1. Initializing the database and creating necessary tables if they don't exist.
2. Checking for the existence of papers to avoid duplication.
3. Inserting new papers into the database.

This approach allows for efficient storage and retrieval of paper information across multiple script executions.

#### Deduplication

To prevent redundant entries, the script implements a deduplication process:

1. For each retrieved paper, it checks if the paper already exists in the database.
2. Only papers not present in the database are added to the list of new papers and inserted into the database.

This ensures that each run of the script only processes and reports genuinely new papers.

#### Output Generation

The script generates two types of output:

1. A CSV file containing details of newly found papers, created only when new papers are discovered.
2. Log files recording the script's execution details, including any errors or warnings.

These outputs facilitate easy review of new papers and monitoring of the script's performance.

#### Details

- Two-tier Keyword System: Script has `must_include` keywords (related to language models) and `optional_keywords` (related to planning).
  - A paper must contain at least one keyword from each list to be considered relevant.
  - The `is_relevant()` function checks for the presence of keywords from both lists.
- Script sets `max_results` to 200 for each query to capture more papers.
- SQLite database is used to keep track of papers already processed:
  - The `init_db()` function creates the database and table if they don't exist.
  - The `paper_exists()` function checks if a paper is already in the database.
  - The `insert_paper()` function adds new papers to the database.
  - In the main loop, the script checks each paper against the database before adding it to the list of new papers (deduplication process).
- The script only creates a CSV file if there are new papers to report.
- The script logs the number of new papers found and the number of papers added to the database.
- Configuration File Extension: Using absolute paths can make the script less portable and harder to share. A good workaround is to use relative paths with environment variables or a configuration file. This approach allows for flexibility when running the script manually or as a CRON job, while also making it easy to share and deploy on different systems.
- Requirements:
  - Need to have the `config.json` file in the same directory as the script.
  - Also, need to have an empty `db` folder.
