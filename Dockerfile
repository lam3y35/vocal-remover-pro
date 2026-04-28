FROM python:3.10-slim

WORKDIR /app

# تثبيت المتطلبات النظامية و ffmpeg
RUN apt-get update && apt-get install -y ffmpeg git curl && rm -rf /var/lib/apt/lists/*

# نسخ ملفات المتطلبات
COPY requirements_cloud.txt .
RUN pip install --no-cache-dir -r requirements_cloud.txt

# نسخ كود التطبيق
COPY app_cloud.py .

# إنشاء مجلد مؤقت للملفات
RUN mkdir -p /tmp/audio_outputs

# منفذ التشغيل
EXPOSE 7860

# متغيرات البيئة
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT="7860"

# أمر التشغيل
CMD ["python", "app_cloud.py"]
