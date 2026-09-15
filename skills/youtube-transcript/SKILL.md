---
name: youtube-transcript
description: Download or transcribe YouTube/audio into Traditional Chinese transcripts with yt-dlp and faster-whisper, including dependency checks, local output conventions, and cross-machine Codex reuse.
---

# YouTube Transcript Skill

Use this skill when the user wants a YouTube video, local audio file, interview, lecture, or meeting recording turned into a Traditional Chinese transcript.

## Default Outcome

Produce a readable Traditional Chinese transcript with timestamps. Prefer both:

- `*.txt` for plain transcript exchange.
- `*.md` for review, notes, and downstream summarization.

Keep downloaded audio and generated transcripts out of unrelated repos unless the user names a destination. Use an explicit output directory such as `outputs/transcripts/`, `/tmp`, or the user's requested folder.

## Tooling

Prefer the helper script:

```bash
python skills/youtube-transcript/scripts/youtube_transcribe.py "YOUTUBE_OR_AUDIO_URL" --out-dir outputs/transcripts
```

For local audio:

```bash
python skills/youtube-transcript/scripts/youtube_transcribe.py "/path/to/audio.mp3" --out-dir outputs/transcripts
```

The script uses:

- `yt-dlp` to download YouTube audio.
- `faster-whisper` for transcription.
- `torch` only to detect CUDA availability.
- `ffmpeg` through `yt-dlp` for audio extraction.

If dependencies are missing, report the exact install command instead of inventing another workflow:

```bash
python -m pip install yt-dlp faster-whisper torch
```

System `ffmpeg` is also required. On Windows, prefer an existing package manager (`winget`, `choco`) if available; on Ubuntu/Debian use `sudo apt install ffmpeg`; on macOS use `brew install ffmpeg`.

## Transcription Defaults

Use these defaults unless the user asks otherwise:

- Model: `large-v3` for quality.
- Language: `zh`.
- Prompt: `以下是繁體中文的逐字稿與訪談紀錄，請使用繁體中文、自然標點與台灣常用詞。`
- Device: auto-detect CUDA, otherwise CPU.
- Compute type: `float16` on CUDA, `int8` on CPU.
- Timestamp format: `[HH:MM:SS -> HH:MM:SS]`.

If the machine is slow or memory constrained, use `--model medium` or `--model small`. Tell the user the quality/speed tradeoff briefly.

## Operating Notes

- Network access may be required for YouTube downloads and first-time model downloads; ask for approval only when the runtime requires it.
- Do not hardcode the video URL inside generated scripts. Pass it as a CLI argument.
- If a YouTube download fails, retry once with `--cookies-from-browser` only when the user explicitly authorizes access to browser cookies.
- If the content is copyrighted, generate the transcript for the user's private workflow; do not publish or redistribute it unless the user confirms they have rights.
- Preserve the user's requested output language. If they ask for Traditional Chinese, do not silently output Simplified Chinese.

## Quick Verification

After changing this skill, run:

```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/youtube-transcript
python skills/youtube-transcript/scripts/youtube_transcribe.py --help
```
