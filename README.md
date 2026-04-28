# 🎙 Vocal Remover Pro

**فصل الأصوات عن الموسيقى باحترافية باستخدام الذكاء الاصطناعي**

واجهة ويب جميلة وسهلة الاستخدام لفصل الأصوات عن الموسيقى الخلفية. مثالي للموسيقيين، المنتجين، ومحبي الكاريوكي.

![الحالة](https://img.shields.io/badge/الحالة-مستقر-green)
![الرخصة](https://img.shields.io/badge/الرخصة-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![التقنية](https://img.shields.io/badge/FastAPI-PyTorch-red)

---

## ✨ المميزات الرئيسية

- 🎯 **فصل دقيق**: فصل الأصوات عن الموسيقى باستخدام أحدث نماذج AI (Demucs)
- ⚡ **معالجة سريعة**: دعم تسريع GPU مع CUDA لمعالجة أسرع بـ 10x
- 📱 **يعمل على جميع الأجهزة**: كمبيوتر، موبايل، تابلت - أي متصفح
- 🌐 **واجهة عربية وإنجليزية**: واجهة مستخدم كاملة باللغتين
- 📊 **شريط تقدم مباشر**: تابع حالة المعالجة لحظة بلحظة
- 🎵 **دعم صيغ متعددة**: MP3, WAV, FLAC, AAC, OGG
- 🔗 **فصل من روابط**: حمل مباشرة من YouTube أو أي رابط صوتي
- ❌ **زر إلغاء**: أوقف أي عملية في أي وقت
- 🖥️ **تطبيق سطح مكتب**: متاح كـ .exe للويندوز
- 📲 **تطبيق موبايل**: أضفه للشاشة الرئيسية واستخدمه كتطبيق أصلي

---

## 📁 هيكل المشروع

```
vocal-remover-pro/
├── backend/
│   ├── main.py        ← خادم FastAPI (جميع نقاط API)
│   └── engine.py      ← محرك الفصل (PyTorch / Demucs)
├── frontend/
│   └── index.html     ← تطبيق صفحة واحدة كامل (سحب وإفلات، شريط تقدم، إعدادات)
├── outputs/           ← يُنشأ تلقائياً عند أول تشغيل
├── run.py             ← مشغل بنقرة واحدة
├── build.py           ← حزمة كـ .exe
├── requirements.txt   ← المتطلبات
└── README.md          ← هذا الملف
```

---

## 🚀 البدء السريع

### الطريقة 1: التشغيل المباشر (موصى به للتجربة)

```bash
# 1. استنساخ المشروع
git clone https://github.com/YOUR_USERNAME/vocal-remover-pro.git
cd vocal-remover-pro

# 2. تثبيت المتطلبات
pip install -r requirements.txt

# 3. تشغيل التطبيق
python run.py
```

سيتم:
- تشغيل الخادم على **http://127.0.0.1:7070**
- فتح المتصفح تلقائياً
- يمكنك الوصول لوثائق API على **http://127.0.0.1:7070/docs**

### الطريقة 2: مع تسريع GPU (أسرع بـ 10x)

```bash
# لو عندك كارت شاشة NVIDIA
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
python run.py
```

---

## 📋 المتطلبات الأساسية

| الأداة | الإصدار | التثبيت |
|--------|---------|---------|
| Python | 3.10 أو أحدث | [python.org](https://python.org) |
| ffmpeg | أي إصدار | [ffmpeg.org](https://ffmpeg.org) - أضفه للـ PATH |
| CUDA (اختياري) | 11.8 / 12.x | لتسريع GPU |

### تثبيت ffmpeg

**Windows:**
```bash
winget install ffmpeg
# أو حمل من: https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
sudo dnf install ffmpeg  # Fedora
```

---

## 🎯 كيفية الاستخدام

### استخدام الواجهة الرسومية

1. افتح المتصفح على `http://127.0.0.1:7070`
2. اسحب وأفلت ملف صوتي أو الصق رابط URL
3. اضغط زر **"فصل"** لبدء المعالجة
4. تابع شريط التقدم المباشر
5. اضغط **"إلغاء"** في أي وقت لإيقاف العملية
6. حمّل النتيجة (vocals فقط أو الموسيقى فقط أو الكل)

### استخدام API برمجياً

```python
import requests
import json

BASE = "http://127.0.0.1:7070"

# 1. رفع ملف
with open("song.mp3", "rb") as f:
    r = requests.post(f"{BASE}/api/separate",
                      files={"file": f},
                      data={"config_json": json.dumps({"model_name": "htdemucs_ft"})})
job_id = r.json()["job_id"]

# 2. متابعة التقدم
stream = requests.get(f"{BASE}/api/progress/{job_id}", stream=True)
for line in stream.iter_lines():
    if line.startswith(b"data:"):
        event = json.loads(line[5:])
        print(f"التقدم: {event}")
        if event["type"] == "done":
            break

# 3. تحميل النتيجة
r = requests.get(f"{BASE}/api/download/{job_id}")
with open("vocals.wav", "wb") as f:
    f.write(r.content)

# 4. إلغاء عملية (في أي وقت)
requests.delete(f"{BASE}/api/job/{job_id}")
```

---

## 🔌 نقاط API المتاحة

| الطريقة | النقطة | الوصف |
|---------|--------|-------|
| `POST` | `/api/separate` | رفع ملف → يرجع `job_id` |
| `POST` | `/api/separate-url` | تحميل من رابط (YouTube) → `job_id` |
| `GET` | `/api/progress/{id}` | **بث مباشر** - تقدم المعالجة |
| `GET` | `/api/download/{id}` | تحميل الصوت المفصول |
| `GET` | `/api/stems/{id}/{stem}` | تحميل مسار منفرد (vocals/drums/bass/other) |
| `GET` | `/api/job/{id}` | حالة المهمة (JSON) |
| `DELETE` | `/api/job/{id}` | **إلغاء + تنظيف** |
| `POST` | `/api/cancel/{id}` | إلغاء مهمة جارية |
| `GET` | `/api/config` | الحصول على الإعدادات الحالية |
| `POST` | `/api/config` | حفظ الإعدادات |
| `GET` | `/api/system` | معلومات النظام (GPU, RAM, ffmpeg) |

---

## ⚙️ الإعدادات والتخصيص

الإعدادات تُحفظ في `~/.vocal_remover_pro_config.json`.

| المفتاح | الافتراضي | الوصف |
|---------|----------|-------|
| `model_name` | `htdemucs_ft` | نموذج AI: `htdemucs_ft` / `htdemucs` / `mdx` / `demucs` |
| `segment` | `8.0` | طول الجزء بالثواني |
| `overlap` | `1.0` | التداخل بين الأجزاء |
| `shifts` | `3` | عدد التحولات الزمنية |
| `output_format` | `wav` | الصيغة: `wav` / `mp3` / `flac` / `aac` / `ogg` |
| `output_all_stems` | `false` | تصدير جميع المسارات منفصلة |
| `device` | `auto` | الجهاز: `auto` / `cuda` / `cpu` |
| `audio_bitrate` | `256k` | جودة الصيغ المضغوطة |
| `adaptive_mode` | `true` | ضبط تلقائي حسب الجهاز |

---

## 📱 الاستخدام على الموبايل (تطبيق ويب تقدمي)

التطبيق يعمل كتطبيق ويب تقدمي (PWA) - لا يحتاج تثبيت!

### على الشبكة المحلية:

1. شغّل الخادم: `python run.py --host 0.0.0.0`
2. اعرف عنوان IP المحلي لجهازك (مثلاً `192.168.1.100`)
3. على الموبايل، افتح: `http://192.168.1.100:7070`
4. **Android**: القائمة → "إضافة للشاشة الرئيسية"
5. **iOS**: مشاركة سفاري → "إضافة للشاشة الرئيسية"

الآن التطبيق يعمل كتطبيق أصلي على موبايلك! 📲

---

## 🖥️ الحزمة كتطبيق سطح مكتب

### ويندوز (.exe)

```bash
# تثبيت PyInstaller
pip install pyinstaller

# بناء التطبيق
python build.py

# أو استخدم ملف الدفعات
build_exe.bat
```

**المخرج**: `dist/VocalRemoverPro/VocalRemoverPro.exe`

> ⚠️ وزّع المجلد كاملاً (وليس فقط .exe) لأنه يحتوي على ملفات DLL المطلوبة.

عند النقر المزدوج على `.exe`:
- يبدأ خادم FastAPI في الخلفية
- يفتح المتصفح تلقائياً

### ماك (.app)

```bash
python build.py
# لإضافة علم --windowed، عدّل build.py
```

### لينكس (AppImage)

```bash
pip install pyinstaller
python build.py
# ثم غلّف المجلد بـ appimagetool
```

---

## 🏭 النشر للإنتاج

للحصول على أداء أفضل مع عدة مستخدمين:

```bash
# مع Nginx كـ reverse proxy (موصى به)
uvicorn backend.main:app --host 0.0.0.0 --port 7070 --workers 1

# أو مع gunicorn (لينكس/ماك)
gunicorn backend.main:app -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:7070
```

> **ملاحظة**: استخدم `--workers 1` - ذاكرة التخزين المؤقت للنموذج ليست آمنة للعمليات المتعددة بعد.

---

## 🐛 حل المشاكل الشائعة

| المشكلة | الحل |
|---------|------|
| `ffmpeg not found` | ثبّت ffmpeg وأضفه للـ PATH |
| `CUDA out of memory` | قلّل `segment` إلى 4 ثواني أو استخدم نموذج `mdx` |
| `yt-dlp not installed` | `pip install yt-dlp` |
| تحميل النموذج بطيء | النماذج تُحمّل مرة واحدة من HuggingFace (~300MB) |
| المنفذ مستخدم | `python run.py --port 8080` |
| خطأ في الذاكرة | أغلق التطبيقات الأخرى أو استخدم `long_file_mode: chunk` |

---

## 📚 الأسئلة الشائعة

### س: هل يعمل بدون إنترنت؟
ج: نعم! بعد تحميل النماذج أول مرة، كل المعالجة تتم محلياً بدون إنترنت.

### س: ما الفرق بين النماذج المختلفة؟
ج: 
- `htdemucs_ft`: الأفضل دقةً (موصى به)
- `htdemucs`: سريع وجيد
- `mdx`: متوازن
- `demucs`: الأسرع لكن أقل دقة

### س: كم يستغرق الفصل؟
ج: يعتمد على:
- طول الملف
- قوة جهازك (GPU أسرع 10x)
- إعدادات النموذج
عادةً: دقيقة واحدة لكل دقيقة صوت على CPU، 6 ثواني على GPU.

### س: هل يمكنني فصل أكثر من ملف؟
ج: نعم! ارفع ملفات متعددة وستُعالج بالتتابع.

---

## 🤝 المساهمة

نرحب بالمساهمات! طالع الملفات التالية:
- [دليل المساهمة](CONTRIBUTING.md)
- [دليل المصدر المفتوح](OPEN_SOURCE_GUIDE_AR.md)
- [دليل استكشاف الأخطاء](TROUBLESHOOTING_AR.md)

---

## 📄 الرخصة

هذا المشروع مرخص تحت رخصة [MIT](LICENSE).

---

## 🙏 شكر وتقدير

- نموذج [Demucs](https://github.com/facebookresearch/demucs) من Meta Research
- مكتبة [FastAPI](https://fastapi.tiangolo.com/)
- مجتمع المصادر المفتوحة

---

## 📬 التواصل

- 📧 البريد: your-email@example.com
- 💬 المشاكل: [GitHub Issues](https://github.com/YOUR_USERNAME/vocal-remover-pro/issues)
- 🌟 إذا أعجبك المشروع، لا تنسى وضع نجمة ⭐

---

**صُنع بحب ❤️ للمجتمع العربي والعالمي**
