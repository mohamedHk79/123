from flask import Flask, request
import subprocess
import os
import uuid

app = Flask(__name__)
UNLUAC_PATH = "unluac_20201218.jar"  # الملف لازم يكون في نفس مجلد server.py

@app.route('/decompile', methods=['POST'])
def decompile():
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        return "No file uploaded", 400

    # حفظ ملف مؤقت
    temp_filename = f"/tmp/{uuid.uuid4().hex}.luac"
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.read())

    try:
        # تشغيل unluac.jar
        result = subprocess.run(
            ["java", "-jar", UNLUAC_PATH, temp_filename],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout  # بيرجع كود Lua
    except subprocess.CalledProcessError as e:
        return e.stderr, 500
    finally:
        os.remove(temp_filename)  # حذف الملف المؤقت بعد المعالجة

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
