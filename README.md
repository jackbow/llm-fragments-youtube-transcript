# llm-fragments-youtube-transcript

A fragment loader for [LLM](https://llm.datasette.io/) that converts youtube transcripts into plaintext using [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) and [yt-dlp](https://github.com/yt-dlp/yt-dlp).

yt-dlp is used for metadata (title, uploader, date, description) and youtube-transcript-api is used to fetch the transcript. yt-dlp at time of writing can only write subs to disk.

[![PyPI](https://img.shields.io/pypi/v/llm-fragments-youtube-transcript.svg)](https://pypi.org/project/llm-fragments-youtube-transcript/)
[![Changelog](https://img.shields.io/github/v/release/jackbow/llm-fragments-youtube-transcript?include_prereleases&label=changelog)](https://github.com/jackbow/llm-fragments-youtube-transcript/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/jackbow/llm-fragments-youtube-transcript/blob/main/LICENSE)

## To do

- [ ] Chat mode
- [ ] Embedding generation

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/):

```bash
llm install llm-fragments-youtube-transcript
```

## Usage

Use `-f 'yt:URL'` to fetch and convert an online video transcript to plaintext.

Example:

```bash
llm -f 'yt:https://youtube.com/?v=' "Summarize this video."
```

The output includes:
- Title
- Uploader
- Date
- Description
- Transcription

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

```bash
cd llm-fragments-youtube-transcript
uv sync
source .venv/bin/activate
```

## Dependencies

- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api): For extracting transcriptions
- [yt-dlp](https://github.com/yt-dlp/yt-dlp): For extracting metadata from youtube videos
- [llm](https://llm.datasette.io/): The LLM CLI tool this plugin extends
