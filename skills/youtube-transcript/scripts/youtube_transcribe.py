#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download/transcribe YouTube or local audio into Traditional Chinese text."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path


DEFAULT_PROMPT = "以下是繁體中文的逐字稿與訪談紀錄，請使用繁體中文、自然標點與台灣常用詞。"


def fail_missing(package: str, install_hint: str) -> None:
    print(f"缺少 Python 套件：{package}", file=sys.stderr)
    print(f"安裝方式：{install_hint}", file=sys.stderr)
    raise SystemExit(2)


try:
    import yt_dlp
except ImportError:  # pragma: no cover - exercised on machines without deps
    yt_dlp = None

try:
    from faster_whisper import WhisperModel
except ImportError:  # pragma: no cover
    WhisperModel = None


def import_torch():
    try:
        import torch
    except ImportError:
        return None
    return torch


def slugify(value: str, fallback: str = "transcript") -> str:
    value = re.sub(r"https?://", "", value)
    value = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", value, flags=re.UNICODE)
    value = value.strip(".-_")
    return (value or fallback)[:80]


def is_url(source: str) -> bool:
    return source.startswith(("http://", "https://"))


def format_timestamp(seconds: float) -> str:
    total = max(0, int(seconds))
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def ensure_dependencies(source: str) -> None:
    if is_url(source) and yt_dlp is None:
        fail_missing("yt-dlp", "python -m pip install yt-dlp")
    if WhisperModel is None:
        fail_missing("faster-whisper", "python -m pip install faster-whisper")
    if shutil.which("ffmpeg") is None:
        print("警告：找不到 ffmpeg。YouTube 音訊抽取可能失敗。", file=sys.stderr)


def download_youtube_audio(url: str, temp_dir: Path, cookies_from_browser: str | None) -> tuple[Path, str]:
    assert yt_dlp is not None
    output_template = str(temp_dir / "%(title).120s-%(id)s.%(ext)s")
    options: dict[str, object] = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "noplaylist": True,
        "quiet": False,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    if cookies_from_browser:
        options["cookiesfrombrowser"] = (cookies_from_browser,)

    with yt_dlp.YoutubeDL(options) as downloader:
        info = downloader.extract_info(url, download=True)
        title = info.get("title") or slugify(url)
        candidate = Path(downloader.prepare_filename(info)).with_suffix(".mp3")

    if not candidate.exists():
        mp3s = sorted(temp_dir.glob("*.mp3"), key=lambda path: path.stat().st_mtime, reverse=True)
        if not mp3s:
            raise FileNotFoundError("yt-dlp completed but no mp3 file was produced")
        candidate = mp3s[0]
    return candidate, str(title)


def resolve_audio(source: str, temp_dir: Path, cookies_from_browser: str | None) -> tuple[Path, str]:
    if is_url(source):
        return download_youtube_audio(source, temp_dir, cookies_from_browser)
    path = Path(source).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"找不到音訊檔：{path}")
    return path, path.stem


def choose_device_and_compute_type(device: str, compute_type: str) -> tuple[str, str]:
    if device != "auto":
        return device, compute_type
    torch = import_torch()
    if torch is not None and torch.cuda.is_available():
        return "cuda", "float16" if compute_type == "auto" else compute_type
    return "cpu", "int8" if compute_type == "auto" else compute_type


def transcribe(
    audio_path: Path,
    model_size: str,
    language: str,
    prompt: str,
    device: str,
    compute_type: str,
) -> list[dict[str, object]]:
    assert WhisperModel is not None
    runtime_device, runtime_compute = choose_device_and_compute_type(device, compute_type)
    print(f"載入模型：{model_size} / device={runtime_device} / compute_type={runtime_compute}")
    model = WhisperModel(model_size, device=runtime_device, compute_type=runtime_compute)
    segments, info = model.transcribe(
        str(audio_path),
        language=language,
        initial_prompt=prompt,
        vad_filter=True,
    )
    print(f"辨識語言：{info.language} / confidence={info.language_probability:.2f}")
    return [
        {
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip(),
        }
        for segment in segments
        if segment.text.strip()
    ]


def write_outputs(
    segments: list[dict[str, object]],
    out_dir: Path,
    base_name: str,
    source: str,
    title: str,
) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = slugify(base_name or title)
    txt_path = out_dir / f"{stem}.txt"
    md_path = out_dir / f"{stem}.md"

    with txt_path.open("w", encoding="utf-8") as txt:
        for segment in segments:
            start = format_timestamp(float(segment["start"]))
            end = format_timestamp(float(segment["end"]))
            txt.write(f"[{start} -> {end}] {segment['text']}\n")

    with md_path.open("w", encoding="utf-8") as md:
        md.write(f"# {title}\n\n")
        md.write(f"- 來源：{source}\n")
        md.write(f"- 格式：繁體中文逐字稿\n\n")
        md.write("## Transcript\n\n")
        for segment in segments:
            start = format_timestamp(float(segment["start"]))
            end = format_timestamp(float(segment["end"]))
            md.write(f"- [{start} -> {end}] {segment['text']}\n")

    return txt_path, md_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Transcribe YouTube/local audio to Traditional Chinese.")
    parser.add_argument("source", nargs="?", help="YouTube URL or local audio/video file path.")
    parser.add_argument("--out-dir", default="outputs/transcripts", help="Output directory.")
    parser.add_argument("--name", default="", help="Output filename stem. Defaults to video title or audio filename.")
    parser.add_argument("--model", default="large-v3", help="faster-whisper model size.")
    parser.add_argument("--language", default="zh", help="Whisper language code.")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="Initial prompt for transcription style.")
    parser.add_argument("--device", default="auto", choices=("auto", "cpu", "cuda"), help="Runtime device.")
    parser.add_argument("--compute-type", default="auto", help="faster-whisper compute type.")
    parser.add_argument(
        "--cookies-from-browser",
        default=None,
        help="Browser name for yt-dlp cookies, e.g. chrome. Use only with user authorization.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if not args.source:
        print("請提供 YouTube URL 或本機音訊檔路徑。使用 --help 查看參數。", file=sys.stderr)
        return 2

    ensure_dependencies(args.source)
    out_dir = Path(args.out_dir).expanduser().resolve()

    with tempfile.TemporaryDirectory(prefix="yt-transcript-") as temp:
        audio_path, title = resolve_audio(args.source, Path(temp), args.cookies_from_browser)
        segments = transcribe(
            audio_path=audio_path,
            model_size=args.model,
            language=args.language,
            prompt=args.prompt,
            device=args.device,
            compute_type=args.compute_type,
        )
        txt_path, md_path = write_outputs(
            segments=segments,
            out_dir=out_dir,
            base_name=args.name,
            source=args.source,
            title=title,
        )

    print(f"已輸出 TXT：{txt_path}")
    print(f"已輸出 MD：{md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
