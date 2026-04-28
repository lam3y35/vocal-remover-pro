# المشاكل المعروفة والحلول المقترحة
## Known Issues and Proposed Solutions

تم تطبيق الحلول التالية في هذا الإصدار:
The following solutions have been implemented in this version:

---

### 1. الإلغاء الفعلي (True Cancellation)

**المشكلة:** زر الإلغاء يغير الحالة لكن العملية قد تستمر في الخلفية.

**الحل المطبق:**
- استخدام `threading.Event()` للإشارة إلى العملية بالتوقف
- إضافة نقاط فحص (checkpoints) في جميع مراحل المعالجة
- معالجة الاستثناء `asyncio.CancelledError` بشكل صحيح

**التنفيذ:**
```python
# في backend/engine.py
self.stop_event = threading.Event()

def check_cancelled(self) -> bool:
    return self.stop_event.is_set()

# في كل مرحلة من المعالجة
if self.check_cancelled():
    raise asyncio.CancelledError("Operation cancelled by user")
```

**في API:**
```python
# في backend/main.py
JOB_STOP_EVENTS: Dict[str, threading.Event] = {}

def cancel_job_execution(job_id: str):
    if job_id in JOB_STOP_EVENTS:
        JOB_STOP_EVENTS[job_id].set()
```

---

### 2. الملفات الكبيرة جداً (ساعتين+)

**المشكلة:** الوقت الطويل للملفات الكبيرة.

**الحلول المقترحة:**

#### أ. تقسيم الملف إلى أجزاء (Chunking)
```python
# يمكن تفعيل هذا الوضع في الإعدادات
config = {
    "long_file_mode": "chunk",
    "chunk_minutes": 10,
}
```

#### ب. المعالجة المتوازية (Parallel Processing)
```python
# معالجة الأجزاء بالتوازي إذا كان GPU متاحاً
if config.get('parallel_processing', False):
    # استخدام multiprocessing أو concurrent.futures
    pass
```

#### ج. استخدام GPU مخصص
```bash
# للتثبيت مع دعم CUDA
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**ملاحظة:** وضع التقسيم التلقائي متاح في الإعدادات:
- `long_file_mode`: "auto" | "chunk" | "full"
- `chunk_minutes`: عدد الدقائق لكل جزء (افتراضي: 10)

---

### 3. تحميل الملفات من URL

**المشكلة:** الكود الحالي يحاكي التحميل فقط.

**الحل المطبق:**
تم إضافة ملف `backend/url_downloader.py` باستخدام مكتبة `yt-dlp`:

```python
# في backend/url_downloader.py
import yt_dlp

def download_audio_from_url(url, output_dir, progress_callback=None):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
```

**المتطلبات:**
```bash
pip install yt-dlp>=2024.1.0
```

**الاستخدام:**
```bash
# من خلال API
POST /api/separate-url
Form: url=https://youtube.com/watch?v=...

# أو مباشرة
python backend/url_downloader.py <URL>
```

**المواقع المدعومة:**
- YouTube
- SoundCloud
- Bandcamp
- Vimeo
- وأكثر من 1000 موقع آخر عبر yt-dlp

---

## ملفات المشروع المحدثة

### `/workspace/backend/engine.py`
- ✅ إضافة `threading.Event()` للإلغاء
- ✅ إضافة `check_cancelled()` في جميع المراحل
- ✅ معالجة `asyncio.CancelledError`

### `/workspace/backend/main.py`
- ✅ إضافة `JOB_STOP_EVENTS` global dict
- ✅ تحديث `run_separation_engine()` لدعم الإلغاء
- ✅ تحديث `cancel_job()` لاستدعاء `cancel_job_execution()`
- ✅ دمج `url_downloader` في معالجة URLs

### `/workspace/backend/url_downloader.py` (جديد)
- ✅ تحميل من YouTube ومواقع أخرى
- ✅ تحويل تلقائي إلى WAV
- ✅ تقارير تقدم مفصلة

### `/workspace/requirements.txt`
- ✅ `yt-dlp>=2024.1.0` مضاف بالفعل

---

## اختبار الميزات

### 1. اختبار الإلغاء
```bash
# تشغيل الخادم
python backend/main.py

# في نافذة أخرى، إرسال طلب إلغاء
curl -X DELETE http://localhost:7070/api/job/<job_id>
```

### 2. اختبار تحميل URL
```bash
# تحميل من YouTube
curl -X POST http://localhost:7070/api/separate-url \
  -F "url=https://youtube.com/watch?v=VIDEO_ID"
```

### 3. مراقبة التقدم
```bash
# الاتصال بـ SSE stream
curl http://localhost:7070/api/progress/<job_id>
```

---

## ملاحظات الأداء

### للملفات الطويلة (> 30 دقيقة):
1. استخدم وضع التقسيم (`chunk_minutes: 10`)
2. فعّل معالجة GPU إذا كانت متاحة
3. قلل `shifts` إلى 0 لزيادة السرعة

### للذاكرة المحدودة:
```python
config = {
    "segment": 8.0,  # تقليل حجم القطعة
    "overlap": 0.5,  # تقليل التداخل
    "shifts": 0,     # تعطيل التحولات
}
```

---

## التحديثات المستقبلية المقترحة

1. **معالجة متوازية حقيقية للأجزاء**
   - استخدام `concurrent.futures.ProcessPoolExecutor`
   
2. **دعم الحفظ السحابي**
   - رفع النتائج مباشرة إلى Google Drive / Dropbox
   
3. **واجهة ويب محسّنة**
   - شريط تقدم تفاعلي
   - معاينة قبل التحميل

4. **وضع الدفعات (Batch Mode)**
   - معالجة ملفات متعددة في وقت واحد

---

**آخر تحديث:** 2024
**الإصدار:** 1.0.0
