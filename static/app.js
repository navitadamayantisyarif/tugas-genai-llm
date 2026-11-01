// Meeting samples for instant testing
const SAMPLES = {
  sample1: {
    title: "Sprint Planning & API Integration",
    text: `Meeting Sprint Planning Tim Engineering - 31 Oktober 2026.
Peserta: Budi (Backend Lead), Siti (QA), Dimas (Frontend), Rian (DevOps).

Agenda pembahasan:
1. Progress integrasi AI model menggunakan Groq dan FastAPI.
2. Persiapan testing dan CI/CD deployment ke staging.
3. Diskusi database: Tim sepakat menggunakan PostgreSQL daripada MongoDB karena relasi data skema transkrip sudah jelas.

Hasil diskusi & penugasan:
- Budi wajib menyelesaikan endpoint POST /analyze dengan structured JSON output paling lambat hari Selasa depan. Ini prioritas tinggi karena frontend membutuhkannya.
- Siti bertugas menyusun skenario end-to-end testing untuk variasi prompt sebelum hari Rabu.
- Dimas akan menyelesaikan dashboard UI responsif dengan dark mode dan menghubungkannya ke API setelah endpoint siap (deadline Kamis).
- Rian sepakat menyiapkan container Docker dan GitHub Actions pipeline sebelum akhir minggu.

Catatan suasana: Diskusi berjalan sangat produktif, terbuka, dan semua anggota tim memiliki target yang jelas.`
  },
  sample2: {
    title: "Client Pitch & Product Roadmap Meeting",
    text: `Catatan Rapat Penyelarasan Roadmap Produk bersama Klien PT Maju Digital.
Tanggal: 28 Oktober 2026.
Hadir: Pak Gunawan (Klien), Amanda (Product Lead), Kevin (Tech Architect).

Inti Pembahasan:
- Klien mengapresiasi prototipe awal sistem ekstraksi dokumen rapat otomatis.
- Namun klien meminta waktu respon latency LLM ditekan di bawah 2 detik agar usable saat live conference.
- Amanda menyetujui penambahan fitur ekspor hasil ke format PDF dan Excel.

Keputusan:
- Fitur multi-language (Indonesia, Inggris, Mandarin) disepakati masuk ke rilis Fase 2 bulan depan.
- Prioritas Fase 1 difokuskan pada kecepatan inferensi dan akurasi ekstraksi action item.

Tindak lanjut:
- Kevin akan melakukan benchmarking latency antara Groq Llama-3.3 dan model alternatif sebelum hari Jumat (High priority).
- Amanda membuat dokumen user journey untuk fitur export PDF sebelum hari Selasa.
- Tim klien (Pak Gunawan) akan mengirimkan 20 sampel transkrip nyata untuk validasi model sebelum 5 November.`
  }
};

let currentResponseData = null;

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("analyzer-form");
  const meetingTitleInput = document.getElementById("meeting-title");
  const meetingTextInput = document.getElementById("meeting-text");
  const charNum = document.getElementById("char-num");
  const submitBtn = document.getElementById("submit-btn");
  const btnText = submitBtn.querySelector(".btn-text");
  const btnLoader = submitBtn.querySelector(".btn-loader");
  const errorBanner = document.getElementById("error-message");

  const sample1Btn = document.getElementById("sample1-btn");
  const sample2Btn = document.getElementById("sample2-btn");

  const emptyState = document.getElementById("empty-state");
  const resultsContent = document.getElementById("results-content");
  const headerTools = document.getElementById("header-tools");
  const copyJsonBtn = document.getElementById("copy-json-btn");
  const toggleJsonBtn = document.getElementById("toggle-json-btn");
  const rawJsonContainer = document.getElementById("raw-json-container");
  const rawJsonCode = document.getElementById("raw-json-code");

  // Character counter
  meetingTextInput.addEventListener("input", () => {
    charNum.textContent = meetingTextInput.value.length;
  });

  // Prompt Version selection styles
  const promptOptions = document.querySelectorAll(".prompt-option");
  promptOptions.forEach((opt) => {
    opt.addEventListener("click", () => {
      promptOptions.forEach((o) => o.classList.remove("active"));
      opt.classList.add("active");
      const radio = opt.querySelector('input[type="radio"]');
      if (radio) radio.checked = true;
    });
  });

  // Load Samples
  sample1Btn.addEventListener("click", () => {
    meetingTitleInput.value = SAMPLES.sample1.title;
    meetingTextInput.value = SAMPLES.sample1.text;
    charNum.textContent = meetingTextInput.value.length;
    meetingTextInput.focus();
  });

  sample2Btn.addEventListener("click", () => {
    meetingTitleInput.value = SAMPLES.sample2.title;
    meetingTextInput.value = SAMPLES.sample2.text;
    charNum.textContent = meetingTextInput.value.length;
    meetingTextInput.focus();
  });

  // Form Submit
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorBanner.style.display = "none";

    const text = meetingTextInput.value.trim();
    if (!text || text.length < 10) {
      showError("Transkrip rapat harus diisi minimal 10 karakter.");
      return;
    }

    const meetingTitle = meetingTitleInput.value.trim() || undefined;
    const selectedVersionRadio = document.querySelector('input[name="prompt_version"]:checked');
    const promptVersion = selectedVersionRadio ? selectedVersionRadio.value : "C";

    // Set loading state
    submitBtn.disabled = true;
    btnText.style.display = "none";
    btnLoader.style.display = "inline-flex";

    try {
      const response = await fetch("/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: text,
          meeting_title: meetingTitle,
          prompt_version: promptVersion,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || `Server error (${response.status})`);
      }

      currentResponseData = data;
      renderResults(data);
    } catch (err) {
      showError(err.message || "Gagal menghubungi server backend.");
    } finally {
      submitBtn.disabled = false;
      btnText.style.display = "inline-flex";
      btnLoader.style.display = "none";
    }
  });

  function showError(msg) {
    errorBanner.textContent = msg;
    errorBanner.style.display = "block";
  }

  function renderResults(data) {
    emptyState.style.display = "none";
    resultsContent.style.display = "block";
    headerTools.style.display = "flex";

    // Fill metadata
    document.getElementById("res-title").textContent = data.meeting_title || "Meeting Analysis";
    document.getElementById("res-prompt-ver").textContent = data.prompt_version_used || "C";
    document.getElementById("res-model").textContent = data.model_used || "Llama-3.3";
    document.getElementById("res-tone").textContent = data.sentiment_tone || "Productive";

    // Summary
    document.getElementById("res-summary").textContent = data.summary || "Tidak ada ringkasan.";

    // Key points
    const kpContainer = document.getElementById("res-key-points");
    kpContainer.innerHTML = "";
    if (data.key_points && data.key_points.length > 0) {
      data.key_points.forEach((kp) => {
        const li = document.createElement("li");
        li.textContent = kp;
        kpContainer.appendChild(li);
      });
    } else {
      kpContainer.innerHTML = "<li>Tidak ada poin khusus.</li>";
    }

    // Decisions
    const decContainer = document.getElementById("res-decisions");
    decContainer.innerHTML = "";
    if (data.decisions_made && data.decisions_made.length > 0) {
      data.decisions_made.forEach((dec) => {
        const li = document.createElement("li");
        li.textContent = dec;
        decContainer.appendChild(li);
      });
    } else {
      decContainer.innerHTML = "<li>Tidak ada keputusan formal yang dicatat.</li>";
    }

    // Action items
    const actContainer = document.getElementById("res-action-items");
    actContainer.innerHTML = "";
    if (data.action_items && data.action_items.length > 0) {
      data.action_items.forEach((item) => {
        const tr = document.createElement("tr");

        const priorityClass = (item.priority || "Medium").toLowerCase() === "high"
          ? "priority-high"
          : (item.priority || "Medium").toLowerCase() === "low"
            ? "priority-low"
            : "priority-medium";

        tr.innerHTML = `
          <td><strong>${escapeHtml(item.task)}</strong></td>
          <td><span class="assignee-badge">${escapeHtml(item.assignee || "Team")}</span></td>
          <td>${escapeHtml(item.deadline || "TBD")}</td>
          <td><span class="priority-badge ${priorityClass}">${escapeHtml(item.priority || "Medium")}</span></td>
        `;
        actContainer.appendChild(tr);
      });
    } else {
      actContainer.innerHTML = `<tr><td colspan="4" style="text-align: center; color: var(--text-dim);">Tidak ada action item teridentifikasi.</td></tr>`;
    }

    // Raw JSON view
    rawJsonCode.textContent = JSON.stringify(data, null, 2);
  }

  // Toggle raw JSON view
  toggleJsonBtn.addEventListener("click", () => {
    if (rawJsonContainer.style.display === "none") {
      rawJsonContainer.style.display = "block";
      toggleJsonBtn.textContent = "Sembunyikan JSON";
    } else {
      rawJsonContainer.style.display = "none";
      toggleJsonBtn.textContent = "Lihat JSON";
    }
  });

  // Copy JSON
  copyJsonBtn.addEventListener("click", async () => {
    if (!currentResponseData) return;
    try {
      await navigator.clipboard.writeText(JSON.stringify(currentResponseData, null, 2));
      const originalText = copyJsonBtn.innerHTML;
      copyJsonBtn.textContent = "Tersalin!";
      setTimeout(() => {
        copyJsonBtn.innerHTML = originalText;
      }, 2000);
    } catch {
      alert("Gagal menyalin ke clipboard.");
    }
  });

  function escapeHtml(text) {
    if (!text) return "";
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }
});
