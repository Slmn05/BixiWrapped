# 🚲 BixiWrapped

**BixiWrapped** is a Python tool that allows you to scrape, analyze, and visualize your personal [BIXI](https://bixi.com/) (Montreal's bike-sharing system) ride history. Ever wondered how many kilometers you biked, your most frequent stations, or what your routes look like on a map? This tool creates a "Wrapped" style summary of your biking season.

## 📁 Project Structure

* `scrapping.py`: The data collection script. Logs into your BIXI account portal and scrapes your ride history (dates, durations, start/end stations, etc.).
* `traces.py`: The analysis and visualization script. Processes the scraped data to generate insights, routes, and visual summaries.
* `data/`: The directory where your scraped raw data and processed outputs are stored locally.
* `requirements.txt`: Contains all the Python dependencies required to run the project.

## ✨ Features

- **Automated Data Extraction:** Safely scrape your trip history directly from the BIXI web portal.
- **Ride Analytics:** Calculate total time biked, favorite stations, and most active days.
- **Visual Traces:** Generate visual representations (traces) of your biking routes across the city.

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher installed on your machine.
- An active BIXI account with a history of rides.

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Slmn05/BixiWrapped.git](https://github.com/Slmn05/BixiWrapped.git)
   cd BixiWrapped