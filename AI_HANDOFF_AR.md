# دليل تسليم السياق للذكاء الاصطناعي (AI Handoff Guide)

## حالة المشروع الحالية
المشروع عبارة عن تطبيق فصل أصوات متقدم يعمل على:
- **السيرفر السحابي:** Hugging Face Spaces (Docker)
- **النسخة الحالية:** 2.0.0
- **المحرك:** HT-Demucs
- **الواجهة:** Gradio

## المكونات الرئيسية

### 1. ملفات التطبيق الأساسية
| الملف | الوصف |
|------|-------|
| `app_cloud.py` | كود التطبيق الرئيسي (Gradio + Demucs) |
| `requirements_cloud.txt` | مكتبات بايثون المطلوبة |
| `Dockerfile` | إعداد بيئة التشغيل السحابية |
| `update_manifest.json` | ملف التحديثات التلقائية |

### 2. ملفات الدعم والتوثيق
| الملف | الوصف |
|------|-------|
| `README.md` | دليل المستخدم الرئيسي |
| `CONTRIBUTING.md` | دليل المساهمين |
| `TROUBLESHOOTING_AR.md` | حل المشاكل الشائعة |
| `OPEN_SOURCE_GUIDE_AR.md` | دليل العمل مفتوح المصدر |
| `.github/ISSUE_TEMPLATE/*` | قوالب الإبلاغ عن المشاكل وطلب الميزات |

## الميزات المُطبّقة

✅ **فصل الأصوات:** دعم كامل لفصل Vocals, Drums, Bass, Other  
✅ **زر الإلغاء:** إمكانية إيقاف أي عملية في أي وقت  
✅ **شريط التقدم:** عرض تقدم المعالجة بشكل مباشر  
✅ **نظام التحديثات:** التحقق التلقائي من وجود نسخ جديدة  
✅ **التشخيص الذكي:** تقرير JSON جاهز لتحليل المشاكل  
✅ **دعم URL:** معالجة الروابط المباشرة (قيد التطوير)  
✅ **واجهة متجاوبة:** تعمل على الموبايل واللاب  

## المشاكل المعروفة والحلول المقترحة

### 1. الإلغاء الفعلي (True Cancellation)
**المشكلة:** زر الإلغاء يغير الحالة لكن العملية قد تستمر في الخلفية.  
**الحل المقترح:** استخدام `threading.Event()` أو `concurrent.futures` مع timeout.

```python
import threading
stop_event = threading.Event()

def separate_audio(...):
    for step in processing_steps:
        if stop_event.is_set():
            return "تم الإلغاء"
        # متابعة المعالجة
```

### 2. الملفات الكبيرة جداً (ساعتين+)
**المشكلة:** الوقت الطويل للملفات الكبيرة.  
**الحل المقترح:** 
- تقسيم الملف إلى أجزاء (chunking)
- معالجة متوازية (parallel processing)
- استخدام GPU مخصص على Hugging Face Pro

### 3. تحميل الملفات من URL
**المشكلة:** الكود الحالي يحاكي التحميل فقط.  
**الحل المقترح:** إضافة مكتبة `yt-dlp` أو `requests` لتحميل فعلي.

```python
import yt_dlp

def download_from_url(url):
    ydl_opts = {'format': 'bestaudio'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        # تحميل الملف
```

## المطلوب من الذكاء الاصطناعي التالي

### الأولويات القصوى
1. **تفعيل الإلغاء الحقيقي:** ربط `cancel_flag` بحلقة المعالجة الفعلية في Demucs.
2. **تحميل URL حقيقي:** دمج `yt-dlp` لدعم مئات المواقع (YouTube, SoundCloud, etc.).
3. **تحسين شريط التقدم:** استخدام callback من Demucs لتحديث progress بدقة.

### تحسينات مقترحة
- إضافة دعم للغات متعددة في الواجهة.
- حفظ سجل العمليات (History) لكل مستخدم.
- إضافة معاينة صوتية قبل التحميل.
- ضغط الملفات المفصولة قبل التحميل (ZIP).

## روابط مهمة
- **مستودع GitHub:** `https://github.com/YOUR_USERNAME/YOUR_REPO`
- **Hugging Face Space:** `https://huggingface.co/spaces/YOUR_USERNAME/vocal-remover-pro`
- **توثيق Demucs:** `https://github.com/facebookresearch/demucs`
- **توثيق Gradio:** `https://gradio.app/docs`

## ملاحظات للنشر
- عند كل تحديث، عدّل `VERSION` في `app_cloud.py` و `update_manifest.json`.
- ارفع ملف ZIP في GitHub Releases.
- حدّث رابط التحميل في `update_manifest.json`.

---
**آخر تحديث:** 2024-01-15  
**بواسطة:** AI Assistant
