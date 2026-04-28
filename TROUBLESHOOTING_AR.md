# Troubleshooting (Arabic)

## ffmpeg not found
- الحل: ثبت ffmpeg ثم افتح Terminal جديد.
- تحقق:
  - `ffmpeg -version`

## المعالجة بطيئة جدا
- فعّل `Auto optimize for this laptop`.
- قلل:
  - `Segment` إلى 4-6
  - `Shifts` إلى 1-2
- استخدم `Long file mode = Auto` أو `chunk`.

## الجهاز يسخن
- اغلق `All stems` إن لم تكن ضرورية.
- استخدم إعدادات خفيفة.
- اترك البرنامج يعمل cooling pauses (مفعّل تلقائيا).

## الملف كبير جدا وفشل
- جرّب تقسيم الملف.
- خفّض الجودة/الإعدادات.
- على CPU فقط: الملفات الطويلة جدا قد تحتاج وقت طويل جدا.

## الفيديو الناتج غير موجود
- تأكد اخترت:
  - `Result type = Video with cleaned vocals`
- وتأكد أن الملف المدخل فيديو وليس صوت فقط.

## فحص التحديث لا يعمل
- ضع رابط صحيح لـ `Update manifest URL`.
- جرب فتح الرابط في المتصفح للتأكد أنه JSON صالح.
