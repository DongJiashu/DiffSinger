## About this Repository

This repository is part of my master's thesis project. It is based on the official [OpenVPI DiffSinger](https://github.com/openvpi/DiffSinger) implementation.

In addition to reproducing and adapting the core DiffSinger model, this repo includes all scripts and resources used throughout my research pipeline. These include external tools, dependent repositories, and custom scripts located in the `user_script/` directory. While the main singing voice synthesis model comes from OpenVPI's DiffSinger, the end-to-end workflow and data processing were extended to suit the needs of my thesis experiments.

### Thesis Topic

This work explores phoneme-mapped cross-lingual transfer learning for singing voice synthesis (SVS), focusing on adapting an English-trained DiffSinger model to German using minimal target-language data. We focus on the **acoustic model** (not the variance model), and investigate how data quality—particularly accent, vocal range, and recording conditions—impacts low-resource SVS performance.

### Installation

Please follow the installation and dependency setup as described in the original [DiffSinger repository](https://github.com/openvpi/DiffSinger). This fork maintains compatibility with the upstream environment and training pipeline.

## Workflow Overview

The experimental pipeline includes the following key stages, with associated scripts and tools:

### 1. Audio Segmentation
- Extract audio: [`mp4_to_wav`](/user_script/00_audio/mp4_to_wav.py)
- Clean audio: [fishaudio preprocess tools](https://github.com/fishaudio/audio-preprocess)
- Auto-slice: [AudioSlicer](https://github.com/openvpi/audio-slicer)
- Manual adjustment (optional): [`slice_audio`, `trim_audio`](user_script/00_audio)

### 2. Lyrics Annotation
- Automatic transcription: [Whisper via fishaudio](https://github.com/fishaudio/audio-preprocess)
- Manual annotation (optional): [`lyrics_to_lab`, `check_lab`](user_script/01_lyric)

### 3. Corpus Construction (optional)
- Convert GT-Singer format to DiffSinger format: [`convert`, `cleanup`](user_script/02_corpus)
- Select wavs by target duration: [`filter_by_duration`](user_script/02_corpus)
- Calculate total corpus length: [`calculate_duration`](user_script/02_corpus)
- Clean up folder: [`clean up folder`](user_script/02_corpus)

### 4. Phonetic Dictionary Update
- Check and fill missing words in lexicon: [`check_lexicon`](user_script/03_dictionary)

### 5. Phoneme Alignment (MFA)
- Automatic Alignment using [Montreal Forced Aligner](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner)
- Manual Alignmeny using [Vlabeler](https://github.com/sdercolin/vlabeler)

### 6. Phoneme Mapping (Cross-lingual Transfer)
- Phoneme-to-phoneme mapping via IPA & PHOIBLE: [`phoneme_mapping`](user_script/04_phoneme_mapping/)

### 7. Inference Stimuli Preparation
- ph num english: [colstone/ENG_dur_num](https://github.com/colstone/ENG_dur_num) 
- ph num german switch this file: [`dur_num_dict.txt`](user_script/05_stimuli/dur_num_dict.txt)
- Note sequence: [OpenVPI/SOME](https://github.com/openvpi/SOME)
- f0 and time-step: [OpenVPI MakeDiffSinger](https://github.com/openvpi/MakeDiffSinger)
- Combine multiple ds files (optional): [`combine_ds.py`](user_script/05_stimuli)

### 8. Objective Evaluation
- FFE & MCD: [`user_script/06_objective_evaluation/FFE&MCD/`](user_script/06_objective_evaluation/FFE&MCD/)
- Intelligibility transcription (Whisper): [fishaudio transcribe](https://github.com/fishaudio/audio-preprocess)
- Word Error Rate (WER): [`run_wer_eval.py`](user_script/06_objective_evaluation/Intelligibility/run_wer_eval.py)


## References

### Original Paper & Implementation

- Paper: [DiffSinger: Singing Voice Synthesis via Shallow Diffusion Mechanism](https://arxiv.org/abs/2105.02446)
- Implementation: [OpenVPI/DiffSinger](https://github.com/openvpi/DiffSinger)

### Generative Models & Algorithms

- Denoising Diffusion Probabilistic Models (DDPM): [paper](https://arxiv.org/abs/2006.11239), [implementation](https://github.com/hojonathanho/diffusion)
  - [DDIM](https://arxiv.org/abs/2010.02502) for diffusion sampling acceleration
  - [PNDM](https://arxiv.org/abs/2202.09778) for diffusion sampling acceleration
  - [DPM-Solver++](https://github.com/LuChengTHU/dpm-solver) for diffusion sampling acceleration
  - [UniPC](https://github.com/wl-zhao/UniPC) for diffusion sampling acceleration
- Rectified Flow (RF): [paper](https://arxiv.org/abs/2209.03003), [implementation](https://github.com/gnobitab/RectifiedFlow)

### Dependencies & Submodules

- [RoPE](https://github.com/lucidrains/rotary-embedding-torch) for transformer encoder
- [HiFi-GAN](https://github.com/jik876/hifi-gan) and [NSF](https://github.com/nii-yamagishilab/project-NN-Pytorch-scripts/tree/master/project/01-nsf) for waveform reconstruction
- [pc-ddsp](https://github.com/yxlllc/pc-ddsp) for waveform reconstruction
- [RMVPE](https://github.com/Dream-High/RMVPE) and yxlllc's [fork](https://github.com/yxlllc/RMVPE) for pitch extraction
- [Vocal Remover](https://github.com/tsurumeso/vocal-remover) and yxlllc's [fork](https://github.com/yxlllc/vocal-remover) for harmonic-noise separation

### External Tools and Related Repositories

The following repositories are used as part of the data preparation and evaluation pipeline described in the Workflow Overview:

- [OpenVPI/AudioSlicer](https://github.com/openvpi/audio-slicer) – Automatic audio slicing
- [OpenVPI/MakeDiffSinger](https://github.com/openvpi/MakeDiffSinger) – Data preprocessing utilities
- [OpenVPI/SOME](https://github.com/openvpi/SOME) – Note duration extraction
- [fishaudio/audio-preprocess](https://github.com/fishaudio/audio-preprocess) – Audio cleaning and Whisper-based lyric transcription
- [PHOIBLE](https://github.com/phoible/dev) - Phoible phonological feature database
- [Montreal Forced Aligner (MFA)](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner) – Phoneme-level alignment
- [Vlabeler](https://github.com/sdercolin/vlabeler) -manual phoneme-level alignment
- [colstone/ENG_dur_num](https://github.com/colstone/ENG_dur_num) – Duration-number mapping utilities
- [GTSinger](https://github.com/AaronZ345/GTSinger) - Dataset 

## Disclaimer

Any organization or individual is prohibited from using any functionalities included in this repository to generate someone's speech without his/her consent, including but not limited to government leaders, political figures, and celebrities. If you do not comply with this item, you could be in violation of copyright laws.

## License

This forked DiffSinger repository is licensed under the [Apache 2.0 License](LICENSE).
