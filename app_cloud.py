import os
import gradio as gr
import torch
from demucs.pretrained import get_model
from demucs.apply import apply_model
from demucs.audio import save_audio
import tempfile
import json
import time
from datetime import datetime
import threading
import requests
import yt_dlp

# إعدادات النسخة الحالية
VERSION = "2.1.0"
MANIFEST_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/update_manifest.json"

# متغيرات عالمية للتحكم في العملية
stop_event = threading.Event()
current_process = None

def load_model():
    """تحميل النموذج عند بدء التشغيل"""
    print("Loading AI Model...")
    model = get_model('htdemucs')
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Model loaded on {device}")
    return model, device

# تحميل النموذج مرة واحدة
model, device = load_model()

def separate_audio(input_file, progress=gr.Progress()):
    """دالة فصل الأصوات مع دعم الإلغاء الحقيقي وشريط التقدم الدقيق"""
    global stop_event
    
    # إعادة تعيين حدث الإيقاف
    stop_event.clear()
    
    if input_file is None:
        return None, "يرجى رفع ملف صوتي أو إدخال رابط URL أولاً.", []
    
    try:
        start_time = time.time()
        progress(0, desc="جاري التحميل والتحضير...")
        
        # التحقق من الإلغاء
        if stop_event.is_set():
            return None, "تم إلغاء العملية بواسطة المستخدم.", []
        
        # تحميل الملف الصوتي
        from demucs.audio import load_audio
        wav = load_audio(input_file)
        
        progress(0.1, desc="جاري معالجة الملف...")
        
        if stop_event.is_set():
            return None, "تم إلغاء العملية أثناء التحضير.", []
        
        # تطبيق النموذج مع callback للتقدم
        progress(0.3, desc="جاري فصل المسارات الصوتية...")
        
        def progress_callback(state):
            """تحديث شريط التقدم بناءً على حالة Demucs"""
            if stop_event.is_set():
                raise InterruptedError("تم إلغاء العملية بواسطة المستخدم")
            # حساب النسبة المئوية (0.3 إلى 0.8)
            current_progress = 0.3 + (state * 0.5)
            progress(current_progress, desc=f"جاري الفصل... {int(state*100)}%")
        
        # تطبيق الفصل مع دعم الإلغاء
        sources = apply_model(
            model, 
            wav, 
            device=device, 
            progress=True,
            callback=progress_callback if callable(progress_callback) else None
        )
        
        if stop_event.is_set():
            return None, "تم إلغاء العملية قبل الحفظ.", []
        
        progress(0.8, desc="جاري حفظ الملفات المفصولة...")
        
        output_dir = tempfile.mkdtemp()
        stems = ['vocals', 'drums', 'bass', 'other']
        output_files = []
        
        for i, source in enumerate(sources[0]):
            if stop_event.is_set():
                return None, "تم إلغاء العملية أثناء الحفظ.", []
                
            stem_name = stems[i]
            out_path = os.path.join(output_dir, f"{stem_name}.wav")
            save_audio(source, out_path, samplerate=44100)
            output_files.append(out_path)
            
        elapsed = time.time() - start_time
        msg = f"✅ تمت العملية بنجاح في {elapsed:.2f} ثانية!"
        
        return output_files, msg, output_files

    except InterruptedError as e:
        return None, str(e), []
    except Exception as e:
        return None, f"❌ حدث خطأ: {str(e)}", []

def cancel_operation():
    """دالة إلغاء العملية"""
    global stop_event
    stop_event.set()
    return "🛑 جاري إيقاف العملية...", []

def check_for_updates():
    """التحقق من وجود تحديثات"""
    try:
        import requests
        response = requests.get(MANIFEST_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            latest_ver = data.get('version', '0.0.0')
            if latest_ver > VERSION:
                download_url = data.get('download_url', '#')
                return f"⚠️ توجد نسخة جديدة ({latest_ver}) متاحة! [تحميل التحديث]({download_url})"
            return f"✅ أنت تستخدم أحدث نسخة ({VERSION})."
        return "❌ تعذر الاتصال بخادم التحديثات."
    except Exception as e:
        return f"❌ خطأ في التحقق: {str(e)}"

def get_diagnostics():
    """الحصول على بيانات التشخيص"""
    diag = {
        "version": VERSION,
        "device": str(device),
        "cuda_available": torch.cuda.is_available(),
        "timestamp": datetime.now().isoformat(),
        "status": "operational",
        "cancel_supported": True,
        "url_download_supported": True,
        "model": "htdemucs"
    }
    return json.dumps(diag, indent=2, ensure_ascii=False)

def download_from_url(url, progress=gr.Progress()):
    """تحميل ملف صوتي من URL باستخدام yt-dlp"""
    global stop_event
    
    stop_event.clear()
    
    if not url:
        return None, "يرجى إدخال رابط URL صحيح.", []
    
    try:
        progress(0, desc="جاري تجهيز التحميل...")
        
        # إعدادات yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(tempfile.gettempdir(), '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }
        
        progress(0.2, desc="جاري التحميل من الرابط...")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # الحصول على معلومات الفيديو
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'Unknown')
            
            if stop_event.is_set():
                return None, "تم إلغاء التحميل.", []
            
            progress(0.4, desc=f"جاري تحميل: {video_title[:30]}...")
            
            # التحميل الفعلي
            ydl.download([url])
            
            if stop_event.is_set():
                return None, "تم إلغاء التحميل.", []
        
        # البحث عن الملف المحمل
        output_path = None
        for file in os.listdir(tempfile.gettempdir()):
            if file.endswith('.wav') and video_title[:20] in file:
                output_path = os.path.join(tempfile.gettempdir(), file)
                break
        
        if output_path and os.path.exists(output_path):
            progress(0.8, desc="تم التحميل بنجاح، جاري المعالجة...")
            # إعادة استخدام دالة الفصل
            return separate_audio(output_path, progress)
        else:
            return None, "❌ فشل في العثور على الملف المحمل.", []
            
    except Exception as e:
        return None, f"❌ خطأ في التحميل: {str(e)}", []


def process_url(url, progress=gr.Progress()):
    """معالجة رابط URL (تحميل حقيقي الآن)"""
    return download_from_url(url, progress)

# بناء الواجهة
with gr.Blocks(title="Vocal Remover Pro", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎵 Vocal Remover Pro (Cloud Edition)")
    gr.Markdown("افصل الأصوات والآلات الموسيقية بدقة عالية باستخدام الذكاء الاصطناعي. يعمل على Hugging Face Spaces.")
    
    with gr.Tabs():
        with gr.TabItem("📁 رفع ملف"):
            input_audio = gr.Audio(label="رفع ملف صوتي", type="filepath")
            btn_separate_file = gr.Button("🚀 ابدأ فصل الملف", variant="primary")
            
        with gr.TabItem("🔗 رابط URL"):
            input_url = gr.Textbox(label="أدخل رابط الملف الصوتي (URL)", placeholder="https://example.com/audio.mp3")
            btn_process_url = gr.Button("🚀 ابدأ معالجة الرابط", variant="primary")
    
    with gr.Row():
        btn_cancel = gr.Button("🛑 إلغاء العملية", variant="stop", scale=1)
        btn_check_update = gr.Button("🔄 التحقق من التحديثات", scale=1)
        btn_diag = gr.Button("🔍 تقرير التشخيص", scale=1)
    
    with gr.Row():
        output_status = gr.Textbox(label="حالة النظام", interactive=False, lines=2)
        update_status = gr.Textbox(label="حالة التحديثات", interactive=False)
    
    output_audios = gr.File(label="📥 الملفات المفصولة (Vocals, Drums, Bass, Other)", file_count="multiple")
    diag_output = gr.Code(label="بيانات التشخيص", language="json", visible=False)

    # ربط الأزرار بالوظائف
    btn_separate_file.click(
        fn=separate_audio, 
        inputs=[input_audio], 
        outputs=[output_audios, output_status, output_audios]
    )
    
    btn_process_url.click(
        fn=process_url, 
        inputs=[input_url], 
        outputs=[output_audios, output_status, output_audios]
    )
    
    btn_cancel.click(
        fn=cancel_operation, 
        inputs=[], 
        outputs=[output_status, output_audios]
    )
    
    btn_check_update.click(
        fn=check_for_updates, 
        outputs=[update_status]
    )
    
    btn_diag.click(
        fn=get_diagnostics, 
        outputs=[diag_output]
    ).then(
        fn=lambda x: gr.update(visible=True), 
        inputs=[], 
        outputs=[diag_output]
    )

    gr.Markdown("---")
    gr.Markdown(f"**الإصدار الحالي:** {VERSION} | **المحرك:** HT-Demucs | **السيرفر:** Hugging Face Spaces (Docker)")
    gr.Markdown("### تعليمات سريعة:")
    gr.Markdown("- لملفات كبيرة (أكثر من 10 دقائق)، قد تستغرق العملية وقتاً طويلاً.")
    gr.Markdown("- يمكنك إلغاء أي عملية في أي وقت باستخدام زر 'إلغاء العملية'.")
    gr.Markdown("- للتأكد من التحديثات، اضغط على 'التحقق من التحديثات'.")

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
