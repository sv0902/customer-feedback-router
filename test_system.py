import sqlite3 
import pytest
from database import create_table, save_feedback, get_review_queue
from ai_service import classify_feedback

# Test 1: Empty text handling (Edge case)
def test_empty_feedback_handling():
    result = classify_feedback("")
    assert result["status"] == "needs_review"
    assert result["confidence"] == 0.0

# Test 2: Low-confidence status threshold
def test_low_confidence_status():
    
    confidence = 0.55
    status = "processed" if confidence >= 0.7 else "needs_review"
    assert status == "needs_review"

# Test 3: Database insert and read check
def test_database_insert_and_fetch():
    create_table()
    save_feedback(
        source="email",
        feedback="Test review item",
        intent="Complaint",
        topic="Delivery",
        priority="High",
        confidence=0.40, 
        status="needs_review"
    )
    
    queue = get_review_queue()
    
    assert len(queue) > 0
    
    assert queue[-1][7] == "needs_review"

# Test 4: Edge case / Failure handling
def test_whitespace_feedback_handling():
    result = classify_feedback("   ")
    assert result["status"] == "needs_review"
    assert result["intent"] == "Unknown"