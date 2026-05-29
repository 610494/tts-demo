import os
import shutil
from pathlib import Path

# 1. 基本路徑設定
output_site_dir = "docs"
audio_dest_dir = os.path.join(output_site_dir, "audio", "turbo_compare")
os.makedirs(audio_dest_dir, exist_ok=True)

# 來源目錄 (請確定終端機是在包含這個資料夾的目錄下執行的)
generated_dir = "output_chatterbox/turbo_compare"
esd_base_path = Path("/share/nas169/wago/data/Emotion Speech Dataset")

prompts = {
    "P1_Joy": "Oh my goodness, you won't believe what just happened! We actually got the funding for our research project! Let's celebrate right now!",
    "P2_Grief": "I... I didn't think it would end this way. Everything we built over the last few years... it's just gone. Just like that.",
    "P3_Tech": "Automatic speech recognition relies heavily on extracting acoustic features from raw audio signals, converting continuous waveforms into discrete tokens."
}

long_audio_map = {
    "0012": {"Angry": "0012_000363.wav", "Happy": "0012_000955.wav", "Sad": "0012_001324.wav", "Surprise": "0012_001607.wav"},
    "0016": {"Sad": "0016_001081.wav"},
    "0017": {"Angry": "0017_000363.wav", "Sad": "0017_001305.wav"},
    "0020": {"Happy": "0020_000728.wav", "Sad": "0020_001063.wav", "Surprise": "0020_001413.wav"}
}

speakers = ["0012", "0016", "0017", "0020"]
emotions = ["Angry", "Happy", "Neutral", "Sad", "Surprise"]

# 2. HTML 網頁頭部
html_head = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatterbox TTS: Base vs Turbo (Fair Comparison)</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; line-height: 1.6; max-width: 1400px; margin: 0 auto; padding: 20px; color: #333; }
        h1 { border-bottom: 2px solid #eaecef; padding-bottom: 10px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        th, td { border: 1px solid #dfe2e5; padding: 10px; text-align: left; vertical-align: middle; }
        th { background-color: #f6f8fa; font-weight: 600; }
        audio { width: 200px; height: 35px; display: block; }
        .text-content { font-style: italic; color: #555; font-size: 14px; }
        .badge { background: #0366d6; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; display: inline-block; margin-top: 5px; }
        .nav-link { display: inline-block; margin-bottom: 20px; font-weight: bold; color: #0366d6; text-decoration: none; }
        .nav-link:hover { text-decoration: underline; }
        .model-header { text-align: center; background-color: #e8f0fe; color: #1a73e8; }
        .model-header-turbo { text-align: center; background-color: #fce8e6; color: #d93025; }
        .missing { color: red; font-size: 12px; }
    </style>
</head>
<body>
    <a href="index.html" class="nav-link">← Back to Main Menu</a>
    <h1>Chatterbox TTS: Base vs. Turbo Architecture</h1>
    <p>This page compares the standard Chatterbox model against the Turbo version. Both models are conditioned on the <b>exact same >5s reference audio</b> to ensure a fair evaluation of prosody, emotion preservation, and voice cloning quality.</p>
    <table>
        <thead>
            <tr>
                <th style="width: 10%">Speaker & Emotion</th>
                <th style="width: 25%">Target Text</th>
                <th style="width: 20%">Reference Audio (>5s)</th>
                <th class="model-header" style="width: 22.5%">Base Model Result</th>
                <th class="model-header-turbo" style="width: 22.5%">Turbo Model Result</th>
            </tr>
        </thead>
        <tbody>
"""

html_body = ""

# 3. 動態生成表格內容
found_pairs = 0
for spk in speakers:
    for emo in emotions:
        if emo not in long_audio_map.get(spk, {}):
            continue
            
        ref_filename = long_audio_map[spk][emo]
        ref_src = esd_base_path / spk / emo / ref_filename
        
        # 寬容處理：就算找不到 ESD 原始檔，也只是標記出來，繼續往下處理生成的音檔
        ref_dest_name = f"ref_{spk}_{emo}_long.wav"
        ref_html = ""
        if ref_src.exists():
            shutil.copy(ref_src, os.path.join(audio_dest_dir, ref_dest_name))
            ref_html = f'<audio controls preload="none" src="audio/turbo_compare/{ref_dest_name}"></audio>'
        else:
            print(f"⚠️ 找不到參考音檔: {ref_src}")
            ref_html = '<span class="missing">Reference Audio Missing</span>'
        
        for p_name, p_text in prompts.items():
            base_file_name = f"ESD{spk}_{emo}_{p_name}.wav"
            turbo_file_name = f"ESD{spk}_{emo}_{p_name}_turbo.wav"
            
            base_src = os.path.join(generated_dir, base_file_name)
            turbo_src = os.path.join(generated_dir, turbo_file_name)
            
            base_exists = os.path.exists(base_src)
            turbo_exists = os.path.exists(turbo_src)
            
            # 如果兩個都存在，才寫入 HTML
            if base_exists and turbo_exists:
                shutil.copy(base_src, os.path.join(audio_dest_dir, base_file_name))
                shutil.copy(turbo_src, os.path.join(audio_dest_dir, turbo_file_name))
                found_pairs += 1
                
                row_html = f"""
            <tr>
                <td><b>Spk {spk}</b><br><span class="badge">{emo}</span></td>
                <td class="text-content">{p_text}</td>
                <td>{ref_html}</td>
                <td><audio controls preload="none" src="audio/turbo_compare/{base_file_name}"></audio></td>
                <td><audio controls preload="none" src="audio/turbo_compare/{turbo_file_name}"></audio></td>
            </tr>"""
                html_body += row_html
            else:
                # 幫你找出到底是缺了誰！
                if not base_exists:
                    print(f"❌ 找不到 Base 音檔: {base_src}")
                if not turbo_exists:
                    print(f"❌ 找不到 Turbo 音檔: {turbo_src}")

# 4. 組合 HTML 尾部並寫入檔案
html_tail = """
        </tbody>
    </table>
</body>
</html>
"""

final_html = html_head + html_body + html_tail

html_output_path = os.path.join(output_site_dir, "chatterbox_compare.html")
with open(html_output_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print("\n" + "="*50)
print(f"✅ Chatterbox Base vs Turbo 網頁生成完畢！")
print(f"✅ 成功寫入 {found_pairs} 對比較資料。")
print("="*50)
if found_pairs == 0:
    print("⚠️ 警告：寫入數為 0！請檢查上面印出的紅色 ❌ 錯誤路徑，確認你的音檔是不是真的放在那裡。")