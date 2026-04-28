# دليل النشر الكامل - Vocal Remover Pro

## 📋 نظرة عامة
هذا الدليل يشرح خطوة بخطوة كيفية نشر التطبيق على GitHub و Hugging Face Spaces.

---

## 🚀 الجزء 1: إعداد GitHub

### الخطوة 1: إنشاء مستودع جديد
1. اذهب إلى [GitHub.com](https://github.com)
2. اضغط على **+** → **New repository**
3. اسم المستودع: `vocal-remover-pro`
4. اجعله **Public**
5. اضغط **Create repository**

### الخطوة 2: رفع الملفات
```bash
cd /workspace
git init
git add .
git commit -m "Initial commit: Cloud-ready vocal remover with cancel support"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/vocal-remover-pro.git
git push -u origin main
```

### الخطوة 3: إنشاء Release
1. اذهب إلى **Releases** → **Create a new release**
2. Tag version: `v2.0.0`
3. Release title: `Vocal Remover Pro v2.0.0`
4. وصف الإصدار:
   ```
   ## التغييرات الجديدة:
   - ✅ دعم Hugging Face Spaces
   - ✅ زر إلغاء العمليات
   - ✅ نظام تحديثات تلقائي
   - ✅ تقرير تشخيصي مدمج
   - ✅ دعم رفع الملفات وروابط URL
   ```
5. ارفع ملف ZIP (اختياري لمستخدمي Windows)
6. اضغط **Publish release**

### الخطوة 4: تحديث manifest
عدّل رابط التحميل في `update_manifest.json`:
```json
{
  "download_url": "https://github.com/YOUR_USERNAME/vocal-remover-pro/releases/download/v2.0.0/VocalRemoverPro_Windows.zip"
}
```

---

## ☁️ الجزء 2: النشر على Hugging Face Spaces

### الخطوة 1: إنشاء Space جديد
1. اذهب إلى [Hugging Face Spaces](https://huggingface.co/spaces)
2. اضغط **Create new Space**
3. اختر:
   - **Space name:** `vocal-remover-pro`
   - **License:** MIT
   - **SDK:** Docker
   - **Visibility:** Public

### الخطوة 2: ربط GitHub
1. في صفحة Space الجديدة، اذهب إلى **Settings**
2. تحت **Repository**، اضغط **Connect to GitHub**
3. اختر المستودع `YOUR_USERNAME/vocal-remover-pro`
4. سيتم البناء والنشر تلقائياً!

### الخطوة 3: الانتظار
- أول بناء قد يستغرق 5-10 دقائق
- ستظهر حالة البناء في تبويب **Logs**
- عند الانتهاء، ستحصل على رابط مثل:
  ```
  https://huggingface.co/spaces/YOUR_USERNAME/vocal-remover-pro
  ```

---

## 🔧 الجزء 3: التكوين النهائي

### تحديث الروابط
في الملفات التالية، استبدل `YOUR_USERNAME` و `YOUR_REPO`:

1. **app_cloud.py**:
   ```python
   MANIFEST_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/vocal-remover-pro/main/update_manifest.json"
   ```

2. **update_manifest.json**:
   ```json
   "download_url": "https://github.com/YOUR_USERNAME/vocal-remover-pro/releases/download/v2.0.0/VocalRemoverPro_Windows.zip"
   ```

3. **AI_HANDOFF_AR.md**: حدّث الروابط في قسم "روابط مهمة"

### دفع التحديثات
```bash
git add .
git commit -m "Update deployment configuration"
git push
```

---

## ✅ التحقق من النجاح

### قائمة التحقق:
- [ ] المستودع على GitHub موجود وملفاتُه مرفوعة
- [ ] Space على Hugging Face يعمل
- [ ] الرابط يُظهر واجهة Gradio
- [ ] زر رفع الملف يعمل
- [ ] زر الإلغاء موجود
- [ ] زر التحقق من التحديثات يعمل
- [ ] تقرير التشخيص يُنتج JSON صحيح

### اختبار سريع:
1. افتح رابط Space
2. ارفع ملف صوتي قصير (10 ثوانٍ)
3. اضغط "ابدأ فصل الملف"
4. انتظر اكتمال المعالجة
5. حمّل الملفات المفصولة
6. جرّب زر الإلغاء أثناء العملية

---

## 🔄 الجزء 4: الصيانة والتحديثات

### عند إصدار نسخة جديدة:

1. **عدّل الإصدار**:
   - `app_cloud.py`: غيّر `VERSION = "2.0.1"`
   - `update_manifest.json`: حدّث version و release_date

2. **أنشئ Release جديد** على GitHub

3. **ادفع التحديثات**:
   ```bash
   git add .
   git commit -m "Release v2.0.1: bug fixes and improvements"
   git push
   ```

4. **انتظر البناء التلقائي** على Hugging Face (5-10 دقائق)

---

## 🆘 حل المشاكل الشائعة

| المشكلة | الحل |
|---------|------|
| البناء يفشل على HF | تحقّق من `Dockerfile` و `requirements_cloud.txt` |
| النموذج لا يحمل | تأكد من وجود اتصال إنترنت في Space |
| الواجهة لا تظهر | راجع logs في تبويب Settings → Logs |
| الملفات الكبيرة تفشل | استخدم GPU Space (مدفوع) أو قسّم الملف |

---

## 📞 الدعم

- للمشاكل التقنية: افتح **Issue** على GitHub
- للاستفسارات: استخدم تبويب **Discussions**
- للتقارير الأمنية: راسل صاحب المستودع مباشرة

---

**آخر تحديث:** 2024-01-15  
**الإصدار:** 2.0.0
