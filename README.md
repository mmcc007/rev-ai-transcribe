# Rev AI Audio Transcription Tool

This Python script uses the Rev AI API to transcribe audio files, save the transcript locally, extract topics, and perform sentiment analysis. It’s designed to be run from the command line, with the Rev AI access token securely stored in a `.env` file and the audio file path provided as an argument. Optionally, it can extract topics from an existing text transcript file.

## Features

- **Transcription**: Converts audio files (MP3, WAV, FLAC) to text using Rev AI’s Asynchronous Speech-to-Text API.
- **File Saving**: Saves the transcript to a local file named after the input audio file (e.g., `recording_transcript.txt` for `recording.mp3`).
- **Topic Extraction**: Identifies key topics from the transcript using Rev AI’s NLP capabilities or a basic local fallback method.
- **Sentiment Analysis**: Analyzes the sentiment (positive, negative, neutral) of transcript segments via Rev AI’s API.
- **Flexible Input**: Supports transcribing audio files or extracting topics from pre-existing text transcripts.

## Prerequisites

- **Python 3.6+**: Ensure Python is installed on your system.
- **Rev AI Account**: Obtain an access token from [Rev AI](https://www.rev.ai/).
- **Supported Audio Formats**: MP3, WAV, or FLAC files.

## Installation

1. **Clone or Download**:
   - Clone this repository or download the script (`transcribe.py`).

2. **Install Dependencies**:
   - Install required Python libraries using pip:
     ```
     pip install rev-ai python-dotenv
     ```

3. **Set Up Environment**:
   - Create a `.env` file in the same directory as the script:
     ```
     echo "REVAI_ACCESS_TOKEN=your_token_here" > .env
     ```
   - Replace `your_token_here` with your actual Rev AI access token.

## Usage

Run the script from the command line with the following options:

### Transcribe an Audio File
Transcribe an audio file, save the transcript, and analyze topics and sentiment:
```
python transcribe.py <audio_file_path>
```
Example:
```
python transcribe.py ~/Downloads/recording.mp3
```
- Output: Transcript saved as `recording_transcript.txt`, with topics and sentiment printed to the console.

### Extract Topics from a Transcript File
Extract topics from an existing text transcript file (skips transcription):
```
python transcribe.py <audio_file_path> <transcript_file_path>
```
Example:
```
python transcribe.py ~/Downloads/recording.mp3 ~/Downloads/recording_transcript.txt
```
- Output: Topics extracted from the text file and printed to the console.

### Notes
- The audio file path must be a valid MP3, WAV, or FLAC file.
- The transcript file (if provided) must be a plain text file.
- The script waits up to 30 minutes for transcription to complete, polling every 10 seconds.

## Example Output

For `python transcribe.py ~/Downloads/recording.mp3`:
```
Submitting job for file: ~/Downloads/recording.mp3
Job submitted successfully. Job ID: abc123
Job status: in_progress. Waiting...
Transcription completed.
Transcript saved to: recording_transcript.txt

Extracted Topics:
- discussion (confidence: 0.95)
- meeting (confidence: 0.89)

Sentiment Analysis:
- Text: 'This is great news'
  Sentiment: positive (confidence: 0.92)
- Text: 'We need to fix this'
  Sentiment: negative (confidence: 0.87)

Full Transcript:
This is great news. We need to fix this issue soon.
```

## Script Details

- **File Saving**: The transcript is saved in the current working directory with the format `<audio_base_name>_transcript.txt`.
- **Topic Extraction**: Uses Rev AI’s server-side topic detection when transcribing audio. For text input or as a fallback, it employs a basic word-frequency method (top 5 non-common words).
- **Sentiment Analysis**: Enabled via Rev AI’s API, providing sentiment per transcript segment with confidence scores.
- **Error Handling**: Validates file existence, token presence, and job status, exiting with descriptive messages on failure.

## Customization

- **Output Location**: Modify the `output_file` path in the script to save transcripts elsewhere (e.g., next to the audio file).
- **Polling Settings**: Adjust `max_wait_time` (default: 1800s) or `polling_interval` (default: 10s) for different wait times.
- **Topic Extraction**: Enhance the `extract_topics` function for more sophisticated local analysis if needed.

## Limitations

- Requires a Rev AI access token and internet connection.
- Transcription time depends on audio length and Rev AI’s processing speed (max 30-minute wait).
- Local topic extraction is basic compared to Rev AI’s NLP; use the API’s results for best accuracy.

## Troubleshooting

- **“Token not found”**: Ensure `.env` exists and contains `REVAI_ACCESS_TOKEN=your_token`.
- **“File does not exist”**: Check the file path provided.
- **API Errors**: Verify your token is valid and has sufficient credits ([Rev AI Pricing](https://www.rev.ai/pricing)).

## License

This project is unlicensed and provided as-is for personal use. Refer to Rev AI’s terms for API usage.

## Acknowledgments

- Built with [Rev AI’s Asynchronous API](https://docs.rev.ai/api/asynchronous/).
- Thanks to xAI for inspiring AI-driven exploration!
