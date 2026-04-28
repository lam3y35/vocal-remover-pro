# AI Handoff Guide

استخدم هذا القالب عندما تريد من AI Bot تحليل مشكلة:

## 1) المعلومات المطلوبة
- وصف المشكلة باختصار
- خطوات إعادة المشكلة
- الملف الناتج من `Download diagnostics`
- لقطة شاشة من الواجهة

## 2) Prompt جاهز

```
Analyze this Vocal Remover Pro issue.
I attached diagnostics JSON + screenshot.
Please identify root cause, suggest the minimal safe fix, and provide exact file-level patch plan.
Prioritize CPU stability and long-file behavior.
```

## 3) نصيحة
- لا تطلب من AI تغيير كل شيء مرة واحدة.
- اطلب إصلاح واحد واضح ثم اختبر.
