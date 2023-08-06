#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com

import hashlib
import shutil
import wave
from pathlib import Path
from typing import List

import chardet
import numpy as np


def ensure_dir(dir_path):
    if type(dir_path) == str:
        dir_path = Path(dir_path)
    dir_path.mkdir(parents=True, exist_ok=True)


def resolve_filepath(p) -> Path:
    if isinstance(p, str):
        p = Path(p)
    return p.resolve()


def detect_encoding(input_file):
    input_file = resolve_filepath(input_file)

    with open(input_file, "rb") as f:
        c = chardet.detect(f.read())

        if c["encoding"] == "gb2312":
            return "gbk"

        return c["encoding"]


def write_text_lines(output_file, lines, encoding="utf8"):
    output_file = resolve_filepath(output_file)
    ensure_dir(output_file.parents[0])

    with open(output_file, "w", encoding=encoding, newline="\n") as f:
        for line in lines:
            if not isinstance(line, str):
                line = str(line)
            f.write(line)
            f.write("\n")
    print(f"write txt file: {output_file}")


def read_text_lines(input_file, encoding="utf8"):
    input_file = resolve_filepath(input_file)
    with open(input_file, "r", encoding=encoding) as f:
        lines = f.readlines()

    return [line.strip() for line in lines]


def read_text_multi(input_files, encoding="utf8"):
    lines = []
    for f in input_files:
        lines.extend(read_text_lines(f))
    return lines


def lines_of(input_file, encoding="utf8"):
    input_file = resolve_filepath(input_file)
    with open(input_file, "r", encoding=encoding) as f:
        while True:
            line = f.readline()
            if not line:
                break

            line = line.strip()
            yield line


def write_here_sh(output_file, cli_lines):
    lines = [
        "#!/usr/bin/env bash",
        "",
        'DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )',
        "cd $DIR",
        "",
    ]

    lines.extend(cli_lines)
    write_text_lines(output_file, lines)


def backup(p, force=False):
    p = resolve_filepath(p)
    dst = p.parent / f"{p.name}.bak"
    if dst.exists() and not force:
        print(f"backup file alread exists: {dst}")
        return dst

    shutil.copy(p, dst)
    print(f"backup {p} -> {dst}")
    return dst


def copy(src, dst):
    dst = resolve_filepath(dst)
    ensure_dir(dst.parent)
    shutil.copy(src, dst)


def read_pcm_audio(wav_path):
    with open(wav_path, "rb") as f:
        temp = f.read()
        sig = np.frombuffer(temp, dtype=np.int16)
        return sig


def read_pcm_audio_by(wav_path, size):
    with open(wav_path, "rb") as f:
        temp = f.read(size)
        sig = np.frombuffer(temp, dtype=np.int16)
        return sig


def write_wav(audio_path: Path, audio_data):
    output_dir = audio_path.parents[0]
    output_dir.mkdir(parents=True, exist_ok=True)

    nchannels = 1
    sampwidth = 2
    framerate = 16000
    nframes = len(audio_data)
    wave_file = wave.open(str(audio_path), "wb")
    wave_file.setparams(((nchannels, sampwidth, framerate, nframes, "NONE", "NONE")))
    wave_file.writeframes(np.array(audio_data, dtype="int16").tobytes())
    wave_file.close()


_img_ext = {".jpg", ".bmp", ".png", ".jpeg", ".rgb", ".tif", ".tiff", ".gif", ".pdf"}


def check_image_file(path):
    return any([path.lower().endswith(e) for e in _img_ext])


def list_all_imgs(d: Path) -> List[Path]:
    img_list = []
    for f in d.iterdir():
        if f.is_dir():
            continue

        if check_image_file(f.name):
            img_list.append(f)
    return img_list


def build_file_name(name, extension, suffix):
    if suffix is None:
        return f"{name}{extension if extension else ''}"
    else:
        return f"{name}-{suffix}{extension if extension else ''}"


def build_sh_name(name, suffix):
    return build_file_name(name, ".sh", suffix)


def build_txt_name(name, suffix):
    return build_file_name(name, ".txt", suffix)


def sha256sum(file_path):
    h = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()
