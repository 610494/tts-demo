import os
import shutil
from pathlib import Path

# 1. 基本路徑設定
output_site_dir = "docs"
audio_dest_dir = os.path.join(output_site_dir, "audio")
os.makedirs(audio_dest_dir, exist_ok=True)

# 來源目錄 (請確保這些路徑與你實際的目錄名稱一致)
generated_dir = "output_chatterbox"
esd_base_path = Path("/share/nas169/wago/data/Emotion Speech Dataset")

speakers = ["0012", "0016", "0017", "0020"]
emotions = ["Angry", "Happy", "Neutral", "Sad", "Surprise"]
prompts = {
    "P1_Joy": "Oh my goodness, you won't believe what just happened! We actually got the funding for our research project! Let's celebrate right now!",
    "P2_Grief": "I... I didn't think it would end this way. Everything we built over the last few years... it's just gone. Just like that.",
    "P3_Tech": "Automatic speech recognition relies heavily on extracting acoustic features from raw audio signals, converting continuous waveforms into discrete tokens."
}

# 2. HTML 網頁頭部 (純字串，不使用 f-string)
html_head = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatterbox TTS: Emotion & Voice Cloning Demo</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; line-height: 1.6; max-width: 1200px; margin: 0 auto; padding: 20px; color: #333; }
        h1 { border-bottom: 2px solid #eaecef; padding-bottom: 10px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        th, td { border: 1px solid #dfe2e5; padding: 12px; text-align: left; vertical-align: middle; }
        th { background-color: #f6f8fa; font-weight: 600; }
        audio { width: 220px; height: 40px; }
        .text-content { font-style: italic; color: #555; }
        .badge { background: #0366d6; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; display: inline-block; margin-top: 5px; }
    </style>
</head>
<body>
    <h1>Chatterbox TTS: Disentanglement of Voice & Emotion</h1>
    <p>This page demonstrates the zero-shot voice cloning capabilities of Chatterbox, using reference audio from the ESD dataset to control speaker identity and emotion.</p>
    <table>
        <thead>
            <tr>
                <th>Speaker & Emotion</th>
                <th>Target Text</th>
                <th>Reference Audio (Prompt)</th>
                <th>Generated Audio (Result)</th>
            </tr>
        </thead>
        <tbody>
"""

html_body = ""

# 3. 遍歷組合，複製檔案並動態生成表格內容
for spk in speakers:
    for emo in emotions:
        # 尋找 Reference Audio
        ref_src = list((esd_base_path / spk / emo).glob("*.wav"))
        if not ref_src:
            continue
            
        ref_file = ref_src[0]
        ref_dest_name = f"ref_{spk}_{emo}.wav"
        
        # 複製 Reference 到 docs/audio
        shutil.copy(ref_file, os.path.join(audio_dest_dir, ref_dest_name))
        
        for p_name, p_text in prompts.items():
            gen_file_name = f"ESD{spk}_{emo}_{p_name}.wav"
            gen_src = os.path.join(generated_dir, gen_file_name)
            
            # 確保生成的音檔存在才寫入 HTML 這一行
            if os.path.exists(gen_src):
                shutil.copy(gen_src, os.path.join(audio_dest_dir, gen_file_name))
                
                # 這裡確保有使用 f 標籤進行變數替換
                row_html = f"""
            <tr>
                <td><b>Speaker {spk}</b><br><span class="badge">{emo}</span></td>
                <td class="text-content">{p_text}</td>
                <td><audio controls preload="none" src="audio/{ref_dest_name}"></audio></td>
                <td><audio controls preload="none" src="audio/{gen_file_name}"></audio></td>
            </tr>"""
                html_body += row_html

# 4. 組合 HTML 尾部並寫入檔案
html_tail = """
        </tbody>
    </table>
</body>
</html>
"""

final_html = html_head + html_body + html_tail

html_output_path = os.path.join(output_site_dir, "index.html")
with open(html_output_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"✅ Demo 網頁生成完畢！共寫入 {html_body.count('<tr>')} 筆資料。")
print(f"請前往 {output_site_dir}/ 資料夾查看 index.html")