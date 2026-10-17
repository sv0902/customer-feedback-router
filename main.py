import csv
import os
from database import create_table, save_feedback, get_review_queue
from ai_service import classify_feedback

CSV_FILE = "data/feedback.csv"

def run_pipeline():
    
    create_table()

    if not os.path.exists(CSV_FILE):
        print(f"Error: {CSV_FILE} file not found!")
        return

    
    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        
        print("Processing customer feedback...\n")
        for row in reader:
            source = row.get("source", "Unknown").strip()
            text = row.get("feedback", "").strip()

            
            if not text:
                continue

            print(f"Analyzing [{source}]: {text}")
            
            
            result = classify_feedback(text)

            
            save_feedback(
                source=source,
                feedback=text,
                intent=result.get("intent"),
                topic=result.get("topic"),
                priority=result.get("priority"),
                confidence=result.get("confidence"),
                status=result.get("status")
            )

    
    print("\n--- Manual Review Queue (needs_review) ---")
    review_items = get_review_queue()
    if not review_items:
        print("No items need manual review.")
    else:
        for item in review_items:
            
            print(f"ID: {item[0]} | Source: {item[1]} | Priority: {item[5]} | Conf: {item[6]} | Feedback: {item[2]}")

if __name__ == "__main__":
    run_pipeline()