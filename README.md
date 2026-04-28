# 🎵 Vocal Remover Pro - الإصدار السحابي

<div dir="rtl">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Hugging Face Spaces](https://img.shields.io/badge/🤗-Hugging%20Face%20Spaces-blue)](https://huggingface.co/spaces)

**افصل الأصوات عن الموسيقى بدقة عالية باستخدام الذكاء الاصطناعي!**

تطبيق متقدم لفصل المسارات الصوتية (Vocals, Drums, Bass, Other) يعمل على أي جهاز من خلال المتصفح.

---

## ✨ الميزات الرئيسية

- 🚀 **يعمل على السحابة**: لا حاجة لتثبيت أي شيء، افتح الرابط واستخدم مباشرة
- 📱 **متجاوب**: يعمل على الموبايل، اللاب توب، والتابلت
- 🛑 **زر إلغاء**: أوقف أي عملية في أي وقت
- 🔄 **تحديثات تلقائية**: تحقق من وجود نسخ جديدة بضغطة زر
- 🔍 **تشخيص ذكي**: تقرير JSON جاهز لحل المشاكل
- 🎯 **دقة عالية**: يستخدم نموذج HT-Demucs الأحدث
- 🌐 **دعم الروابط**: ارفع ملفات أو أدخل روابط URL مباشرة

---

## 🚀 البدء السريع

### خيار 1: استخدام النسخة السحابية (موصى به)

1. افتح رابط Hugging Face Space:
   ```
   https://huggingface.co/spaces/YOUR_USERNAME/vocal-remover-pro
   ```

2. ارفع ملف صوتي أو أدخل رابط URL

3. اضغط "ابدأ فصل الملف"

4. حمّل الملفات المفصولة!

### خيار 2: التشغيل المحلي (للمطورين)

```bash
# استنساخ المشروع
git clone https://github.com/YOUR_USERNAME/vocal-remover-pro.git
cd vocal-remover-pro

# تثبيت المتطلبات
pip install -r requirements_cloud.txt

# تشغيل التطبيق
python app_cloud.py

# افتح المتصفح على:
# http://localhost:7860
```

---

## 📖 الوثائق الكاملة

| الدليل | الوصف |
|--------|-------|
| [🚀 دليل البدء السريع](QUICK_START.md) | ابدأ استخدام التطبيق في دقائق |
| [☁️ دليل النشر](DEPLOYMENT_GUIDE.md) | انشر التطبيق على GitHub و Hugging Face |
| [🔧 حل المشاكل](TROUBLESHOOTING_AR.md) | حلول للمشاكل الشائعة |
| [📝 دليل المساهمين](CONTRIBUTING.md) | كيف تساهم في المشروع |
| [📋 قائمة التحقق من الإصدار](RELEASE_CHECKLIST.md) | Checklist للإصدارات الجديدة |
| [🤖 دليل تسليم AI](AI_HANDOFF_AR.md) | معلومات للذكاء الاصطناعي |

---

## 🎯 كيفية الاستخدام

### رفع ملف:
1. اضغط على تبويب "📁 رفع ملف"
2. اختر ملف صوتي من جهازك
3. اضغط "🚀 ابدأ فصل الملف"
4. انتظر اكتمال المعالجة
5. حمّل الملفات المفصولة (Vocals, Drums, Bass, Other)

### رابط URL:
1. اضغط على تبويب "🔗 رابط URL"
2. أدخل رابط مباشر لملف صوتي
3. اضغط "🚀 ابدأ معالجة الرابط"
4. حمّل النتيجة

### أدوات إضافية:
- **🛑 إلغاء العملية**: أوقف أي عملية جارية
- **🔄 التحقق من التحديثات**: تحقّق من وجود نسخة جديدة
- **🔍 تقرير التشخيص**: احصل على بيانات تقنية للمشاكل

---

## 🏗️ البنية التقنية

| المكون | التقنية |
|--------|---------|
| الواجهة | Gradio |
| محرك الفصل | HT-Demucs |
| السيرفر | Hugging Face Spaces (Docker) |
| اللغة | Python 3.10+ |

### هيكل المشروع:
```
vocal-remover-pro/
├── app_cloud.py              # التطبيق الرئيسي (Gradio)
├── requirements_cloud.txt    # المتطلبات
├── Dockerfile               # إعداد السيرفر السحابي
├── update_manifest.json     # ملف التحديثات
├── README.md                # هذا الملف
├── QUICK_START.md           # دليل البدء
├── DEPLOYMENT_GUIDE.md      # دليل النشر
├── .github/
│   ├── ISSUE_TEMPLATE/      # قوالب المشاكل
│   └── PULL_REQUEST_TEMPLATE.md
└── ... (ملفات أخرى)
```

---

## ⚙️ الإعدادات المتقدمة

### تحديث رابط Manifest:
في `app_cloud.py`، عدّل:
```python
MANIFEST_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/vocal-remover-pro/main/update_manifest.json"
```

### تخصيص النموذج:
لتغيير نموذج Demucs المستخدم، عدّل في `app_cloud.py`:
```python
model = get_model('htdemucs_ft')  # أو 'htdemucs', 'mdx_extra', etc.
```

---

## 🆘 الدعم

### المشاكل الشائعة:

| المشكلة | الحل |
|---------|------|
| العملية بطيئة | استخدم GPU Space (مدفوع) أو ملفات أصغر |
| زر الإلغاء لا يعمل | راجع [TROUBLESHOOTING_AR.md](TROUBLESHOOTING_AR.md) |
| لا يمكن رفع الملف | تحقّق من حجم الملف (< 100MB للنسخة المجانية) |

### الحصول على المساعدة:
1. اقرأ [دليل حل المشاكل](TROUBLESHOOTING_AR.md)
2. ابحث في [Issues الموجودة](https://github.com/YOUR_USERNAME/vocal-remover-pro/issues)
3. افتح [Issue جديد](https://github.com/YOUR_USERNAME/vocal-remover-pro/issues/new/choose)
4. اسأل في [Discussions](https://github.com/YOUR_USERNAME/vocal-remover-pro/discussions)

---

## 🤝 المساهمة

نرحب بالمساهمات! اقرأ [دليل المساهمين](CONTRIBUTING.md) للبدء.

### أنواع المساهمات المطلوبة:
- 🐛 إصلاح أخطاء
- ✨ ميزات جديدة
- 📚 تحسين التوثيق
- 🌐 ترجمة ل لغات أخرى
- 🧪 اختبار على أجهزة مختلفة

---

## 📜 الترخيص

MIT License - راجع ملف [LICENSE](LICENSE) للتفاصيل.

---

## 🙏 شكر خاص

- [Demucs](https://github.com/facebookresearch/demucs) من Facebook Research
- [Gradio](https://gradio.app/) للواجهة الرائعة
- [Hugging Face](https://huggingface.co/) للاستضافة السحابية

---

## 📬 تواصل

- **GitHub:** [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- **Hugging Face:** [YOUR_USERNAME](https://huggingface.co/YOUR_USERNAME)
- **Email:** your.email@example.com

---

<div align="center">

**⭐ إذا أعجبك المشروع، لا تنسَ تقييمه على GitHub! ⭐**

Made with ❤️ by YOUR_USERNAME

</div>

</div>
