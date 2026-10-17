Customer Feedback Router
This project is a simple Python pipeline to organize customer feedback collected across email, website forms, and surveys.

Instead of reading through every message manually, the script uses Gemini to classify the input, saves the results into a local SQLite database, and flags low-confidence entries for manual review.


What It Does
1. Reads customer feedback entries from data/feedback.csv.
2. Strips extra whitespace and skips empty rows.
3. Classifies text with Gemini to extract intent, topic, priority, and confidence score.
4. If confidence is 0.70 or higher, status is marked as processed.
5. If confidence is below 0.70 or an API error occurs, status is marked as needs_review.
6. Saves all records into feedback.db and displays the manual review queue in the console.


 Project Structure

```text
feedback_system/
├── data/
│   └── feedback.csv
├── main.py
├── ai_service.py
├── database.py
├── test_system.py
├── requirements.txt
├── .env.example
├── .gitignore
├── design_note.md
└── README.md
```


Setup and Usage

1. Install dependencies:
pip install -r requirements.txt

2. Set your API key in a .env file:
GEMINI_API_KEY=your_actual_api_key_here

3. Run the pipeline:
python main.py

4. Run tests:
python -m pytest test_system.py


Database Details
Feedback records are stored in feedback.db inside the feedback table with columns:
id, source, feedback, intent, topic, priority, confidence, and status.
