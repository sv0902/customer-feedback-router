Design Decision Note: Customer Feedback Router


1. Problem Overview
Customer support teams receive high volumes of unstructured text across emails, web forms, and feedback surveys. Reviewing every entry manually is time consuming, while fully automating with AI can cause critical bugs or edge cases to slip through undetected. The goal of this project was to build a dependable processing pipeline that automates straightforward classification while safely routing uncertain or failing cases to human reviewers.


2. Key Architecture Choices

Keeping Code Simple and Modular:
Rather than combining everything into a single script or relying on heavyweight frameworks, the solution is divided into three focused modules:
- database.py: Manages local SQLite connection, table schema creation, parameterized insert queries to guard against SQL injection, and review queue retrieval.
- ai_service.py: Encapsulates all Gemini API communication and payload parsing behind a single classify_feedback function. The rest of the codebase remains agnostic to the underlying AI implementation.
- main.py: Connects all parts by loading the CSV dataset, stripping input whitespace, invoking classification, storing results, and displaying records flagged for human review.

Model Selection:
I used gemini-3.5-flash-lite because it offers low response latency, efficient token usage, and consistent JSON output structure.

The 0.70 Confidence Threshold:
To balance automation efficiency against accuracy, a threshold of 0.70 was chosen:
- At or above 0.70 confidence: The classification is deemed reliable and assigned status "processed".
- Below 0.70 confidence: The record is assigned status "needs_review" and routed to the manual review queue.


3. Error Handling and Resilience
- Empty and Whitespace Inputs: Detected locally before making any network request, avoiding unnecessary API consumption and tagging the row as "needs_review".
- API and Network Outages (such as 503 temporary unavailability): Wrapped in try-except blocks. If the external service fails, the script falls back to a safe default (confidence 0.0 and status "needs_review"), allowing the batch runner to continue uninterrupted.
- JSON Cleaning: Any markdown code fences or backticks wrapping the response text are stripped before invoking json.loads.


4. Testing Strategy
I wrote 4 automated unit tests using pytest. To ensure tests execute quickly, operate without network connectivity, and consume zero API quota, they validate empty input handling, whitespace normalization, confidence threshold assignment, and database persistence directly without making live external API calls.