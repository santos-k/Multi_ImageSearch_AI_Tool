# MultiSearch AI Recommendation System
![image](https://user-images.githubusercontent.com/40932902/213404949-acac1083-fb46-4f56-88c3-3d6cba899fa0.png)


[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/)
[![Dash 2.7](https://img.shields.io/badge/Dash-2.7-blue)](https://dash.plotly.com/)
[![Plolty 5.11](https://img.shields.io/badge/Plotly-5.11-blue)](https://pypi.org/project/plotly/)
![GitHub repo size](https://img.shields.io/github/repo-size/santos-k/Multi_ImageSearch_AI_Tool?logo=github) 
![GitHub Repo stars](https://img.shields.io/github/stars/santos-k/Multi_ImageSearch_AI_Tool?style=social) 
![GitHub watchers](https://img.shields.io/github/watchers/santos-k/Multi_ImageSearch_AI_Tool?style=social) 
![GitHub followers](https://img.shields.io/github/followers/santos-k?style=social) 

## Overview
The deep learning fashion recommendation project is a web-based application that utilizes machine learning techniques to recommend fashion items to users. The project is built using the Python programming language and the Dash framework, which is based on Flask and Bootstrap.

The project allows users to search for fashion items in a database by providing various types of input, including multiple images, a CSV file containing image URLs, or text search. Users also have the option to filter the results by specifying the database to search in, the category of the product, the brand, and the image matching confidence level.

Once the user submits their input, the project sends the data to an API which processes the information and returns a JSON data containing all the results and their corresponding information. The results are displayed in a card format, with each card displaying the original image and similar results. If there are more results in the same card, the user can slide through them. The results are also divided into pages for the user's convenience, allowing them to navigate through the results using the next and previous buttons.

Each result image has two buttons, "correct" and "wrong", which allow the user to provide feedback on the matching accuracy. Once the user clicks on any of the buttons, the feedback is stored in a dataframe. After submitting feedback for all the results, the dataframe can be downloaded as a CSV file.

Overall, the project's goal is to make it easier for users to discover new fashion items that match their preferences, by providing them with a convenient and user-friendly interface. It can be used by multiple users at the same time, and it does not require any sign-up or login process.


## Package Requirements
The following packages are required for running the deep learning fashion recommendation project:

- **datetime** -  (for working with dates and times)
- **dash** -  (for building the front-end interface of the project)
- **dash_bootstrap_components** -  (for adding Bootstrap components to the Dash interface)
- **base64** -  (for encoding and decoding binary data to and from base64 format)
- **os** -  (for interacting with the operating system)
- **pandas** -  (for working with dataframes)
- **io** -  (for working with input/output operations)
- **uuid** -  (for generating unique identifiers)
- **api** -  and helper (local files that contain additional functions or methods used in the project)
- **pickle** -  (for serializing and deserializing Python objects)
- **math** -  (for mathematical operations)
- **ast** -  (for converting string representation of lists to actual lists)
- **warnings** -  (for handling warnings)
- **requests** -  (for sending HTTP requests)
- **json** -  (for working with JSON data)
- **operator** -  (for comparing values)

**Note:** For more details on package versions, please check the requirements.txt file. It's important to make sure that the versions of the packages installed are compatible with the versions used in development, to avoid any conflicts.

## Files

- [.idea](https://github.com/santos-k/Multi_ImageSearch_AI_Tool/edit/main/.idea) 
- [assets/](https://github.com/santos-k/Multi_ImageSearch_AI_Tool/edit/main/assets) - assets used in app
  - [dropdown_df/](https://github.com/santos-k/Multi_ImageSearch_AI_Tool/tree/main/assets/dropdown_df) - drop down menu list dfs
  - [input_file/](https://github.com/santos-k/Multi_ImageSearch_AI_Tool/tree/main/assets/input_file) - files uploaded by users
  - [outputs/](https://github.com/santos-k/Multi_ImageSearch_AI_Tool/tree/main/assets/outputs) - output result file
  - [data.csv](https://github.com/santos-k/Multi_ImageSearch_AI_Tool/tree/main/assets/data.csv) - input csv data, for every users it will get changed as per input
  - [delete.svg](https://github.com/santos-k/Multi_ImageSearch_AI_Tool/tree/main/assets/delete.svg) - delete button icon image
  - [kb.png](https://github.com/santos-k/Multi_ImageSearch_AI_Tool/tree/main/assets/kb.png) - title icon image
- [.gitignore](https://github.com/santos-k/Multi_ImageSearch_AI_Tool/edit/main/.gitignore) - gitignore file
- [LICENSE](https://github.com/santos-k/Multi_ImageSearch_AI_Tool/edit/main/LICENCE) - Licence file
- [README.md](https://github.com/santos-k/Multi_ImageSearch_AI_Tool/edit/main/README.md) - documentation
- [api.py](https://github.com/santos-k/Multi_ImageSearch_AI_Tool/edit/main/api.py) - send and receive data from api
- [app.py](https://github.com/santos-k/Multi_ImageSearch_AI_Tool/edit/main/app.py) - main app file
- [helper.py](https://github.com/santos-k/Multi_ImageSearch_AI_Tool/edit/main/helper.py) - additional methods and fucntions
- [requirements.txt](https://github.com/santos-k/Multi_ImageSearch_AI_Tool/edit/main/requirements.txt) - packages used in app
- [resul3.json](https://github.com/santos-k/Multi_ImageSearch_AI_Tool/edit/main/resul3.json) - sample result json
- [result.json](https://github.com/santos-k/Multi_ImageSearch_AI_Tool/edit/main/result.json) - sample result json
- [store_user_data.csv](https://github.com/santos-k/Multi_ImageSearch_AI_Tool/edit/main/store_user_data.csv) - input data storage file

# How it works?
1. Go to the Home Page
2. Select the **Search Type** (default is File Search)
    1. **Image Search:** Allows selection of single or multiple images with validation applied
    2. **File Search:** Allows selection of a single CSV file with validation applied
    3. **Catalog Search:** Allows searching from an internal database with filtering based on options
3. Select the **Database** Type
    1. **Catalog:** Searches from an internal database of their own products
    2. **Scraped:** Searches from data scraped from other ecommerce websites
4. Select the **Sub-Database** (applicable only for Scraped database type) using multiple checkboxes
5. Select the **Category** and **Brand** (optional) for additional filtering (only avaible for single sub-database)
6. Set the **Matching Threshold Value as a percentage** (default is 80%) to determine the confidence score of the results.
7. Click on the **Search** button to initiate the search and display the results
8. Click on the **Clear** button to clear the page
9. Click on the **Delete** button to delete the last feedback record (if an incorrect button was pressed by mistake and can be used immediately after the mistake)
10. Click on the **Download** button to download the feedback data as a CSV file.

![image](https://user-images.githubusercontent.com/40932902/213434000-4f94f26b-af11-44dc-8ae8-dfeacb571897.png)

### On Search button Click:

![image](https://user-images.githubusercontent.com/40932902/213441020-eb0277f8-536a-4f96-9399-d7f06fec9135.png)
![image](https://user-images.githubusercontent.com/40932902/213442462-592ca719-ca67-457d-9026-b6350d211c7f.png)
![image](https://user-images.githubusercontent.com/40932902/213442894-70615500-a1d4-42e0-907e-c8299d004a19.png)
![image](https://user-images.githubusercontent.com/40932902/213442794-872217ff-4918-424b-afd5-a7b69a73fba2.png)
![image](https://user-images.githubusercontent.com/40932902/213442812-c4eb5357-3c12-451c-a8c4-79d889fc5cc2.png)
![image](https://user-images.githubusercontent.com/40932902/213442950-255612c0-ab76-4bb9-b82f-cee93741801d.png)







