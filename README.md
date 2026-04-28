# 🎵 Vocal Remover Pro - الإصدار السحابي

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Hugging Face Spaces](https://img.shields.io/badge/🤗-Hugging%20Face%20Spaces-blue)](https://huggingface.co/spaces)
[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/vocal-remover-pro?style=social)](https://github.com/YOUR_USERNAME/vocal-remover-pro/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/vocal-remover-pro?style=social)](https://github.com/YOUR_USERNAME/vocal-remover-pro/network/members)

<div align="center">

**افصل الأصوات عن الموسيقى بدقة عالية باستخدام الذكاء الاصطناعي!**

تطبيق متقدم لفصل المسارات الصوتية (Vocals, Drums, Bass, Other) يعمل على أي جهاز من خلال المتصفح.

 

</div>

---

## ✨ الميزات الرئيسية

| الميزة | الوصف |
|--------|-------|
| 🚀 **سحابي 100%** | لا حاجة لتثبيت أي شيء، افتح الرابط واستخدم مباشرة |
| 📱 **متجاوب تماماً** | يعمل على الموبايل، اللاب توب، والتابلت |
| 🛑 **إلغاء فوري** | أوقف أي عملية في أي وقت بضغطة زر |
| 🔄 **تحديثات تلقائية** | نظام ذكي للتحقق من النسخ الجديدة |
| 🔍 **تشخيص شامل** | تقرير JSON جاهز لحل المشاكل التقنية |
| 🎯 **دقة عالية** | يستخدم نموذج HT-Demucs الأحدث من Facebook Research |
| 🌐 **دعم الروابط** | ارفع ملفات أو أدخل روابط URL مباشرة |
| 📊 **شريط تقدم** | متابعة حية لحالة المعالجة |

---

## 🚀 الاستخدام السريع

### خيار 1: النسخة السحابية (موصى به للمستخدمين)

**لا يحتاج تثبيت! فقط اضغط وشغّل:**

1. **افتح التطبيق:**
   ```
   https://huggingface.co/spaces/YOUR_USERNAME/vocal-remover-pro
   ```

2. **ارفع ملفك** أو أدخل رابط URL

3. **اضغط "ابدأ فصل الملف"** وانتظر النتيجة

4. **حمّل الملفات المفصولة** (Vocals, Drums, Bass, Other)

### خيار 2: التشغيل المحلي (للمطورين)

```bash
# 1. استنساخ المشروع
git clone https://github.com/YOUR_USERNAME/vocal-remover-pro.git
cd vocal-remover-pro

# 2. تثبيت المتطلبات (يتطلب Python 3.8+)
pip install -r requirements_cloud.txt

# 3. تشغيل التطبيق
python app_cloud.py

# 4. افتح المتصفح
# http://localhost:7860
```

### خيار 3: نشر نسختك الخاصة على Hugging Face

```bash
# اتبع الخطوات في دليل النشر
# سيستغرق 5 دقائق فقط!
```

📖 **اقرأ:** [دليل النشر الكامل →](DEPLOYMENT_GUIDE.md)

---

## 📖 الوثائق الكاملة

| الدليل | الوصف | لمن هذا الدليل؟ |
|--------|-------|----------------|
| [🚀 دليل البدء السريع](QUICK_START.md) | ابدأ استخدام التطبيق في 3 دقائق | المستخدمين الجدد |
| [☁️ دليل النشر](DEPLOYMENT_GUIDE.md) | انشر التطبيق على GitHub و Hugging Face خطوة بخطوة | المطورين |
| [🔧 حل المشاكل](TROUBLESHOOTING_AR.md) | حلول مفصلة للمشاكل الشائعة | الجميع |
| [📝 دليل المساهمين](CONTRIBUTING.md) | كيف تساهم في المشروع | المساهمين المحتملين |
| [📋 قائمة التحقق من الإصدار](RELEASE_CHECKLIST.md) | Checklist احترافي للإصدارات | المُصيّنين |
| [🤖 دليل تسليم AI](AI_HANDOFF_AR.md) | معلومات تقنية للذكاء الاصطناعي | المطورين وAI bots |
| [📦 ملخص المشروع](PROJECT_SUMMARY.md) | نظرة عامة شاملة على المشروع | الجميع |

---

## 🎯 كيفية استخدام التطبيق

### 📁 رفع ملف صوتي

1. افتح التطبيق (سحابي أو محلي)
2. اختر تبويب **"📁 رفع ملف"**
3. اسحب وأفلت الملف أو اضغط للاختيار
4. اضغط **"🚀 ابدأ فصل الملف"**
5. تابع التقدم عبر شريط الحالة
6. عند الانتهاء، حمّل الملفات الأربع:
   - 🎤 **Vocals** (الأصوات)
   - 🥁 **Drums** (الطبول)
   - 🎸 **Bass** (الجيتار البيس)
   - 🎹 **Other** (باقي الآلات)

### 🔗 معالجة رابط URL

1. اختر تبويب **"🔗 رابط URL"**
2. الصق رابط مباشر لملف صوتي (MP3, WAV, FLAC, etc.)
3. اضغط **"🚀 ابدأ معالجة الرابط"**
4. حمّل النتيجة

### 🛠️ الأدوات الإضافية

| الزر | الوظيفة | متى تستخدمه؟ |
|------|---------|-------------|
| 🛑 **إلغاء العملية** | إيقاف فوري للمعالجة | إذا أردت إلغاء عملية جارية |
| 🔄 **التحقق من التحديثات** | فحص وجود نسخة جديدة | بشكل دوري لمعرفة آخر التحديثات |
| 🔍 **تقرير التشخيص** | استخراج بيانات تقنية | عند وجود مشكلة تحتاج دعم فني |

---

## 🏗️ البنية التقنية

### التقنيات المستخدمة

| المكون | التقنية | الإصدار |
|--------|---------|---------|
| الواجهة الأمامية | Gradio | 4.x |
| محرك الفصل | HT-Demucs | 4.0.1 |
| الاستضافة | Hugging Face Spaces | Docker |
| اللغة | Python | 3.10+ |
| الحاوية | Docker | Latest |

### هيكل المشروع

```
vocal-remover-pro/
├── 📄 app_cloud.py              # التطبيق الرئيسي (Gradio)
├── 📄 requirements_cloud.txt    # المكتبات المطلوبة
├── 🐳 Dockerfile                # إعداد السيرفر السحابي
├── 📄 update_manifest.json      # نظام التحديثات التلقائية
├── 📄 README.md                 # هذا الملف
│
├── 📚 الوثائق:
│   ├── QUICK_START.md           # دليل البدء السريع
│   ├── DEPLOYMENT_GUIDE.md      # دليل النشر التفصيلي
│   ├── TROUBLESHOOTING_AR.md    # حل المشاكل
│   ├── CONTRIBUTING.md          # دليل المساهمين
│   ├── RELEASE_CHECKLIST.md     # قائمة التحقق
│   ├── AI_HANDOFF_AR.md         # دليل تسليم AI
│   └── PROJECT_SUMMARY.md       # ملخص المشروع
│
├── ⚙️ ملفات GitHub:
│   └── .github/
│       ├── ISSUE_TEMPLATE/      # قوالب الإبلاغ
│       │   ├── bug_report.md
│       │   └── feature_request.md
│       ├── PULL_REQUEST_TEMPLATE.md
│       └── FUNDING.yml
│
└── 📂 ملفات إضافية:
    ├── run.py                   # مشغّل محلي
    ├── build.py                 # أداة البناء
    └── outputs/                 # مجلد المخرجات
```

---

## ⚙️ الإعدادات المتقدمة

### تخصيص رابط التحديثات

في `app_cloud.py`، عدّل السطر التالي:

```python
MANIFEST_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/vocal-remover-pro/main/update_manifest.json"
```

استبدل `YOUR_USERNAME` باسم المستخدم الخاص بك على GitHub.

### تغيير نموذج الذكاء الاصطناعي

لتغيير نموذج Demucs المستخدم (للتجربة أو تحسين الأداء):

```python
# في app_cloud.py، غيّر:
model = get_model('htdemucs')  # النموذج الافتراضي

# إلى أحد الخيارات التالية:
model = get_model('htdemucs_ft')    # Fine-tuned version
model = get_model('mdx_extra')      # جودة أعلى لكن أبطأ
model = get_model('repro')          # للأغراض البحثية
```

### ضبط موارد السيرفر

في `Dockerfile`، يمكنك تعديل:

```dockerfile
# لزيادة الذاكرة المخصصة (إذا كانت منصتك تدعم ذلك)
ENV PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
```

---

## 🆘 الدعم وحل المشاكل

### المشاكل الأكثر شيوعاً

| المشكلة | السبب المحتمل | الحل السريع |
|---------|--------------|-------------|
| ⏳ العملية بطيئة جداً | CPU فقط أو ملف كبير | استخدم GPU Space (مدفوع) أو قلّل حجم الملف |
| 🛑 زر الإلغاء لا يستجيب | قيد المعالجة الثقيلة | راجع [TROUBLESHOOTING_AR.md](TROUBLESHOOTING_AR.md) للحلول المتقدمة |
| 📁 فشل رفع الملف | حجم > 100MB (للنسخة المجانية) | استخدم ملف أصغر أو ترقي لمساحة مدفوعة |
| 🔗 رابط URL لا يعمل | الرابط غير مباشر أو محمي | استخدم رابط مباشر بدون حماية |
| 🔄 التحديثات لا تظهر | خطأ في رابط Manifest | تحقّق من صحة الرابط في `app_cloud.py` |

### الحصول على المساعدة

1. **اقرأ أولاً:** [دليل حل المشاكل الشاملة](TROUBLESHOOTING_AR.md)
2. **ابحث:** [في المشاكل الموجودة](https://github.com/YOUR_USERNAME/vocal-remover-pro/issues?q=is%3Aissue)
3. **اسأل المجتمع:** [في قسم النقاشات](https://github.com/YOUR_USERNAME/vocal-remover-pro/discussions)
4. **ابلغ عن مشكلة جديدة:** [افتح Issue جديد](https://github.com/YOUR_USERNAME/vocal-remover-pro/issues/new/choose)
5. **للطوارئ:** استخدم زر **"🔍 تقرير التشخيص"** في التطبيق وأرفقه مع البلاغ

### قالب الإبلاغ عن مشكلة

عند فتح Issue جديد، استخدم القالب الجاهز وسيتم تعبئته تلقائياً:

```markdown
### وصف المشكلة
اشرح المشكلة بالتفصيل...

### خطوات إعادة الإنتاج
1. افتح التطبيق...
2. اضغط على...
3. حدث الخطأ...

### البيئة
- الجهاز: [مثال: MacBook Pro M1]
- المتصفح: [مثال: Chrome 120]
- حجم الملف: [مثال: 45 MB]
- نوع الملف: [مثال: MP3 320kbps]

### تقرير التشخيص (اختياري)
[الصق مخرجات زر التشخيص هنا]
```

---

## 🤝 المساهمة في المشروع

نرحب بجميع أنواع المساهمات! 

### أنواع المساهمات المطلوبة

| النوع | أمثلة | الصعوبة |
|-------|-------|---------|
| 🐛 **إصلاح أخطاء** | إصلاح مشاكل في الواجهة أو المحرك | سهلة-متوسطة |
| ✨ **ميزات جديدة** | إضافة تأثيرات، صيغ جديدة، إلخ | متوسطة-صعبة |
| 📚 **تحسين التوثيق** | ترجمة، أمثلة إضافية، شروحات فيديو | سهلة |
| 🌐 **ترجمة** | إضافة لغات جديدة للواجهة والوثائق | سهلة |
| 🧪 **اختبار** | اختبار على أجهزة ومتصفحات مختلفة | سهلة |
| 🎨 **تحسين UI/UX** | تحسين التصميم وتجربة المستخدم | متوسطة |

### كيف تبدأ؟

1. اقرأ [دليل المساهمين الكامل](CONTRIBUTING.md)
2. ابحث عن [Issues مفتوحة](https://github.com/YOUR_USERNAME/vocal-remover-pro/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22) مناسبة للمبتدئين
3. Fork المشروع وأنشئ فرع جديد
4. قدّم Pull Request مع وصف واضح للتغييرات

---

## 📜 الترخيص

**MIT License** - حر ومفتوح المصدر

يمكنك:
- ✅ استخدام المشروع تجارياً
- ✅ تعديله وتوزيعه
- ✅ دمجها في مشاريعك

يجب:
- © ذكر المؤلف الأصلي
- 📄 تضمين نص الترخيص

📖 **اقرأ الترخيص الكامل:** [LICENSE](LICENSE)

---

## 🙏 شكر وتقدير

هذا المشروع مبني بفضل أدوات رائعة من المجتمع المفتوح المصدر:

| المشروع | الرابط | الشكر |
|---------|--------|-------|
| **Demucs** | [facebookresearch/demucs](https://github.com/facebookresearch/demucs) | محرك الفصل الصوتي الأروع |
| **Gradio** | [gradio.app](https://gradio.app/) | واجهة سهلة وقوية |
| **Hugging Face** | [huggingface.co](https://huggingface.co/) | استضافة سحابية مجانية |
| **PyTorch** | [pytorch.org](https://pytorch.org/) | إطار عمل الذكاء الاصطناعي |

---

## 📬 تواصل معنا

| المنصة | الرابط |
|--------|--------|
| **GitHub** | [@YOUR_USERNAME](https://github.com/YOUR_USERNAME) |
| **Hugging Face** | [YOUR_USERNAME](https://huggingface.co/YOUR_USERNAME) |
| **Email** | your.email@example.com |
| **Twitter** | @YOUR_USERNAME (اختياري) |
| **Discord** | [رابط السيرفر] (اختياري) |

---

## 📈 إحصائيات المشروع

<div align="center">

![GitHub Stars](https://img.shields.io/github/stars/YOUR_USERNAME/vocal-remover-pro?style=social)
![GitHub Forks](https://img.shields.io/github/forks/YOUR_USERNAME/vocal-remover-pro?style=social)
![GitHub Issues](https://img.shields.io/github/issues/YOUR_USERNAME/vocal-remover-pro)
![GitHub Pull Requests](https://img.shields.io/github/issues-pr/YOUR_USERNAME/vocal-remover-pro)
![GitHub Contributors](https://img.shields.io/github/contributors/YOUR_USERNAME/vocal-remover-pro)
![Last Commit](https://img.shields.io/github/last-commit/YOUR_USERNAME/vocal-remover-pro)
![License](https://img.shields.io/github/license/YOUR_USERNAME/vocal-remover-pro)

</div>



**شارك المشروع مع أصدقائك!**

[Share on Twitter](https://twitter.com/intent/tweet?text=Check%20out%20this%20amazing%20AI%20vocal%20remover!&url=https://github.com/YOUR_USERNAME/vocal-remover-pro)
[Share on Facebook](https://www.facebook.com/sharer/sharer.php?u=https://github.com/YOUR_USERNAME/vocal-remover-pro)
[Share on LinkedIn](https://www.linkedin.com/shareArticle?mini=true&url=https://github.com/YOUR_USERNAME/vocal-remover-pro)


</div>
