# this tool is used to extract wav from mp4. 

import os
import subprocess
import wave
import argparse

def extract_all_audio(input_dir, output_dir=None):
    if os.path.isfile(input_dir):
        files = [os.path.basename(input_dir)]
        root = os.path.dirname(input_dir)
        walk_iter = [(root, [], files)]
    else:
        walk_iter = os.walk(input_dir)

    for root, _, files in walk_iter:
        for file in files:
            if file.lower().endswith(('.mp4', '.mov')):
                mp4_path = os.path.join(root, file)
                if output_dir:
                    relative_path = os.path.relpath(root, input_dir)
                    out_dir = os.path.join(output_dir, relative_path)
                    os.makedirs(out_dir, exist_ok=True)
                    wav_path = os.path.join(out_dir, os.path.splitext(file)[0] + '.wav')
                else:
                    wav_path = os.path.splitext(mp4_path)[0] + ".wav"

                cmd = [
                    "ffmpeg", "-y", "-i", mp4_path,
                    "-vn", "-acodec", "pcm_s16le",
                    "-ar", "44100", "-ac", "2", wav_path
                ]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                with wave.open(wav_path, "rb") as wf:
                    sample_rate = wf.getframerate()
                    print(f"WAV saved to: {wav_path}")
                    print(f"Sample Rate: {sample_rate} Hz")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract audio from all video files in a folder and convert to WAV.")
    parser.add_argument("input_dir", help="Directory containing video files")
    parser.add_argument("--output", "-o", help="Directory to save output WAV files (optional)")
    args = parser.parse_args()

    extract_all_audio(args.input_dir, args.output)