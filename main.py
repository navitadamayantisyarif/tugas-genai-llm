import os
import json
import re
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from groq import AsyncGroq, APIConnectionError, AuthenticationError, RateLimitError

# Load environment variables from .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

app = FastAPI(
    title="Meeting Notes & Action Items Analyzer API",
    description="GenAI-powered Meeting Notes Analyzer built with FastAPI and Groq LLM",
    version="1.0.0",
)

# CORS middleware to support any web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# SYSTEM PROMPT & EXPERIMENT PROMPTS
# ==========================================

SYSTEM_PROMPT = (
    "You are an expert Executive AI Meeting Assistant and Project Management Specialist. "
    "Your expertise lies in analyzing unstructured meeting notes and transcripts, "
    "synthesizing key insights, detecting decisions, and extracting concrete actionable tasks with clear ownership. "
    "You always provide strictly valid, parseable JSON responses following the requested schema."
)

PROMPT_TEMPLATES = {
    # Prompt A: Sederhana (Basic Prompt)
    "A": (
        "Summarize this meeting and extract action items:\n\n{text}"
    ),
    # Prompt B: Role + Task + Context
    "B": (
        "Role: Senior Project Manager & Meeting Secretary\n"
        "Task: Analyze the meeting transcript below, identify the main discussion topics, "
        "and extract key action items.\n"
        "Context: This meeting took place within a fast-moving product and engineering team "
        "discussing project updates, technical blockers, and next steps.\n\n"
        "Meeting Transcript:\n{text}"
    ),
    # Prompt C: Role + Task + Context + Constraint + Output Format (Prompt Utama Aplikasi - Full Structured)
    "C": (
        "Role: Lead Agile Scrum Master and Executive Technical Secretary\n\n"
        "Task: Thoroughly analyze the unstructured meeting transcript below. "
        "Generate a concise executive summary, identify critical discussion points, "
        "document all formal decisions made, extract concrete prioritized action items, "
        "and evaluate the overall meeting tone.\n\n"
        "Context: The team discussed project status, architecture decisions, resource assignments, "
        "and upcoming delivery deadlines. Some tasks might have explicit assignees while others are general.\n\n"
        "Constraint:\n"
        "1. Do not hallucinate or invent tasks, names, or decisions not present in the text.\n"
        "2. Only extract formal engineering, product, or organizational tasks. Strictly ignore trivial daily chatter, casual remarks, jokes, or non-work domestic chores (e.g., buying snacks, coffee, lunch).\n"
        "3. If task assignment is vague or mentions multiple alternative candidates (e.g. 'A or B'), set assignee strictly to 'Unassigned' and describe the ambiguity in the task description.\n"
        "4. Deadline must be an estimated timeframe mentioned in text or 'TBD' if no clear deadline was established.\n"
        "5. Priority must be strictly one of: 'High', 'Medium', or 'Low'.\n"
        "6. Format output strictly as valid JSON matching the exact schema specified below.\n"
        "7. Do NOT include markdown code blocks, backticks (```json), or conversational preface/postscript.\n\n"
        "Output Format (Valid JSON):\n"
        "{\n"
        '  "meeting_title": "Descriptive title of the meeting",\n'
        '  "summary": "2-3 sentences concise executive summary",\n'
        '  "key_points": ["Point 1", "Point 2"],\n'
        '  "decisions_made": ["Decision 1", "Decision 2"],\n'
        '  "action_items": [\n'
        '    {"task": "Action description", "assignee": "Name", "deadline": "Date/Time or TBD", "priority": "High|Medium|Low"}\n'
        "  ],\n"
        '  "sentiment_tone": "e.g., Productive & Decisive, Collaborative, or Tense & Urgent"\n'
        "}\n\n"
        "Meeting Transcript:\n{text}"
    ),
}

# ==========================================
# PYDANTIC SCHEMAS (Request & Response)
# ==========================================

class AnalyzeRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=10,
        description="Raw meeting transcript or notes to be analyzed",
        examples=["Meeting sprint planning tanggal 31 Oktober 2026. Budi sepakat menyelesaikan integrasi API Groq paling lambat hari Selasa. Siti akan menyiapkan unit test untuk endpoint authentication sebelum Rabu. Tim memutuskan menggunakan PostgreSQL bukan MongoDB. Suasana diskusi sangat produktif."],
    )
    meeting_title: Optional[str] = Field(
        None,
        description="Optional title for the meeting. If omitted, AI will infer one.",
        examples=["Sprint Planning & API Integration"],
    )
    prompt_version: Optional[str] = Field(
        "C",
        description="Prompt version experiment: 'A' (Simple), 'B' (Role+Task+Context), or 'C' (Role+Task+Context+Constraint+Format)",
        examples=["C"],
    )


class ActionItem(BaseModel):
    task: str = Field(..., description="Action item description")
    assignee: str = Field(default="Unassigned", description="Person responsible")
    deadline: str = Field(default="TBD", description="Expected completion deadline")
    priority: str = Field(default="Medium", description="High, Medium, or Low")


class AnalyzeResponse(BaseModel):
    meeting_title: str = Field(..., description="Title or topic of the meeting")
    summary: str = Field(..., description="Executive summary of the meeting")
    key_points: List[str] = Field(..., description="Key discussion points")
    decisions_made: List[str] = Field(default_factory=list, description="Decisions agreed upon")
    action_items: List[ActionItem] = Field(..., description="Extracted actionable tasks with assignees")
    sentiment_tone: str = Field(default="Neutral", description="Meeting tone and sentiment")
    prompt_version_used: str = Field(..., description="Prompt version used (A, B, or C)")
    model_used: str = Field(..., description="LLM model used for analysis")


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def clean_json_response(raw_text: str) -> dict:
    """Extract and parse JSON from LLM response, stripping markdown blocks if present."""
    text = raw_text.strip()
    # Check for markdown code fences like ```json ... ```
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        text = match.group(1)
    else:
        # Match outermost curly braces
        match_braces = re.search(r"(\{.*\})", text, re.DOTALL)
        if match_braces:
            text = match_braces.group(1)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Fallback dictionary if JSON parsing fails (e.g. on basic Prompt A output)
        return {
            "meeting_title": "Meeting Summary",
            "summary": raw_text[:500],
            "key_points": [line.strip("- *") for line in raw_text.splitlines() if line.strip().startswith(("-", "*"))][:5] or ["Hasil ekstraksi teks tidak dalam format JSON terstruktur."],
            "decisions_made": [],
            "action_items": [],
            "sentiment_tone": "Unspecified",
        }


def get_groq_client() -> AsyncGroq:
    """Initialize AsyncGroq client with environment variable validation."""
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key or "placeholder" in api_key.lower() or api_key == "your_api_key_here":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "GROQ_API_KEY belum dikonfigurasi di file .env. "
                "Silakan buka file .env dan isi GROQ_API_KEY Anda dengan key valid dari https://console.groq.com/keys"
            ),
        )
    return AsyncGroq(api_key=api_key)


# ==========================================
# API ENDPOINTS
# ==========================================

@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint to verify API status and API key configuration."""
    api_key = os.getenv("GROQ_API_KEY", "")
    is_configured = bool(api_key and "placeholder" not in api_key.lower() and api_key != "your_api_key_here")
    return {
        "status": "healthy",
        "service": "Meeting Notes & Action Items Analyzer API",
        "groq_api_key_configured": is_configured,
        "default_model": GROQ_MODEL,
    }


@app.post("/analyze", response_model=AnalyzeResponse, tags=["Meeting Analyzer"])
async def analyze_meeting(request: AnalyzeRequest):
    """
    Endpoint utama untuk menganalisis catatan atau transkrip rapat.
    
    Menerima teks rapat dan menghasilkan structured output JSON yang terdiri dari:
    - meeting_title
    - summary
    - key_points
    - decisions_made
    - action_items (task, assignee, deadline, priority)
    - sentiment_tone
    """
    if not request.text or len(request.text.strip()) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Teks transkrip rapat terlalu pendek. Minimal 10 karakter.",
        )

    version = (request.prompt_version or "C").upper()
    if version not in PROMPT_TEMPLATES:
        version = "C"

    prompt_template = PROMPT_TEMPLATES[version]
    user_prompt = prompt_template.replace("{text}", request.text)

    # Initialize Groq client
    client = get_groq_client()

    try:
        # Build messages with System Prompt and User Prompt
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]

        # Call Groq LLM API
        # Model default: llama-3.3-70b-versatile
        completion = await client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.2 if version == "C" else 0.5,
            response_format={"type": "json_object"} if version == "C" else None,
        )

        raw_content = completion.choices[0].message.content or "{}"
        parsed_data = clean_json_response(raw_content)

        # Normalize and construct structured response
        title = request.meeting_title or parsed_data.get("meeting_title", "Meeting Analysis")
        summary = parsed_data.get("summary", "Ringkasan rapat berhasil dibuat.")
        key_points = parsed_data.get("key_points", [])
        decisions = parsed_data.get("decisions_made", [])
        sentiment = parsed_data.get("sentiment_tone", "Productive")

        # Normalize action items
        raw_actions = parsed_data.get("action_items", [])
        action_items_list: List[ActionItem] = []
        for item in raw_actions:
            if isinstance(item, dict):
                action_items_list.append(
                    ActionItem(
                        task=str(item.get("task", "Tugas tidak spesifik")),
                        assignee=str(item.get("assignee", "Team")),
                        deadline=str(item.get("deadline", "TBD")),
                        priority=str(item.get("priority", "Medium")),
                    )
                )
            elif isinstance(item, str):
                action_items_list.append(
                    ActionItem(
                        task=item,
                        assignee="Team",
                        deadline="TBD",
                        priority="Medium",
                    )
                )

        return AnalyzeResponse(
            meeting_title=title,
            summary=summary,
            key_points=key_points if isinstance(key_points, list) else [str(key_points)],
            decisions_made=decisions if isinstance(decisions, list) else [str(decisions)],
            action_items=action_items_list,
            sentiment_tone=sentiment,
            prompt_version_used=version,
            model_used=GROQ_MODEL,
        )

    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autentikasi Groq gagal. Pastikan GROQ_API_KEY di file .env sudah benar.",
        )
    except RateLimitError:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit Groq API tercapai. Silakan coba beberapa saat lagi.",
        )
    except APIConnectionError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Gagal menghubungi server Groq. Periksa koneksi internet Anda.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Terjadi kesalahan saat memproses rapat: {str(e)}",
        )


# ==========================================
# STATIC FILES & WEB DASHBOARD (Opsional tapi menarik)
# ==========================================
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/", include_in_schema=False)
    async def serve_index():
        index_path = os.path.join(static_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"message": "Meeting Notes & Action Items Analyzer API is running. Visit /docs for Swagger."}
else:
    @app.get("/", include_in_schema=False)
    async def home():
        return {
            "message": "Meeting Notes & Action Items Analyzer API is running.",
            "docs": "/docs",
            "health": "/health",
        }
