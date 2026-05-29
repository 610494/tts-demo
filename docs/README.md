# TTS Emotion & Voice Disentanglement Demo

This repository hosts a demonstration of Text-to-Speech (TTS) models, focusing on their ability to disentangle **speaker identity** and **emotional expression**. 

🌐 **[Live Demo Page](https://610494.github.io/tts-demo/)**

---

## 🎯 Experiment Overview

The goal of this experiment is to evaluate the 3D Controllability (Speaker × Emotion × Content) of modern TTS models under zero-shot or prompted conditions. We utilize a **Cross-Matrix Test** to systematically test boundaries and observe potential "emotion leakage."

### Models Evaluated

#### 1. Chatterbox TTS (Zero-Shot Voice Cloning)
* **Control Method:** Driven by extracting acoustic features from a Reference Audio prompt.
* **Methodology:** We utilized reference audio from the ESD dataset. The model must mimic the speaker's voice from the prompt while attempting to apply the requested text, revealing whether the emotion from the reference audio "leaks" into the generated output.

#### 2. Parler-TTS (Mini-Expresso)
* **Control Method:** Driven entirely by natural language style descriptions (Text-Prompted).
* **Methodology:** Instead of reference audio, we crafted specific descriptive prompts to dictate the speaker's identity and emotional state. 
    * *Example Description:* `"Gary's voice is angry and aggressive, with high energy and a loud tone, with a very close recording that almost has no background noise."`

### Dataset & Configuration
* **Reference Audio / Styles**: Derived from the **[Emotion Speech Dataset (ESD)](https://github.com/HLTSingapore/Emotion-Speech-Dataset)**. 
* **Speakers Evaluated**: 4 Speakers (2 Female, 2 Male).
* **Emotions Evaluated**: 5 Categories (`Angry`, `Happy`, `Neutral`, `Sad`, `Surprise`).
* **Target Text (Content)**: 3 varied sentences covering joyful excitement, grief/sadness, and technical jargon to test stability and pronunciation.

---

## ⚡ Performance Benchmark: Real-Time Factor (RTF)

To assess the computational efficiency of these models during inference, we calculated the Real-Time Factor (RTF). A lower RTF indicates faster generation speed relative to the length of the output audio.

*Hardware: Evaluated on an NVIDIA GPU using PyTorch (`cuda` device).*
*Note: The first generation run for Chatterbox (Cold Start) was excluded from this calculation to provide an accurate representation of sustained inference speed.*

| Model | Architecture Type | Control Method | RTF (Mean) | RTF (Std. Dev.) |
| :--- | :--- | :--- | :---: | :---: |
| **Chatterbox TTS** | Voice Cloning | Audio Prompt | **0.5312** | ± 0.0183 |
| **Parler-TTS (Mini-Expresso)** | Autoregressive | Text Prompt | **1.1724** | ± 0.0104 |

**Insights:**
* **Speed:** Chatterbox operates significantly faster (roughly 2x) than Parler-TTS Mini-Expresso in our environment.
* **Stability:** Both models exhibit high stability across varying lengths and emotional complexities, with Parler-TTS showing exceptionally low variance (Std: 0.01) in inference times.

---

## 🚀 How to Navigate the Demo

Visit the **[Demo Site](https://610494.github.io/tts-demo/)** to listen to the generated samples. 

You can view the specific results for each model from the main menu. The tables provide a direct side-by-side comparison between the target text, the provided reference audio (or style description), and the final generated output.