# 🚀 البدء السريع - Vocal Remover Pro

## خيار 1: التشغيل على Hugging Face Spaces (موصى به)

### للمطورين:
```bash
# 1. ارفع المشروع على GitHub
git push origin main

# 2. أنشئ Space جديد على Hugging Face
# اذهب إلى: https://huggingface.co/spaces/new
# اختر SDK: Docker
# اربط بمستودع GitHub

# 3. انتظر 5-10 دقائق للبناء
# الرابط سيكون: https://huggingface.co/spaces/YOUR_USERNAME/vocal-remover-pro
```

### للمستخدمين:
1. افتح رابط Space المنشور
2. ارفع ملف صوتي أو أدخل رابط URL
3. اضغط "ابدأ فصل الملف"
4. حمّل الملفات المفصولة

---

## خيار 2: التشغيل المحلي (للتطوير)

### المتطلبات:
- Python 3.8+
- 4GB RAM على الأقل
- اتصال إنترنت (لتحميل النموذج أول مرة)

### التثبيت:
```bash
cd /workspace
pip install -r requirements_cloud.txt
python app_cloud.py
```

### الاستخدام:
افتح المتصفح على: `http://localhost:7860`

---

## خيار 3: تطبيق Windows (قريباً)

1. نزّل ملف ZIP من GitHub Releases
2. فك الضغط
3. شغّل `VocalRemoverPro.exe`

---

## الأزرار الرئيسية في التطبيق:

| الزر | الوظيفة |
|------|---------|
| 🚀 ابدأ فصل الملف | يبدأ معالجة الملف المرفوع |
| 🛑 إلغاء العملية | يوقف أي عملية جارية |
| 🔄 التحقق من التحديثات | يتحقق من وجود نسخة جديدة |
| 🔍 تقرير التشخيص | يُنتج ملف JSON للمشاكل التقنية |

---

## نصائح سريعة:

✅ **لملفات قصيرة (< 5 دقائق):** استخدم مباشرة  
⚠️ **لملفات طويلة (> 10 دقائق):** قد تستغرق وقتاً طويلاً على CPU  
🛑 **للإلغاء:** اضغط زر الإلغاء في أي وقت  
📱 **للموبايل:** افتح رابط Space في متصفح الموبايل  

---

## روابط مهمة:

- **المستودع:** https://github.com/YOUR_USERNAME/vocal-remover-pro
- **التحديثات:** https://github.com/YOUR_USERNAME/vocal-remover-pro/releases
- **المشاكل:** https://github.com/YOUR_USERNAME/vocal-remover-pro/issues
- **Hugging Face:** https://huggingface.co/spaces/YOUR_USERNAME/vocal-remover-pro

---

**الإصدار:** 2.0.0 | **آخر تحديث:** 2024-01-15
