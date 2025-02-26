import sys
import os
import time
from dotenv import load_dotenv
from rev_ai import apiclient

# Load environment variables from .env file
load_dotenv()
access_token = os.getenv("REVAI_ACCESS_TOKEN")
if not access_token:
    print("Error: REVAI_ACCESS_TOKEN not found in .env file.")
    sys.exit(1)

# Check command-line argument for audio file path
if len(sys.argv) != 2:
    print("Usage: python transcribe.py <audio_file_path>")
    sys.exit(1)

file_path = sys.argv[1]
if not os.path.isfile(file_path):
    print(f"Error: File '{file_path}' does not exist.")
    sys.exit(1)

# Create Rev AI client
client = apiclient.RevAiAPIClient(access_token)

# Submit the local file for transcription
print(f"Submitting job for file: {file_path}")
job = client.submit_job_local_file(file_path)
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

# Retrieve and display the transcript
transcript_text = client.get_transcript_text(job.id)
print("\nTranscript:")
print(transcript_text)