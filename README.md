# Bot DokerFinder

The `DorkFinder` code is a Python bot designed to perform automated Google searches using specific dorks, providing relevant URLs. It integrates various functionalities, including reading keywords, executing searches, extracting links, storing results in CSV, and displaying the collected information in the console.

# Installation
## 📄 Prerequisites

- Installed Python 3.10.11
- pip 23.3.1

## 🚩 Installation Steps

1. Clone the repository of DorkFinder:

       git clone git clone https://github.com/Pedro-Alvess/Bot_dorker.git

2. Navigate to the project directory.
3. Install dependencies:

       pip install -r requirements.txt

5. Add the keywords to be searched in “keywords.txt”.
6. Add the dorks to the file in "dorkStr.txt".

# ⚙ Additional configuration

The `DorkFinder` code can be executed in two modes: with the visual interface of ChromeDriver or in headless mode.

In the visual interface mode, ChromeDriver opens a visible browser window during execution, allowing you to monitor the progress of the searches in real-time.

In headless mode, ChromeDriver operates without opening a browser window, performing all tasks in the background. This mode is especially useful for execution in environments without a graphical interface, such as servers and container infrastructures.

When running in a container, it is recommended to uncomment the options that disable shared memory (`--disable-dev-shm-usage`) and the sandbox mode (`--no-sandbox`) to ensure more efficient performance and avoid potential errors related to these settings.

# License

This project is licensed under the [GPL-3.0 license](LICENSE).

   
 



 
