import sys
import os
import time
import json
from dotenv import load_dotenv
from rev_ai import apiclient

# Load environment variables from .env file
load_dotenv()
access_token = os.getenv("REVAI_ACCESS_TOKEN")
if not access_token:
    print("Error: REVAI_ACCESS_TOKEN not found in .env file.")
    sys.exit(1)

# Check command-line arguments
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: python transcribe.py <audio_file_path> [transcript_file_path]")
    sys.exit(1)

audio_file_path = sys.argv[1]
transcript_file_path = sys.argv[2] if len(sys.argv) == 3 else None

# Validate audio file
if not os.path.isfile(audio_file_path):
    print(f"Error: Audio file '{audio_file_path}' does not exist.")
    sys.exit(1)

# Validate optional transcript file
if transcript_file_path and not os.path.isfile(transcript_file_path):
    print(f"Error: Transcript file '{transcript_file_path}' does not exist.")
    sys.exit(1)

# Create Rev AI client
client = apiclient.RevAiAPIClient(access_token)

# Function to extract topics from text
def extract_topics(transcript_text):
    print("\nExtracting topics from transcript...")
    # For simplicity, we'll simulate topic extraction if not using API directly
    # In practice, Rev AI would do this server-side with topics_config
    words = transcript_text.lower().split()
    common_words = set(["the", "is", "a", "and", "to", "in", "of", "for"])
    topics = [word for word in words if word not in common_words and len(word) > 3]
    # Take top 5 most frequent words as "topics" (rudimentary approach)
    from collections import Counter
    topic_counts = Counter(topics).most_common(5)
    return [topic for topic, count in topic_counts]

# If transcript file is provided, extract topics and exit
if transcript_file_path:
    with open(transcript_file_path, "r") as f:
        transcript_text = f.read()
    topics = extract_topics(transcript_text)
    print("Topics extracted:")
    for topic in topics:
        print(f"- {topic}")
    sys.exit(0)

# Submit the audio file for transcription with topic extraction and sentiment analysis
print(f"Submitting job for file: {audio_file_path}")
job = client.submit_job_local_file(
    audio_file_path,
    topics_config={"enabled": True},  # Enable topic extraction
    sentiment_analysis_config={"enabled": True}  # Enable sentiment analysis
)
print(f"Job submitted successfully. Job ID: {job.id}")

# Poll for job completion
max_wait_time = 1800  # 30 minutes in seconds
polling_interval = 10  # Poll every 10 seconds
elapsed_time = 0

while elapsed_time < max_wait_time:
    job_details = client.get_job_details(job.id)
    status = job_details.status

    if status == "transcribed":
        print("Transcription completed.")
        break
    elif status == "failed":
        print(f"Transcription failed: {job_details.failure}")
        sys.exit(1)
    else:
        print(f"Job status: {status}. Waiting...")
        time.sleep(polling_interval)
        elapsed_time += polling_interval

if elapsed_time >= max_wait_time:
    print("Error: Transcription timed out after 30 minutes.")
    sys.exit(1)

# Retrieve transcript as text
transcript_text = client.get_transcript_text(job.id)

# Save transcript to a file named after the input audio file
base_name = os.path.splitext(os.path.basename(audio_file_path))[0]
output_file = f"{base_name}_transcript.txt"
with open(output_file, "w") as f:
    f.write(transcript_text)
print(f"\nTranscript saved to: {output_file}")

# Retrieve JSON output for topics and sentiment analysis
transcript_json = client.get_transcript_json(job.id)

# Extract and display topics
topics = transcript_json.get("topics", [])
if topics:
    print("\nExtracted Topics:")
    for topic in topics:
        print(f"- {topic['topic_name']} (confidence: {topic['confidence']:.2f})")
else:
    # Fallback to basic topic extraction if API doesn't return topics
    topics = extract_topics(transcript_text)
    print("\nExtracted Topics (basic):")
    for topic in topics:
        print(f"- {topic}")

# Extract and display sentiment analysis
sentiments = transcript_json.get("sentiments", [])
if sentiments:
    print("\nSentiment Analysis:")
    for sentiment in sentiments:
        print(f"- Text: '{sentiment['text']}'")
        print(f"  Sentiment: {sentiment['sentiment']} (confidence: {sentiment['confidence']:.2f})")
else:
    print("\nNo sentiment analysis data returned.")

# Display the full transcript
print("\nFull Transcript:")
print(transcript_text)