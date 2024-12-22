# Web-Content-Classifier
#### Video Demo:  https://www.youtube.com/watch?v=9ENBIWtEiXk
#### Description:

This project focuses on building a system that scrapes websites, preprocesses the content, and classifies them into different categories such as e-commerce, sports, and news using machine learning models like Random Forest and Naive Bayes.

## Project Structure

- **`scrape_website()`**: Scrapes the content of a website using BeautifulSoup, extracts the title, meta description, headers, and main content.
- **`preprocess_data()`**: Cleans and processes the scraped data by concatenating all text fields, converting text to lowercase, and removing punctuation.
- **`extract_features()`**: Converts the processed text data into numerical features using TF-IDF vectorization.
- **`train_model()`**: Splits the data into training and testing sets and trains a machine learning model (Random Forest by default) to classify websites.
- **`evaluate_model()`**: Evaluates the performance of the trained model using classification metrics.
- **`save_to_csv()`** and **`load_from_csv()`**: Utility functions to save the scraped data to a CSV file and load it for reuse.
- **`main()`**: The main function that orchestrates scraping, preprocessing, feature extraction, model training, and evaluation.

## Prerequisites

### Libraries Required

Install the required libraries using the following commands:

```bash
pip install nltk requests beautifulsoup4 scikit-learn pandas
```

### Input Data

The `urls.csv` file should contain the URLs and their corresponding categories. Each row should have the following columns:

- `url`: The URL of the website to scrape.
- `category`: The category label (e.g., 'sports', 'e-commerce', 'news').

## How to Run

1. Ensure you have the required libraries installed:
   - Install the necessary Python packages by running:

   ```bash
   pip install -r requirements.txt
   ```
2. Prepare the `urls.csv` file with URLs and categories as shown in the input data section above.  

3. Run the Script in Jupyter Notebook: Open the Jupyter Notebook and run the cells step-by-step to perform scraping, preprocessing, and model training.

## Main Workflow

1. **Scraping**: 
   - The script scrapes the provided websites and extracts information like the title, meta description, headers, and main content.

2. **Preprocessing**: 
   - The text data is cleaned (lowercased, punctuation removed) and prepared for feature extraction.

3. **Feature Extraction**: 
   - The preprocessed data is transformed into numerical features using TF-IDF vectorization.

4. **Model Training**: 
   - The Random Forest or Naive Bayes classifier is trained on the TF-IDF features.

5. **Model Evaluation**: 
   - The classifier is evaluated on a test set using precision, recall, and F1-score.

## Output

- The script will print out the evaluation metrics for the model, including precision, recall, and F1-scores for each category.

## Customization

- **Changing the Classifier**: 
   - By default, the script uses a Random Forest classifier. You can switch to Naive Bayes by uncommenting the corresponding line in the `train_model()` function.
  
- **Adjusting TF-IDF Parameters**: 
   - Modify the parameters in the `TfidfVectorizer` (e.g., `ngram_range`, `max_features`) to fine-tune feature extraction.

## Saving and Loading Data

- The scraped and preprocessed data is saved to a CSV file (`scraped_data.csv`) for later use. If this file already exists, the script will load it instead of re-scraping the websites.

## Notes

- Some websites may block scraping. The script uses custom headers to mimic a real browser request.
  
- To avoid overwhelming websites with too many requests, a delay of 2 seconds between requests is added.
