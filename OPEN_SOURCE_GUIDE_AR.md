# Open Source + Sync Upgrade Guide

## الهدف

تقدر تنشر المشروع Open Source بحيث:
- أي شخص يقدر يقرأ الكود ويعدّل.
- يحصل نظام تحديثات واضح (manifest + releases).
- المستخدم النهائي يقدر يعرف إذا فيه إصدار أحدث.

## 1) ارفع المشروع على GitHub

1. أنشئ Repository جديد (مثلا: `vocal-remover-pro`)
2. ارفع ملفات المشروع
3. فعّل Issues وDiscussions

## 2) إدارة الإصدارات

- غيّر الإصدار في `backend/version.py` عند كل Release.
- ارفع ملف التوزيع النهائي `VocalRemoverPro_Windows.zip` ضمن Release.

## 3) ملف تحديثات موحّد (manifest)

- استخدم `update_manifest.sample.json` كنموذج.
- ارفعه على رابط ثابت (GitHub Pages أو Raw URL).
- في إعدادات التطبيق، ضع الرابط داخل:
  - `Update manifest URL`

مثال URL:
`https://raw.githubusercontent.com/<user>/<repo>/main/update_manifest.json`

## 4) كيف يعمل التحديث في التطبيق

- التطبيق يفحص `/api/update/check`.
- السيرفر يقرأ `update_manifest_url`.
- إذا وجد إصدار أحدث، يظهر تنبيه في الواجهة مع رابط التحميل.

## 5) تحسين التعاون بين المطورين

- استخدم Pull Requests قبل الدمج.
- اكتب changelog واضح لكل نسخة.
- افتح Issue Templates للأعطال والميزات.

## 6) لو عايز AI Bot يساعد

- شارك ملف diagnostics الناتج من زر `Download diagnostics`.
- افتح Issue وارفِق:
  - ملف diagnostics
  - خطوات إعادة المشكلة
  - صورة الشاشة أو log

هذا يجعل أي AI assistant أو مطور يفهم المشكلة ويحاول حلها بسرعة.
