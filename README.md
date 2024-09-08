# Audio2Note
**Audio2Note** is an open-source tool that transcribes audio into text and generates concise summaries. Using Whisper for transcription in multiple languages and Hugging Face for advanced summarization, it integrates with Google Drive and Notion to streamline idea management.


## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation
Clone this repository on your local machine.

### Prerequisites
- Python 3.8+
- ffmpeg (for audio processing)

### Install the dependencies
Windows
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

Mac/Linux
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Setup Google Cloud Console
1. Go to the [Google Cloud Console](https://console.cloud.google.com) and create a new project.
2. Navigate to **APIs & Services** > **OAuth consent screen**.
3. Choose **External**, add your email, and configure the consent screen.
4. Under **APIs & Services**, go to **Library** and enable the **Google Drive API**.
5. Navigate to **APIs & Services** > **Credentials** and click **Create Credentials** > **OAuth 2.0 Client IDs**.
6. Download the `credentials.json` file and place it in the `auth/` directory.
7. Change the folder name from your google drive in line 116 of `functions/download_drive_file.py`

### Notion API Setup
1. Open the [Notion Developer Console](https://www.notion.so/profile/integrations) and create a new internal integration.
2. Copy the integration secret token and paste it in the `auth/notion_credentials.py` file.
3. Go to the Notion page where you want to store your notes, click **Share**, and copy the **Database ID** from the URL. Paste it in `auth/notion_credentials.py`.
4. Modify the blocks in `functions/notion.py` to customize how notes are uploaded to your Notion workspace.

## Usage
```bash
python main.py
```

You can edit each step of the process in the 'main.py'-file. For example change the language or change the tool for the summary.
You can also make an .exe desktop program with python pyinstaller.
Please close the tkinter window after every comand to have the correct data of the database shown.

## Examples
### Input at Google Drive:
Audio file: "meeting_audio.wav"

### Output at a new Notion page:
**Transcription**: "The team discussed project deadlines and goals for the next quarter..."
**Summary**: "Key points: Deadlines and goals were outlined for the upcoming quarter."

## Contributing
Contributions are welcome! Please fork this repository, make your changes, and submit a pull request.

To set up a development environment:
1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE. See the LICENSE file for details.
