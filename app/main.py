import os
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.safety import is_safe_prompt
from app.logger import log_interaction, METRICS
import time
import importlib
from pydub import AudioSegment
from app.llm_voice import speech_to_text, text_to_speech_cloud

app = FastAPI()
templates = Jinja2Templates(directory="templates")

chat_histories = {}

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "llama").lower()
if LLM_PROVIDER == "openai":
    llm_module = importlib.import_module("app.llm_openai")
elif LLM_PROVIDER == "huggingface":
    llm_module = importlib.import_module("app.llm_huggingface")
else:
    llm_module = importlib.import_module("app.llm_llama")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
async def form_get(request: Request):
    session_id = request.cookies.get("session_id", "default")
    history = chat_histories.get(session_id, [])
    return templates.TemplateResponse("index.html", {"request": request, "history": history})

@app.post("/chat", response_class=HTMLResponse)
async def form_post(request: Request, question: str = Form(...)):
    session_id = request.cookies.get("session_id", "default")
    history = chat_histories.get(session_id, [])

    safe = is_safe_prompt(question)
    prompt_for_llm = question
    if not safe:
        prompt_for_llm = (
            "This question might be unsafe or inappropriate for children. Please gently "
            "explain to the user why this kind of question is not safe and why we should not proceed. "
            f"User asked: {question}"
        )

    start_time = time.time()
    if hasattr(llm_module, "generate_response_async"):
        response_text = await llm_module.generate_response_async(prompt_for_llm)
    else:
        import asyncio
        loop = asyncio.get_event_loop()
        response_text = await loop.run_in_executor(None, llm_module.generate_response, prompt_for_llm)

    latency = time.time() - start_time
    history.append({"role": "user", "text": question})
    history.append({"role": "ai", "text": response_text})
    chat_histories[session_id] = history

    METRICS["total_requests"] += 1
    METRICS["unsafe_requests"] += int(not safe)
    METRICS["last_latency"] = latency
    log_interaction(question, response_text, safe, latency)

    return templates.TemplateResponse("index.html", {"request": request, "history": history})

@app.get("/voice", response_class=HTMLResponse)
async def voice_get(request: Request):
    return templates.TemplateResponse("voice.html", {"request": request})

@app.post("/voice")
async def voice_post(request: Request, file: UploadFile = File(...)):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    raw_audio_path = os.path.join(output_dir, file.filename)
    with open(raw_audio_path, "wb") as f:
        f.write(await file.read())

    # Convert uploaded audio to WAV format
    wav_audio_path = os.path.join(output_dir, "converted.wav")
    try:
        AudioSegment.from_file(raw_audio_path).export(wav_audio_path, format="wav")
    except Exception as e:
        return JSONResponse({"error": f"Audio conversion failed: {e}"}, status_code=400)

    transcript = speech_to_text(wav_audio_path)
    safe = is_safe_prompt(transcript)
    prompt_for_llm = transcript
    if not safe:
        prompt_for_llm = (
            "This question might be unsafe or inappropriate for children. Please gently "
            "explain to the user why this kind of question is not safe and why we should not proceed. "
            f"User asked: {transcript}"
        )

    import asyncio
    loop = asyncio.get_event_loop()
    if hasattr(llm_module, "generate_response_async"):
        response_text = await llm_module.generate_response_async(prompt_for_llm)
    else:
        response_text = await loop.run_in_executor(None, llm_module.generate_response, prompt_for_llm)

    session_id = request.cookies.get("session_id", "default")
    history = chat_histories.get(session_id, [])
    history.append({"role": "user", "text": transcript})
    history.append({"role": "ai", "text": response_text})
    chat_histories[session_id] = history

    # Optionally: trigger TTS asynchronously here
    text_to_speech_cloud(response_text)

    return JSONResponse({"transcript": transcript, "answer": response_text})