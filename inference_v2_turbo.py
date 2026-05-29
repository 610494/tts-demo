import os
import time
import torch
import torchaudio as ta
from pathlib import Path
from chatterbox.tts_turbo import ChatterboxTurboTTS

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"運行裝置: {device.upper()}")

print("\n" + "="*70)
print("正在載入 Chatterbox Turbo 模型...")
print("="*70)

model = ChatterboxTurboTTS.from_pretrained(device=device)

prompts = {
    "P1_Joy": "Oh my goodness, you won't believe what just happened! We actually got the funding for our research project! Let's celebrate right now!",
    "P2_Grief": "I... I didn't think it would end this way. Everything we built over the last few years... it's just gone. Just like that.",
    "P3_Tech": "Automatic speech recognition relies heavily on extracting acoustic features from raw audio signals, converting continuous waveforms into discrete tokens."
}

esd_base_path = Path("/share/nas169/wago/data/Emotion Speech Dataset")

# 1. 根據你的掃描結果，建立明確的「長音檔」對應表 (只包含大於 5 秒的檔案)
# 如果某個語者缺某個情緒，就會在後面的迴圈被自動跳過
long_audio_map = {
    "0012": {
        "Angry": "0012_000363.wav",
        "Happy": "0012_000955.wav",
        "Sad": "0012_001324.wav",
        "Surprise": "0012_001607.wav"
        # 缺 Neutral
    },
    "0016": {
        "Sad": "0016_001081.wav"
        # 缺 Angry, Happy, Neutral, Surprise
    },
    "0017": {
        "Angry": "0017_000363.wav",
        "Sad": "0017_001305.wav"
        # 缺 Happy, Neutral, Surprise
    },
    "0020": {
        "Happy": "0020_000728.wav",
        "Sad": "0020_001063.wav",
        "Surprise": "0020_001413.wav"
        # 缺 Angry, Neutral
    }
}

speakers = ["0012", "0016", "0017", "0020"]
emotions = ["Angry", "Happy", "Neutral", "Sad", "Surprise"]

output_dir = "output_chatterbox"
os.makedirs(output_dir, exist_ok=True)
perf_summary = []

# --- 預熱機制 (尋找 long_audio_map 裡第一個存在的檔案) ---
if device == "cuda":
    print("正在進行 GPU 預熱...")
    warmup_done = False
    for spk, emo_dict in long_audio_map.items():
        if warmup_done: break
        for emo, filename in emo_dict.items():
            warmup_ap_path = esd_base_path / spk / emo / filename
            if warmup_ap_path.exists():
                print(f"-> 使用 {filename} 進行預熱...")
                with torch.no_grad():
                    _ = model.generate("Warm up step.", audio_prompt_path=str(warmup_ap_path))
                torch.cuda.synchronize()
                warmup_done = True
                break

# --- 開始測試迴圈 ---
current_case = 1
# 因為會有缺漏，總數用動態計算
total_cases = sum(len(emo_dict) for emo_dict in long_audio_map.values()) * len(prompts)

for spk in speakers:
    for emo in emotions:
        # 檢查這個語者的這個情緒，有沒有大於 5 秒的檔案
        if emo not in long_audio_map.get(spk, {}):
            print(f"⚠️ {spk} 缺少 >5s 的 {emo} 音檔，跳過。")
            continue
            
        filename = long_audio_map[spk][emo]
        ap_path = esd_base_path / spk / emo / filename
        
        if not ap_path.exists():
             print(f"⚠️ 找不到實體檔案: {ap_path}，跳過。")
             continue

        for p_name, p_text in prompts.items():
            case_id = f"ESD{spk}_{emo}_{p_name}_turbo"
            print(f"[{current_case}/{total_cases}] 正在生成: {case_id} (使用 >5s reference: {filename})...")
            
            if device == "cuda": torch.cuda.synchronize()
            start_time = time.perf_counter()
            
            with torch.no_grad():
                wav = model.generate(p_text, audio_prompt_path=str(ap_path))
                
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