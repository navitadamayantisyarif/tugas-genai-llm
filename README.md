# GenAI Application

## Project Information

### Nama Project:
Meeting Notes & Action Items AI Analyzer

### Use Case:
Meeting Notes & Transcript Analyzer with Automated Action Item Extraction

### Deskripsi Singkat:
Aplikasi berbasis Generative AI yang dirancang untuk menganalisis catatan atau transkrip rapat yang tidak terstruktur (*unstructured meeting notes/transcripts*). Aplikasi ini memanfaatkan Large Language Model (LLM) melalui Groq API dan backend FastAPI untuk menghasilkan ringkasan eksekutif, poin-poin pembahasan utama, keputusan rapat yang disepakati, penugasan tindakan (*action items*) yang dilengkapi penanggung jawab (*assignee*), tenggat waktu (*deadline*), tingkat prioritas (*priority*), serta analisis nada suasana rapat (*meeting tone*).

---

## Tech Stack

Tuliskan teknologi yang digunakan.

- **Bahasa Pemrograman:** Python 3.10+
- **Backend Framework:** FastAPI (Asynchronous Web Framework)
- **Data Validation & Schemas:** Pydantic V2
- **LLM Provider:** Groq Cloud API
- **LLM Model:** `llama-3.3-70b-versatile` (dengan fallback/opsi `llama-3.1-8b-instant`)
- **Environment Management:** `python-dotenv`
- **Web Server:** Uvicorn ASGI Server
- **Frontend (Opsional/Dashboard):** HTML5, Vanilla Modern CSS (Dark Mode & Glassmorphism), Vanilla JavaScript
- **Testing:** Pytest & FastAPI TestClient

---

## Application Flow

Jelaskan menggunakan bahasa kalian sendiri bagaimana aplikasi bekerja dari:

```
User Input
↓
FastAPI
↓
LLM API
↓
Structured Output
```

### Penjelasan kalian:
1. **User Input:** Pengguna mengirimkan catatan atau transkrip percakapan rapat melalui Web Dashboard atau langsung ke endpoint API `POST /analyze`.
2. **FastAPI:** Request diterima dan divalidasi oleh FastAPI menggunakan Pydantic model (`AnalyzeRequest`) untuk memastikan kelayakan teks (minimal 10 karakter) dan opsi versi prompt yang dipilih.
3. **LLM API:** FastAPI menggabungkan `SYSTEM_PROMPT` dan template prompt terpilih lalu mengirimkannya secara asinkron (`AsyncGroq`) ke model `llama-3.3-70b-versatile` dengan parameter `response_format={"type": "json_object"}`.
4. **Structured Output:** Response mentah dari LLM dibersihkan oleh parser sanitizer regex, di-decode menjadi dictionary Python, dan divalidasi ke dalam model Pydantic (`AnalyzeResponse` & `ActionItem`) sehingga menghasilkan structured output JSON yang konsisten, bersih, dan siap ditampilkan di antarmuka web.

---

## API Endpoint

Tuliskan endpoint utama aplikasi.

Contoh:
POST /analyze

### Endpoint kalian:
- **`POST /analyze`** (Endpoint Utama Analisis Transkrip Rapat)
- **`GET /health`** (Health Check Status & Konfigurasi API Key)
- **`GET /docs`** (Interactive Swagger UI OpenAPI Documentation)
- **`GET /`** (Web Dashboard UI)

---

## Example Request

```json
{
  "text": "Meeting Sprint Planning Tim Tech - 31 Oktober 2026.\nPeserta: Budi (Backend Lead), Siti (QA), Dimas (Frontend), Rian (DevOps).\n\nAgenda pembahasan:\n1. Progress integrasi AI model menggunakan Groq dan FastAPI.\n2. Persiapan testing dan CI/CD deployment ke staging server.\n3. Diskusi database: Tim sepakat menggunakan PostgreSQL daripada MongoDB karena relasi data skema transkrip sudah jelas.\n\nHasil diskusi & penugasan:\n- Budi wajib menyelesaikan endpoint POST /analyze dengan structured JSON output paling lambat hari Selasa depan. Ini prioritas tinggi karena frontend membutuhkannya.\n- Siti bertugas menyusun skenario end-to-end testing untuk variasi prompt sebelum hari Rabu.\n- Dimas akan menyelesaikan dashboard UI responsif dengan dark mode dan menghubungkannya ke API setelah endpoint siap (deadline Kamis).\n- Rian sepakat menyiapkan container Docker dan GitHub Actions pipeline sebelum akhir minggu.\n\nCatatan suasana: Diskusi berjalan sangat produktif, terbuka, dan semua anggota tim memiliki target yang jelas.",
  "meeting_title": "Sprint Planning Tim Tech",
  "prompt_version": "C"
}
```

---

## Example Response

```json
{
  "meeting_title": "Sprint Planning Tim Tech",
  "summary": "Tim Engineering mengadakan Sprint Planning untuk membahas integrasi AI Groq dan FastAPI, persiapan pipeline CI/CD, serta migrasi arsitektur database. Disepakati penggunaan PostgreSQL sebagai database utama, dan seluruh PIC telah menerima pembagian tugas serta target penyelesaian minggu ini.",
  "key_points": [
    "Integrasi LLM Groq dengan FastAPI berjalan sesuai jadwal",
    "Keputusan arsitektur database beralih ke PostgreSQL karena kebutuhan relasional yang kuat",
    "Persiapan pengujian end-to-end testing untuk variasi prompt",
    "Otomasi deployment staging menggunakan Docker dan GitHub Actions"
  ],
  "decisions_made": [
    "Menggunakan PostgreSQL sebagai database utama menggantikan MongoDB"
  ],
  "action_items": [
    {
      "task": "Menyelesaikan endpoint POST /analyze dengan format structured JSON",
      "assignee": "Budi",
      "deadline": "Selasa depan",
      "priority": "High"
    },
    {
      "task": "Menyusun skenario end-to-end testing untuk variasi prompt",
      "assignee": "Siti",
      "deadline": "Rabu",
      "priority": "Medium"
    },
    {
      "task": "Menyelesaikan dashboard UI responsif dark mode dan integrasi API",
      "assignee": "Dimas",
      "deadline": "Kamis",
      "priority": "Medium"
    },
    {
      "task": "Menyiapkan container Docker dan GitHub Actions pipeline ke staging",
      "assignee": "Rian",
      "deadline": "Akhir minggu",
      "priority": "Medium"
    }
  ],
  "sentiment_tone": "Productive, Open, and Goal-Oriented",
  "prompt_version_used": "C",
  "model_used": "llama-3.3-70b-versatile"
}
```

---

## Structured Output

Tuliskan structured output/schema yang digunakan pada aplikasi.

Aplikasi ini mendefinisikan schema structured output dengan field-field berikut (diimplementasikan via Pydantic model `AnalyzeResponse` dan `ActionItem`):

```json
{
  "meeting_title": "string (Judul/topik rapat)",
  "summary": "string (Ringkasan eksekutif 2-3 kalimat)",
  "key_points": ["string (Daftar poin utama diskusi)"],
  "decisions_made": ["string (Daftar keputusan yang disepakati)"],
  "action_items": [
    {
      "task": "string (Deskripsi tindakan)",
      "assignee": "string (Penanggung jawab tugas)",
      "deadline": "string (Tenggat waktu)",
      "priority": "High | Medium | Low"
    }
  ],
  "sentiment_tone": "string (Analisis dinamika/suasana rapat)"
}
```

### Kenapa kalian memilih field-field tersebut?
Jelaskan berdasarkan fungsi aplikasi kalian.

Field-field ini dipilih secara spesifik berdasarkan kebutuhan nyata dalam manajemen proyek dan notulensi rapat profesional:
- **`summary` & `key_points`:** Para stakeholder atau manajer yang tidak hadir dalam rapat membutuhkan gambaran umum cepat tanpa harus membaca rekaman transkrip ratusan baris secara manual.
- **`decisions_made`:** Seringkali dalam rapat terjadi perdebatan panjang; memisahkan keputusan yang disepakati (*agreement*) dari sekadar opini mencegah kebingungan di kemudian hari.
- **`action_items` (task, assignee, deadline, priority):** Ini adalah *core value* dari notulensi rapat. Rapat tanpa pembagian PIC (*Person in Charge*), deadline, dan prioritas yang jelas akan berujung pada hilangnya akuntabilitas.
- **`sentiment_tone`:** Membantu Scrum Master atau pimpinan tim mendeteksi apakah suasana rapat sehat atau sedang berada dalam tekanan tinggi/banyak hambatan (*blockers*).

---

## Prompt Experiment

Gunakan input yang sama untuk Prompt A, Prompt B, dan Prompt C.

### Input yang Digunakan

```text
Meeting Sprint Planning Tim Tech - 31 Oktober 2026.
Peserta: Budi (Backend Lead), Siti (QA), Dimas (Frontend), Rian (DevOps).

Agenda pembahasan:
1. Progress integrasi AI model menggunakan Groq dan FastAPI.
2. Persiapan testing dan CI/CD deployment ke staging server.
3. Diskusi database: Tim sepakat menggunakan PostgreSQL daripada MongoDB karena relasi data skema transkrip sudah jelas.

Hasil diskusi & penugasan:
- Budi wajib menyelesaikan endpoint POST /analyze dengan structured JSON output paling lambat hari Selasa depan. Ini prioritas tinggi karena frontend membutuhkannya.
- Siti bertugas menyusun skenario end-to-end testing untuk variasi prompt sebelum hari Rabu.
- Dimas akan menyelesaikan dashboard UI responsif dengan dark mode dan menghubungkannya ke API setelah endpoint siap (deadline Kamis).
- Rian sepakat menyiapkan container Docker dan GitHub Actions pipeline sebelum akhir minggu.

Catatan suasana: Diskusi berjalan sangat produktif, terbuka, dan semua anggota tim memiliki target yang jelas.
```

---

### Prompt A

Tuliskan prompt yang digunakan.

```text
Summarize this meeting and extract action items:

{text}
```

### Actual Output A

Masukkan actual output dari aplikasi.

```text
Here is a summary of the meeting:

The tech team held a sprint planning session discussing Groq AI integration with FastAPI, CI/CD setup, and database selection where they chose PostgreSQL over MongoDB.

Action items:
- Budi needs to finish POST /analyze endpoint by Tuesday (high priority).
- Siti will write end-to-end test scenarios by Wednesday.
- Dimas will build the frontend dashboard by Thursday.
- Rian will setup Docker and GitHub Actions by end of week.

Tone: Productive and clear.
```

---

### Prompt B

Tuliskan prompt yang digunakan.

```text
Role: Senior Project Manager & Meeting Secretary
Task: Analyze the meeting transcript below, identify the main discussion topics, and extract key action items.
Context: This meeting took place within a fast-moving product and engineering team discussing project updates, technical blockers, and next steps.

Meeting Transcript:
{text}
```

### Actual Output B

Masukkan actual output dari aplikasi.

```text
As a Senior Project Manager, here is the structured analysis of the engineering sprint planning:

**Meeting Overview:**
The engineering team aligned on sprint priorities focusing on the Generative AI microservice architecture and release milestones.

**Key Discussion Topics:**
1. LLM Integration with FastAPI & Groq API.
2. Architecture Decision: Selected PostgreSQL due to explicit data relationships.
3. QA & Automated Deployment readiness.

**Action Items:**
1. Budi (Backend Lead): Complete POST /analyze endpoint with structured output (Deadline: Next Tuesday, Priority: High).
2. Siti (QA): Prepare E2E prompt variation test suites (Deadline: Wednesday).
3. Dimas (Frontend): Deliver responsive dark-mode dashboard (Deadline: Thursday).
4. Rian (DevOps): Provision Docker containerization and GitHub Actions CI/CD (Deadline: End of week).

Meeting Atmosphere: Highly productive and collaborative.
```

---

### Prompt C

Tuliskan prompt yang digunakan.

```text
Role: Lead Agile Scrum Master and Executive Technical Secretary

Task: Thoroughly analyze the unstructured meeting transcript below. Generate a concise executive summary, identify critical discussion points, document all formal decisions made, extract concrete prioritized action items, and evaluate the overall meeting tone.

Context: The team discussed project status, architecture decisions, resource assignments, and upcoming delivery deadlines. Some tasks might have explicit assignees while others are general.

Constraint:
1. Do not hallucinate or invent tasks, names, or decisions not present in the text.
2. Only extract formal engineering, product, or organizational tasks. Strictly ignore trivial daily chatter, casual remarks, jokes, or non-work domestic chores (e.g., buying snacks, coffee, lunch).
3. If task assignment is vague or mentions multiple alternative candidates (e.g. 'A or B'), set assignee strictly to 'Unassigned' and describe the ambiguity in the task description.
4. Deadline must be an estimated timeframe mentioned in text or 'TBD' if no clear deadline was established.
5. Priority must be strictly one of: 'High', 'Medium', or 'Low'.
6. Format output strictly as valid JSON matching the exact schema specified below.
7. Do NOT include markdown code blocks, backticks (```json), or conversational preface/postscript.

Output Format (Valid JSON):
{
  "meeting_title": "Descriptive title of the meeting",
  "summary": "2-3 sentences concise executive summary",
  "key_points": ["Point 1", "Point 2"],
  "decisions_made": ["Decision 1", "Decision 2"],
  "action_items": [
    {"task": "Action description", "assignee": "Name", "deadline": "Date/Time or TBD", "priority": "High|Medium|Low"}
  ],
  "sentiment_tone": "e.g., Productive & Decisive, Collaborative, or Tense & Urgent"
}

Meeting Transcript:
{text}
```

### Actual Output C

Masukkan actual output dari aplikasi.
```json
{
  "meeting_title": "Sprint Planning Tim Tech",
  "summary": "Tim Engineering mengadakan Sprint Planning untuk membahas integrasi AI Groq dan FastAPI, persiapan pipeline CI/CD, serta migrasi arsitektur database. Disepakati penggunaan PostgreSQL sebagai database utama, dan seluruh PIC telah menerima pembagian tugas serta target penyelesaian minggu ini.",
  "key_points": [
    "Integrasi LLM Groq dengan FastAPI berjalan sesuai jadwal",
    "Keputusan arsitektur database beralih ke PostgreSQL karena kebutuhan relasional yang kuat",
    "Persiapan pengujian end-to-end testing untuk variasi prompt",
    "Otomasi deployment staging menggunakan Docker dan GitHub Actions"
  ],
  "decisions_made": [
    "Menggunakan PostgreSQL sebagai database utama menggantikan MongoDB"
  ],
  "action_items": [
    {
      "task": "Menyelesaikan endpoint POST /analyze dengan format structured JSON",
      "assignee": "Budi",
      "deadline": "Selasa depan",
      "priority": "High"
    },
    {
      "task": "Menyusun skenario end-to-end testing untuk variasi prompt",
      "assignee": "Siti",
      "deadline": "Rabu",
      "priority": "Medium"
    },
    {
      "task": "Menyelesaikan dashboard UI responsif dark mode dan integrasi API",
      "assignee": "Dimas",
      "deadline": "Kamis",
      "priority": "Medium"
    },
    {
      "task": "Menyiapkan container Docker dan GitHub Actions pipeline ke staging",
      "assignee": "Rian",
      "deadline": "Akhir minggu",
      "priority": "Medium"
    }
  ],
  "sentiment_tone": "Productive, Open, and Goal-Oriented"
}
```

---

## Prompt Evaluation

### Dari ketiga prompt tersebut, mana yang menurut kalian menghasilkan output paling baik?
**Prompt C** adalah yang menghasilkan output paling optimal, konsisten, dan siap digunakan oleh aplikasi web maupun sistem produksi lainnya.

### Kenapa?
Karena Prompt C menerapkan prinsip Prompt Engineering secara komprehensif:
1. **Peran (*Role*) yang Spesifik:** Menempatkan LLM sebagai *Scrum Master & Technical Secretary* membuat gaya bahasa yang dihasilkan formal, objektif, dan relevan dengan lingkungan teknologi.
2. **Konteks & Batasan (*Constraint*):** Batasan tegas melarang halusinasi, membatasi enum nilai prioritas hanya ke `High|Medium|Low`, serta mencegah LLM menambahkan teks pembuka/penutup basa-basi (*conversational chatter*).
3. **Format Luaran (*Output Format*):** Memberikan skema JSON eksplisit dan instruksi zero-markdown membuat output 100% dapat di-parse oleh parser backend tanpa kegagalan decoding (*zero syntax errors*).

### Apa perbedaan paling terlihat antara Prompt A, Prompt B, dan Prompt C berdasarkan hasil testing kalian?
- **Prompt A:** Menghasilkan output berupa teks bebas percakapan (*free-form markdown*). Output ini tidak dapat langsung diproses oleh sistem software/frontend karena tidak memiliki struktur field yang konsisten.
- **Prompt B:** Kualitas analisis dan kategorisasi meningkat drastis berkat adanya *Role* dan *Context*, namun output masih berupa teks markdown dengan formatting tebal (*bold*) dan poin berpeluru (*bullets*), sehingga masih sulit di-parse secara deterministik.
- **Prompt C:** Menghasilkan data terstruktur murni (*pure JSON*) yang langsung cocok dengan model Pydantic, memisahkan secara jelas antara keputusan formal (*decisions_made*), ringkasan eksekutif, dan penugasan dengan metadata lengkap (*task, assignee, deadline, priority*).

---

## Failure Case

### Input yang menghasilkan output kurang baik

```text
Obrolan santai tim:
"Eh besok tolong siapa aja liat bug di login ya, kayaknya mas Budi atau Dimas sempet, tapi ntar deh liat situasi besok. Oh iya kopi di pantry abis, tolong siapa yang keluar beli ya."
```

### Actual Output

```json
{
  "meeting_title": "Obrolan Santai Tim",
  "summary": "Tim mendiskusikan bug login dan kebutuhan membeli kopi di pantry.",
  "key_points": [
    "Ada bug di login",
    "Kopi di pantry habis"
  ],
  "decisions_made": [],
  "action_items": [
    {
      "task": "Liat bug di login",
      "assignee": "Budi atau Dimas",
      "deadline": "ntar deh liat situasi besok",
      "priority": "High"
    },
    {
      "task": "Beli kopi di pantry",
      "assignee": "siapa yang keluar",
      "deadline": "TBD",
      "priority": "High"
    }
  ],
  "sentiment_tone": "Casual"
}
```

### Menurut kalian apa masalah dari output tersebut?
1. **Bercampurnya obrolan santai/non-proyek:** LLM memasukkan kegiatan non-relevan ("Beli kopi di pantry") sebagai *Action Item* resmi proyek dengan prioritas `High`.
2. **Assignee ambigu:** Nilai `assignee` diisi `"Budi atau Dimas"` dan `"siapa yang keluar"`, yang melanggar standar delegasi tugas dalam manajemen proyek.
3. **Deadline tidak terstandardisasi:** Deadline diisi kalimat percakapan informal mentah (`"ntar deh liat situasi besok"`).

### Apa yang kalian ubah pada prompt / constraint / kode?
Kami memperketat **Constraint** pada Prompt C dan menambahkan logika normalisasi di kode:
1. **Penambahan Constraint 1:** *"Only extract formal engineering, product, or organizational tasks. Strictly ignore trivial daily chatter, casual remarks, jokes, or non-work domestic chores (e.g., buying snacks, coffee, lunch)."*
2. **Penambahan Constraint 2:** *"If task assignment is vague or mentions multiple alternative candidates (e.g. 'A or B'), set assignee strictly to 'Unassigned' and describe the ambiguity in the task description."*
3. **Penambahan Constraint 3:** *"Deadline must be an estimated timeframe or 'TBD' if no clear deadline was established."*

### Output setelah diperbaiki

```json
{
  "meeting_title": "Diskusi Penanganan Isu Login",
  "summary": "Terdapat laporan mengenai bug pada modul login yang membutuhkan investigasi lebih lanjut oleh tim teknis tergantung ketersediaan resource esok hari.",
  "key_points": [
    "Identifikasi kebutuhan investigasi bug pada modul login"
  ],
  "decisions_made": [],
  "action_items": [
    {
      "task": "Investigasi dan pengecekan bug login (kandidat penanggung jawab Budi atau Dimas)",
      "assignee": "Unassigned",
      "deadline": "TBD",
      "priority": "Medium"
    }
  ],
  "sentiment_tone": "Casual & Exploratory"
}
```
*Hasil perbaikan:* Urusan membeli kopi dieliminasi, assignee tidak lagi ambigu, dan prioritas tidak berlebihan.

---

## Personal Reflection

Jawab menggunakan pendapat dan pengalaman kalian sendiri selama mengerjakan project.

### 1. Menurut kalian, bagian apa yang paling sulit dari project ini?
Bagian yang paling menantang adalah **memastikan konsistensi output JSON dari LLM**. Meskipun LLM modern sangat cerdas, model bahasa berbasis probabilistik terkadang menambahkan kata pengantar seperti *"Here is your JSON:"* atau membungkusnya dengan *markdown code fence* (````json ... ````). Memadukan parameter API (`response_format={"type": "json_object"}`), prompt engineering yang ketat pada *Constraint*, serta *fallback parser* menggunakan regex di Python membutuhkan pemikiran yang teliti agar sistem tidak pernah *crash* saat terjadi anomali output.

### 2. Bagian kode mana yang paling banyak dibantu oleh AI?
Pembuatan **skema Pydantic (`AnalyzeResponse`, `ActionItem`)** dan konfigurasi **dashboard UI modern (HTML, CSS Dark Mode, dan JavaScript)** adalah bagian yang paling banyak dibantu oleh AI. AI sangat cepat dalam menyusun template styling CSS modern dengan glassmorphism serta boilerplate validasi Pydantic.

### 3. Setelah melihat kode tersebut, jelaskan menggunakan bahasa kalian sendiri bagaimana bagian tersebut bekerja.
Fungsi `clean_json_response` dan endpoint `analyze_meeting` bekerja seperti filter berlapis:
1. Ketika LLM mengembalikan respon teks mentah, kode memeriksa apakah terdapat format markdown ````json ... ````. Jika ada, regex akan memotong teks tersebut dan hanya mengambil objek di antara kurung kurawal terluar `{ ... }`.
2. Teks yang bersih kemudian di-parse oleh `json.loads()`.
3. Setelah menjadi dictionary Python, data dimasukkan ke dalam model Pydantic `AnalyzeResponse`. Di sini, Pydantic bertindak sebagai satpam: ia memverifikasi apakah setiap field memiliki tipe data yang sesuai (misal `key_points` adalah list of string). Jika ada field yang kosong, nilai default yang telah disiapkan akan otomatis terisi.

### 4. Menurut kalian, apa kekurangan terbesar dari aplikasi yang kalian buat jika digunakan oleh user sungguhan?
Kekurangan terbesar saat ini adalah **keterbatasan input hanya melalui teks manual**. Dalam skenario rapat dunia nyata, pengguna biasanya memiliki file rekaman audio (seperti MP3/WAV dari Zoom atau Google Meet) atau dokumen transkrip panjang berformat PDF/DOCX. Jika aplikasi ini digunakan pengguna sungguhan, mereka masih harus menyalin teks secara manual dan berpotensi terbentur batasan panjang konteks (*context window* atau *rate limit*) jika transkrip rapat berlangsung hingga berjam-jam.

### 5. Jika provider LLM kalian diganti, misalnya dari Groq ke Gemini atau OpenAI, bagian mana dari project yang menurut kalian perlu diubah?
Bagian yang perlu diubah cukup terisolasi dan modular:
1. **File `.env`:** Mengganti `GROQ_API_KEY` menjadi `GEMINI_API_KEY` atau `OPENAI_API_KEY`, serta variabel nama model.
2. **Inisialisasi Client di `main.py`:** Mengganti fungsi `get_groq_client()` dan import library dari `groq.AsyncGroq` menjadi `google.genai` (atau `openai.AsyncOpenAI`).
3. **Pemanggilan API Method:** Mengubah baris `await client.chat.completions.create(...)` menjadi metode pemanggilan SDK target (misalnya `await client.models.generate_content(...)` untuk Gemini).
4. Struktur model Pydantic, route FastAPI, prompt templates, dan tampilan frontend tidak perlu diubah sama sekali.

### 6. Setelah mencoba aplikasi kalian sendiri, apa satu improvement yang menurut kalian paling penting jika project ini dilanjutkan?
Fitur paling esensial untuk dikembangkan berikutnya adalah **integrasi otomatis ke Project Management Tools (seperti Trello, Jira, Notion, atau GitHub Issues)**. Saat ini, setelah *action items* diekstraksi, pengguna masih harus memindahkannya manual. Jika ada tombol *"Export to Jira / Trello"* di mana setiap *action item* langsung menjadi tiket kerja berdasar PIC-nya, aplikasi ini akan menjadi alat produktivitas yang sangat bernilai tinggi bagi tim kerja.

---

## AI Usage

### AI tools yang digunakan
- Antigravity AI Pair Programmer
- Groq Cloud LLM Inference Engine (`llama-3.3-70b-versatile`)

### AI digunakan untuk membantu bagian apa?
1. Merancang arsitektur awal integrasi FastAPI asinkron dengan Groq SDK.
2. Menyusun template HTML/CSS/JS untuk visualisasi web dashboard interaktif.
3. Menulis skenario pengujian unit test menggunakan Pytest dan `FastAPI TestClient`.
4. Merumuskan struktur prompt eksperimen (A, B, dan C) sesuai pedoman Prompt Engineering standar industri.

### Bagian apa yang kalian tentukan, perbaiki, atau ubah sendiri setelah melihat hasil dari AI?
1. **Memperbaiki format string template:** Menemukan dan memperbaiki *bug* format string Python di mana penggunaan kurung kurawal `{ ... }` pada contoh JSON skema di Prompt C menyebabkan benturan (*KeyError*) jika dipanggil dengan `.format()`, lalu mengubahnya menjadi metode `.replace("{text}", request.text)`.
2. **Penyempurnaan Constraint Prompt C:** Menambahkan aturan ketat penanganan kasus kegagalan (*failure case*) untuk mengabaikan topik informal (seperti membeli kopi/makanan ringan) dan memetakan penugasan ambigu menjadi `"Unassigned"`.
3. **Penyempurnaan Error Handling:** Menambahkan penanganan spesifik untuk exception Groq seperti `AuthenticationError`, `RateLimitError`, dan `APIConnectionError` agar pengguna mendapatkan pesan error yang ramah dalam bahasa Indonesia, bukan pesan stack trace mentah.

---

## Petunjuk Menjalankan Project

### 1. Prasyarat
- Python 3.10 atau versi lebih baru
- Groq API Key (Dapat diperoleh gratis di [console.groq.com/keys](https://console.groq.com/keys))

### 2. Setup Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependensi
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Environment Variable
Salin `.env.example` menjadi `.env` lalu masukkan Groq API Key Anda:
```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```
Buka file `.env` dan masukkan API Key:
```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### 5. Menjalankan Aplikasi
```bash
fastapi dev main.py
# atau menggunakan uvicorn:
uvicorn main:app --reload --port 8000
```

Buka di browser:
- **Web Dashboard:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 6. Menjalankan Unit Test
```bash
pytest -v
```
