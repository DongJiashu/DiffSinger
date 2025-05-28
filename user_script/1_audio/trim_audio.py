#this tool is to trim wav files

import argparse
from pathlib import Path
import torchaudio

def trim_wav(input_path: Path, output_path: Path, start_sec: float, end_sec: float):
    waveform, sample_rate = torchaudio.load(input_path)
    
    total_sec = waveform.size(1) / sample_rate
    start_sample = int(start_sec * sample_rate)
    end_sample = int(end_sec * sample_rate) if end_sec is not None else waveform.size(1)

    if start_sample >= waveform.size(1):
        raise ValueError("Start time is beyond audio length.")
    if end_sample > waveform.size(1):
        end_sample = waveform.size(1)
    if start_sample >= end_sample:
        raise ValueError("Invalid start/end time configuration.")

    trimmed = waveform[:, start_sample:end_sample]
    torchaudio.save(output_path, trimmed, sample_rate)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trim WAV file by start and end time.")
    parser.add_argument("input", type=Path, help="Path to input .wav file")
    parser.add_argument("output", type=Path, help="Path to output .wav file")
    parser.add_argument("--start", type=float, default=0.0, help="Start time in seconds (default: 0.0)")
    parser.add_argument("--end", type=float, default=None, help="End time in seconds (optional)")

    args = parser.parse_args()
    trim_wav(args.input, args.output, args.start, args.end)