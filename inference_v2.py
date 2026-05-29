import os
import time
import torch
import torchaudio as ta
from pathlib import Path
from chatterbox.tts import ChatterboxTTS

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"運行裝置: {device.upper()}")

print("\n" + "="*70)
print("正在載入 Chatterbox 模型...")
print("="*70)
model = ChatterboxTTS.from_pretrained(device=device)

# 1. 定義 3 種文本 (Prompts) - 需與 Parler 保持完全一致以求公平
prompts = {
    "P1_Joy": "Oh my goodness, you won't believe what just happened! We actually got the funding for our research project! Let's celebrate right now!",
    "P2_Grief": "I... I didn't think it would end this way. Everything we built over the last few years... it's just gone. Just like that.",
    "P3_Tech": "Automatic speech recognition relies heavily on extracting acoustic features from raw audio signals, converting continuous waveforms into discrete tokens."
}

# 2. 定義 ESD 的 4 位語者 與 5 種情緒
esd_base_path = Path("/share/nas169/wago/data/Emotion Speech Dataset")
speakers = ["0012", "0016", "0017", "0020"]
emotions = ["Angry", "Happy", "Neutral", "Sad", "Surprise"]

output_dir = "output_chatterbox"
os.makedirs(output_dir, exist_ok=True)
perf_summary = []

current_case = 1
total_cases = len(prompts) * len(speakers) * len(emotions)

# 3D 矩陣迴圈：語者 -> 情緒 -> 文本
for spk in speakers:
    for emo in emotions:
        # 自動尋找該語者、該情緒資料夾下的第一支 .wav 檔案
        target_dir = esd_base_path / spk / emo
        wav_files = list(target_dir.glob("*.wav"))
        
        if not wav_files:
            print(f"⚠️ 找不到路徑或音訊檔: {target_dir}，跳過 {spk}_{emo} 相關的 3 個測試。")
            current_case += 3
            continue
            
        ap_path = str(wav_files[0]) # 取第一支音訊作為 Reference
        
        for p_name, p_text in prompts.items():
            case_id = f"ESD{spk}_{emo}_{p_name}"
            print(f"[{current_case}/{total_cases}] 正在生成: {case_id} (使用 reference: {Path(ap_path).name})...")
            
            if device == "cuda": torch.cuda.synchronize()
            start_time = time.perf_counter()
            
            with torch.no_grad():
                wav = model.generate(p_text, audio_prompt_path=ap_path)
                
            if device == "cuda": torch.cuda.synchronize()
            end_time = time.perf_counter()
            
            audio_duration = wav.shape[-1] / model.sr
            rtf = (end_time - start_time) / audio_duration if audio_duration > 0 else 0
            
            wav_cpu = wav.cpu() if isinstance(wav, torch.Tensor) else torch.tensor(wav)
            if wav_cpu.ndim == 1: wav_cpu = wav_cpu.unsqueeze(0)
            
            ta.save(os.path.join(output_dir, f"{case_id}.wav"), wav_cpu, model.sr)
            perf_summary.append({"case": case_id, "rtf": f"{rtf:.4f}"})
            current_case += 1

print("\n測試完成！檔案已儲存至:", output_dir)
print(f'perf_summary: {perf_summary}')