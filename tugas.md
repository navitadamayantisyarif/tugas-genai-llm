Project: GenAI Apps

Materi: Generative AI, Large Language Models, Prompt Engineering, LLM API Integration with FastAPI

Instruksi

Buat sebuah aplikasi sederhana berbasis Generative AI menggunakan Python dan FastAPI.

Aplikasi yang dibuat tidak boleh hanya berupa chatbot biasa.

Kalian bebas menentukan sendiri use case yang ingin dibuat.

Beberapa contoh:

Meeting Notes Analyzer
Article Summarizer
CV Analyzer
Feedback Analyzer
Email Draft Generator
Learning Material Generator
Content Planner
Product Description Generator
atau ide lain yang menurut kalian menarik.

Requirement Project

Project minimal harus memiliki:

Python.
FastAPI.
Minimal 1 endpoint menggunakan method POST.
Menggunakan salah satu LLM API:
Groq
Gemini
OpenAI
atau provider LLM lainnya.
API Key disimpan menggunakan file .env.
File .env tidak boleh masuk ke repository GitHub.
Menggunakan Pydantic untuk request body.
Menggunakan System Prompt.
Prompt utama aplikasi minimal memiliki:
Task
Context
Constraint
Output Format
Response aplikasi harus berupa structured output / JSON sesuai dengan kebutuhan aplikasi kalian.
Structured output minimal memiliki 3 field.
Field structured output harus kalian tentukan sendiri berdasarkan use case aplikasi.
Memiliki error handling sederhana.
Memiliki requirements.txt.
Memiliki README.md.
Frontend bersifat opsional.
Contoh Sederhana

Misalnya kalian membuat:

Meeting Notes Analyzer

Request:

{
  "text": "Meeting hari ini membahas progress project..."
}


Contoh output:

{
  "summary": "...",
  "key_points": [],
  "action_items": []
}


Contoh di atas hanya contoh.

Kalian tidak wajib menggunakan field:

summary
key_points
action_items

Tentukan structured output yang sesuai dengan aplikasi kalian sendiri.

Tutorial Pengerjaan
1. Buat Project

Buat folder project:

mkdir tugas-genai-llm
cd tugas-genai-llm


Buat virtual environment:

python -m venv venv


Aktifkan virtual environment.

Windows:

venv\Scripts\activate


macOS / Linux:

source venv/bin/activate

2. Install Dependency

Jika menggunakan Groq:

pip install "fastapi[standard]" groq python-dotenv


Jika menggunakan Gemini / OpenAI / provider lainnya, install SDK sesuai provider yang kalian gunakan.

Setelah dependency terinstall:

pip freeze > requirements.txt

3. Buat .env

Contoh jika menggunakan Groq:

GROQ_API_KEY=your_api_key_here


Buat .gitignore:

.env
venv/
__pycache__/


Jangan upload API Key ke GitHub.

4. Buat FastAPI Dasar

Buat file:

main.py

Contoh:

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "GenAI API is running"
    }


Jalankan:

fastapi dev main.py


Buka:

http://127.0.0.1:8000/docs


Pastikan FastAPI berhasil berjalan.

5. Buat Request Body

Contoh:

from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    text: str


Contoh endpoint:

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    return {
        "text": request.text
    }


Test endpoint melalui:

http://127.0.0.1:8000/docs

6. Hubungkan ke LLM

Contoh jika menggunakan Groq:

from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()

client = AsyncGroq()


Contoh request ke model:

response = await client.chat.completions.create(
    model="openai/gpt-oss-120b",

    messages=[
        {
            "role": "system",
            "content": "You are an AI assistant."
        },
        {
            "role": "user",
            "content": request.text
        }
    ]
)


Mengambil hasil:

result = response.choices[0].message.content


Silakan sesuaikan model, SDK, dan provider berdasarkan provider LLM yang kalian pilih.

Prompt Engineering Experiment

Setelah aplikasi berhasil berjalan, lakukan eksperimen menggunakan input yang sama dengan tiga versi prompt.

Prompt A

Gunakan prompt sederhana.

Contoh:

Summarize this text.

Prompt B

Buat prompt yang memiliki:

Role
+
Task
+
Context

Prompt C

Buat prompt yang memiliki:

Role
+
Task
+
Context
+
Constraint
+
Output Format


Gunakan input yang sama pada ketiga prompt.

Jalankan semuanya menggunakan aplikasi kalian.

Simpan actual output dari masing-masing percobaan.

Actual output tersebut nantinya harus dimasukkan ke README.md.

Testing Tambahan

Setelah aplikasi selesai, coba aplikasi kalian menggunakan beberapa input yang berbeda.

Cari minimal 1 input yang menghasilkan output yang menurut kalian kurang baik, tidak sesuai expectation, atau masih memiliki kekurangan.

Catat:

Input:
...

Output:
...

Masalah:
...


Setelah itu:

ubah prompt; atau
ubah constraint; atau
ubah sebagian kode aplikasi.

Kemudian jalankan kembali input yang sama.

Catat output setelah diperbaiki.

README

Repository kalian wajib memiliki:

README.md

README tidak hanya digunakan untuk menjelaskan project, tetapi juga untuk mencatat hasil eksperimen dan refleksi dari proses pengerjaan kalian.

Gunakan struktur berikut.

GenAI Application
Project Information

Nama Project:

[ISI SENDIRI]

Use Case:

[ISI SENDIRI]

Deskripsi Singkat:

[ISI SENDIRI]

Tech Stack

Tuliskan teknologi yang digunakan.

[ISI SENDIRI]

Application Flow

Jelaskan menggunakan bahasa kalian sendiri bagaimana aplikasi bekerja dari:

User Input
↓
FastAPI
↓
LLM API
↓
Structured Output


Penjelasan kalian:

[ISI SENDIRI]

API Endpoint

Tuliskan endpoint utama aplikasi.

Contoh:

POST /analyze


Endpoint kalian:

[ISI SENDIRI]

Example Request

Masukkan salah satu request aktual yang digunakan ketika testing.

[ISI SENDIRI]

Example Response

Masukkan actual response dari aplikasi.

[ISI SENDIRI]

Structured Output

Tuliskan structured output/schema yang digunakan pada aplikasi.

[ISI SENDIRI]

Kenapa kalian memilih field-field tersebut?

Jelaskan berdasarkan fungsi aplikasi kalian.

[ISI SENDIRI]

Prompt Experiment

Gunakan input yang sama untuk Prompt A, Prompt B, dan Prompt C.

Input yang Digunakan

[ISI SENDIRI]

Prompt A

Tuliskan prompt yang digunakan.

[ISI SENDIRI]

Actual Output A

Masukkan actual output dari aplikasi.

[ISI SENDIRI]

Prompt B

Tuliskan prompt yang digunakan.

[ISI SENDIRI]

Actual Output B

Masukkan actual output dari aplikasi.

[ISI SENDIRI]

Prompt C

Tuliskan prompt yang digunakan.

[ISI SENDIRI]

Actual Output C

Masukkan actual output dari aplikasi.

[ISI SENDIRI]

Prompt Evaluation
Dari ketiga prompt tersebut, mana yang menurut kalian menghasilkan output paling baik?

[ISI SENDIRI]

Kenapa?

[ISI SENDIRI]

Apa perbedaan paling terlihat antara Prompt A, Prompt B, dan Prompt C berdasarkan hasil testing kalian?

[ISI SENDIRI]

Failure Case
Input yang menghasilkan output kurang baik

[ISI SENDIRI]

Actual Output

[ISI SENDIRI]

Menurut kalian apa masalah dari output tersebut?

[ISI SENDIRI]

Apa yang kalian ubah pada prompt / constraint / kode?

[ISI SENDIRI]

Output setelah diperbaiki

[ISI SENDIRI]

Personal Reflection

Jawab menggunakan pendapat dan pengalaman kalian sendiri selama mengerjakan project.

1. Menurut kalian, bagian apa yang paling sulit dari project ini?

[ISI SENDIRI]

2. Bagian kode mana yang paling banyak dibantu oleh AI?

[ISI SENDIRI]

3. Setelah melihat kode tersebut, jelaskan menggunakan bahasa kalian sendiri bagaimana bagian tersebut bekerja.

[ISI SENDIRI]

4. Menurut kalian, apa kekurangan terbesar dari aplikasi yang kalian buat jika digunakan oleh user sungguhan?

[ISI SENDIRI]

5. Jika provider LLM kalian diganti, misalnya dari Groq ke Gemini atau OpenAI, bagian mana dari project yang menurut kalian perlu diubah?

[ISI SENDIRI]

6. Setelah mencoba aplikasi kalian sendiri, apa satu improvement yang menurut kalian paling penting jika project ini dilanjutkan?

[ISI SENDIRI]

AI Usage
AI tools yang digunakan

[ISI SENDIRI]

AI digunakan untuk membantu bagian apa?

[ISI SENDIRI]

Bagian apa yang kalian tentukan, perbaiki, atau ubah sendiri setelah melihat hasil dari AI?

[ISI SENDIRI]

Pengumpulan

Project wajib dikumpulkan dalam bentuk repository GitHub.

1. Buat Repository GitHub

Nama repository:

tugas-genai-llm


Repository boleh:

Public; atau
Private selama mentor memiliki akses.
2. Push Project ke GitHub

Contoh jika repository baru:

git init
git add .
git commit -m "Initial submission Tugas GenAI Apps"
git branch -M main
git remote add origin https://github.com/USERNAME/tugas-genai-llm.git
git push -u origin main


Jika project kalian sudah memiliki Git repository dan hanya ingin mengganti remote:

git remote set-url origin https://github.com/USERNAME/tugas-genai-llm.git


Kemudian:

git add .
git commit -m "Submit Tugas GenAI Apps"
git push

3. Pastikan Repository Berisi

Minimal:

tugas-genai-llm/
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore


Struktur boleh berbeda atau lebih modular.

File .env tidak boleh ikut masuk repository.

4. Sebelum Mengumpulkan

Buka repository GitHub kalian melalui browser.

Pastikan:

Source code sudah masuk.
README.md dapat dibaca.
Semua bagian [ISI SENDIRI] sudah diisi.
Actual output Prompt A, B, dan C sudah ada.
Failure Case sudah ada.
Personal Reflection sudah dijawab.
requirements.txt tersedia.
.env tidak terlihat di repository.
Tidak ada API Key yang tercantum di source code atau README.
5. Yang Dikumpulkan

Kumpulkan LINK REPOSITORY GITHUB kalian di LMS.

Contoh:

https://github.com/arifian853/tugas-genai-llm


Jangan mengumpulkan:

file .zip;
screenshot project;
link Google Drive;
source code yang di-copy langsung ke LMS.

Yang dikumpulkan hanya:

Link Repository GitHub

Checklist

Sebelum submit, cek kembali:

 Project bisa dijalankan.
 FastAPI bisa dibuka melalui /docs.
 LLM API berhasil digunakan.
 Minimal terdapat 1 endpoint POST.
 API Key disimpan menggunakan .env.
 .env tidak masuk repository GitHub.
 Structured output memiliki minimal 3 field.
 Prompt A sudah diuji.
 Prompt B sudah diuji.
 Prompt C sudah diuji.
 Actual output ketiga prompt sudah dimasukkan ke README.
 Minimal 1 failure case ditemukan.
 Failure case sudah dicoba diperbaiki.
 Personal Reflection sudah dijawab.
 AI Usage sudah dijelaskan.
 requirements.txt tersedia.
 Project sudah di-push ke GitHub.
 Link repository GitHub sudah siap dikumpulkan.

Deadline:

Minggu, 1 November 2026, 23.59 WIB

Selamat mengerjakan!