import os
import shutil

# 1. 基本路徑設定
output_site_dir = "docs"
audio_dest_dir = os.path.join(output_site_dir, "audio")
os.makedirs(audio_dest_dir, exist_ok=True)

# 來源目錄 (請根據你的截圖，確認這裡的路徑是否正確)
# 截圖顯示路徑前綴有 outputs/，請確保與你實際路徑完全一致
generated_dir = "/share/nas169/wago/parler-tts/outputs/output_parler_parler-tts-mini-expresso_v2" 

# 2. 定義測項結構 (與你之前生成的設定一致)
speakers = ["Jenna", "Lea", "Gary", "Jon"]
emotions = {
    "Angry": "angry and aggressive, with high energy and a loud tone",
    "Happy": "happy, enthusiastic, and highly energetic, speaking quite fast",
    "Neutral": "calm, professional, and steady, speaking at a moderate pace",
    "Sad": "sad, whispering, and low-energy, taking frequent pauses",
    "Surprise": "amazed and highly surprised, with a dynamic and expressive tone"
}
prompts = {
    "P1_Joy": "Oh my goodness, you won't believe what just happened! We actually got the funding for our research project! Let's celebrate right now!",
    "P2_Grief": "I... I didn't think it would end this way. Everything we built over the last few years... it's just gone. Just like that.",
    "P3_Tech": "Automatic speech recognition relies heavily on extracting acoustic features from raw audio signals, converting continuous waveforms into discrete tokens."
}

# 3. HTML 網頁頭部 (純字串)
html_head = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parler-TTS: Emotion & Text Disentanglement Demo</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; line-height: 1.6; max-width: 1200px; margin: 0 auto; padding: 20px; color: #333; }
        h1 { border-bottom: 2px solid #eaecef; padding-bottom: 10px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        th, td { border: 1px solid #dfe2e5; padding: 12px; text-align: left; vertical-align: middle; }
        th { background-color: #f6f8fa; font-weight: 600; }
        audio { width: 220px; height: 40px; }
        .text-content { font-style: italic; color: #555; }
        .desc-content { font-family: monospace; font-size: 13px; color: #0366d6; background-color: #f1f8ff; padding: 6px; border-radius: 4px; display: block; }
        .badge { background: #28a745; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; display: inline-block; margin-top: 5px; }
        .nav-link { display: inline-block; margin-bottom: 20px; font-weight: bold; color: #0366d6; text-decoration: none; }
        .nav-link:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <a href="index.html" class="nav-link">← Back to Main Menu</a>
    <h1>Parler-TTS (Mini-Expresso): Text-Driven Emotion Control</h1>
    <p>This page demonstrates the expressive capabilities of the Parler-TTS model. Instead of reference audio, speaker identity and emotional tone are controlled entirely via natural language descriptions.</p>
    <table>
        <thead>
            <tr>
                <th style="width: 15%">Speaker & Emotion</th>
                <th style="width: 30%">Target Text (Content)</th>
                <th style="width: 35%">Style Description (Prompt)</th>
                <th style="width: 20%">Generated Audio (Result)</th>
            </tr>
        </thead>
        <tbody>
"""

html_body = ""

# 4. 遍歷組合，複製檔案並動態生成表格內容
found_files = 0
for spk in speakers:
    for emo_name, emo_desc in emotions.items():
        # 這是你當初餵給 Parler 的完整 Description
        full_description = f"{spk}'s voice is {emo_desc}, with a very close recording that almost has no background noise."
        
        for p_name, p_text in prompts.items():
            gen_file_name = f"{spk}_{emo_name}_{p_name}.wav"
            gen_src = os.path.join(generated_dir, gen_file_name)
            
            # 確保生成的音檔存在才寫入 HTML 這一行
            if os.path.exists(gen_src):
                shutil.copy(gen_src, os.path.join(audio_dest_dir, gen_file_name))
                found_files += 1
                
                row_html = f"""
            <tr>
                <td><b>Speaker {spk}</b><br><span class="badge">{emo_name}</span></td>
                <td class="text-content">{p_text}</td>
                <td><span class="desc-content">{full_description}</span></td>
                <td><audio controls preload="none" src="audio/{gen_file_name}"></audio></td>
            </tr>"""
                html_body += row_html
            else:
                print(f"⚠️ 找不到檔案，已跳過: {gen_src}")

# 5. 組合 HTML 尾部並寫入檔案 (命名為 parler.html 以區分 Chatterbox)
html_tail = """
        </tbody>
    </table>
</body>
</html>
"""

final_html = html_head + html_body + html_tail

# 儲存為 parler.html
html_output_path = os.path.join(output_site_dir, "parler.html")
with open(html_output_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"✅ Parler Demo 網頁生成完畢！共處理了 {found_files} 筆音檔。")
print(f"請前往 {output_site_dir}/ 資料夾查看 parler.html")