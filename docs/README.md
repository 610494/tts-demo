# TTS Emotion & Voice Disentanglement Demo

This repository hosts a demonstration of Text-to-Speech (TTS) models, focusing on their ability to disentangle **speaker identity** and **emotional expression**. 

🌐 **[Live Demo Page](https://610494.github.io/tts-demo/)**

---

## 🎯 Experiment Overview

The goal of this experiment is to evaluate the 3D Controllability (Speaker × Emotion × Content) of modern TTS models under zero-shot or prompted conditions.

### Models Evaluated
* **Chatterbox TTS**: A zero-shot voice cloning model driven by reference audio prompts.
* **Parler-TTS (Mini & Expresso)**: A text-driven TTS model controlled by natural language descriptions.

### Dataset & Configuration
* **Reference Audio (Style Prompts)**: Selected from the **[Emotion Speech Dataset (ESD)](https://github.com/HLTSingapore/Emotion-Speech-Dataset)**. 
* **Speakers Evaluated**: 
  * 4 Speakers (2 Female: 0012, 0016 / 2 Male: 0017, 0020)
* **Emotions Evaluated**: 
  * 5 Categories: `Angry`, `Happy`, `Neutral`, `Sad`, `Surprise`.
* **Target Text (Content)**: 
  * 3 varied sentences covering joyful excitement, grief/sadness, and technical jargon to test stability and emotion leakage.

### Evaluation Methodology
We employ a **Cross-Matrix (Disentanglement) Test** generating a total of 60 combinations (4 Speakers × 5 Emotions × 3 Texts) per model. This strict separation allows us to observe if a model suffers from "emotion leakage" (e.g., failing to produce a sad tone when given a sad reference audio but a happy text prompt).

---

## 🚀 How to Navigate the Demo

Visit the **[Demo Site](https://610494.github.io/tts-demo/)** to listen to the generated samples. 
The tables provide a direct side-by-side comparison between the target text, the provided reference audio (or description), and the final generated output.