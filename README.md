# دليل الاستخدام السريع

## 1. التشغيل المحلي (على جهازك)

### المتطلبات:
- Python 3.8 أو أحدث

### الخطوات:
1. حمل الملفات من هذا المستودع
2. افتح التيرمينال وثبت المكتبات:
   ```bash
   pip install -r requirements.txt
   ```
3. شغل البرنامج:
   ```bash
   python run.py
   ```
4. افتح المتصفح على: `http://localhost:7860`

---

## 2. الرفع على Hugging Face Spaces

### الخطوات:
1. سجل دخولك على [huggingface.co](https://huggingface.co)
2. اذهب إلى **Spaces** → **Create new Space**
3. اختر:
   - **Space type**: Gradio
   - **Python version**: 3.10
4. ارفع الملفات التالية فقط:
   - `run.py`
   - `app_cloud.py`
   - `backend/main.py`
   - `backend/engine.py`
   - `frontend/index.html`
   - `requirements.txt`
   - `.gitignore`
   - `README.md` (هذا الملف)

5. بعد الرفع، هيفضل يعمل أوتوماتيك

### ملاحظات مهمة:
- تأكد أن ملف `requirements.txt` فيه كل المكتبات المطلوبة
- لو حجم الموديل كبير، استخدم **Git LFS**:
  ```bash
  git lfs install
  git lfs track "*.bin"
  git lfs track "*.safetensors"
  ```

---

## الملفات الموجودة في المشروع

| الملف | الوظيفة |
|------|---------|
| `run.py` | نقطة البداية للتشغيل المحلي |
| `app_cloud.py` | نسخة معدلة للتشغيل على Hugging Face |
| `backend/main.py` | المنطق الرئيسي للبرنامج |
| `backend/engine.py` | محرك المعالجة |
| `frontend/index.html` | واجهة المستخدم |
| `requirements.txt` | المكتبات المطلوبة |

---

## حل المشاكل الشائعة

**المشكلة**: خطأ في تثبيت المكتبات  
**الحل**: تأكد من تحديث pip أولاً:
```bash
pip install --upgrade pip
```

**المشكلة**: البرنامج مش بيفتح على Hugging Face  
**الحل**: تأكد أن `app_cloud.py` موجود ومكتوب فيه `gradio` كواجهة
