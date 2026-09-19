"""Reliable voice helpers for Streamlit chatbots (bot TTS + user STT)."""
import html
import io
import json
import re
import hashlib

import streamlit as st
import streamlit.components.v1 as components


def _plain(text: str) -> str:
    """Strip markdown-ish markup for natural speech."""
    if not text:
        return ""
    t = re.sub(r"```[\s\S]*?```", " ", text)
    t = re.sub(r"[*_`#~>|\-]", " ", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:900]


@st.cache_data(show_spinner=False, ttl=3600)
def _tts_mp3(text: str) -> bytes:
    """Generate MP3 bytes via Google TTS (cached)."""
    from gtts import gTTS

    buf = io.BytesIO()
    gTTS(text=text, lang="en", slow=False).write_to_fp(buf)
    return buf.getvalue()


def bot_speak(text: str, *, auto: bool = True, label: str = "Bot voice") -> None:
    """
    Speak text reliably:
    1) gTTS + st.audio (works in all browsers)
    2) Speak/Stop buttons via parent-window Web Speech as backup
    """
    clean = _plain(text)
    if not clean:
        return

    uid = hashlib.md5(clean.encode("utf-8")).hexdigest()[:10]
    st.caption(f"🔊 {label}")

    # --- Primary: audible MP3 (reliable) ---
    try:
        with st.spinner("Preparing voice…"):
            audio_bytes = _tts_mp3(clean)
        st.audio(audio_bytes, format="audio/mp3", autoplay=bool(auto))
    except Exception as e:
        st.warning(f"Cloud voice unavailable ({e}). Use the Speak button below.")

    # --- Backup: browser speech on user click (parent window = not blocked) ---
    payload = json.dumps(clean)
    components.html(
        f"""
        <div style="font-family:Outfit,sans-serif;display:flex;gap:8px;align-items:center;">
          <button id="speakBtn_{uid}" style="background:#9B8EC4;color:#fff;border:none;
            border-radius:999px;padding:8px 16px;cursor:pointer;font-weight:600;">🔊 Speak again</button>
          <button id="stopBtn_{uid}" style="background:#F3EEF9;color:#5B4B8A;border:1px solid #D4C8E8;
            border-radius:999px;padding:8px 14px;cursor:pointer;">⏹ Stop</button>
        </div>
        <script>
          (function() {{
            const text = {payload};
            function getSynth() {{
              try {{ return window.parent.speechSynthesis || window.speechSynthesis; }}
              catch (e) {{ return window.speechSynthesis; }}
            }}
            function speak() {{
              const synth = getSynth();
              if (!synth) {{ alert('Speech not supported in this browser'); return; }}
              synth.cancel();
              const u = new SpeechSynthesisUtterance(text);
              u.rate = 1.0; u.pitch = 1.0; u.lang = 'en-US';
              // Chrome quirk: resume if speech stalls
              const keepAlive = setInterval(function() {{
                if (!synth.speaking) {{ clearInterval(keepAlive); return; }}
                synth.pause(); synth.resume();
              }}, 8000);
              u.onend = function() {{ clearInterval(keepAlive); }};
              synth.speak(u);
            }}
            document.getElementById('speakBtn_{uid}').onclick = speak;
            document.getElementById('stopBtn_{uid}').onclick = function() {{
              const synth = getSynth();
              if (synth) synth.cancel();
            }};
          }})();
        </script>
        """,
        height=48,
    )


def voice_mic_panel(key: str = "voice"):
    """User speech → text via Streamlit audio recorder + Google recognition."""
    st.markdown("##### 🎤 Speak your answer")
    st.caption("Click the mic, speak, then stop — your words will appear in the answer box. (Chrome / Edge)")

    # Live browser mic (visual + copy aid)
    components.html(
        f"""
        <div style="font-family:Outfit,sans-serif;background:#FBF8FF;border:1px solid #E4DAF2;
                    border-radius:16px;padding:14px 16px;color:#2D2A3A;">
          <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px;">
            <button id="micStart" style="background:linear-gradient(135deg,#9B8EC4,#7B6BA8);
              color:#fff;border:none;border-radius:999px;padding:10px 18px;cursor:pointer;font-weight:600;">
              🎙️ Start listening
            </button>
            <button id="micStop" style="background:#fff;color:#5B4B8A;border:1px solid #D4C8E8;
              border-radius:999px;padding:10px 16px;cursor:pointer;">Stop</button>
            <button id="micCopy" style="background:#fff;color:#5B4B8A;border:1px solid #D4C8E8;
              border-radius:999px;padding:10px 16px;cursor:pointer;">Copy text</button>
          </div>
          <div id="status" style="font-size:0.8rem;color:#7B6BA8;margin-bottom:6px;">Idle — allow mic permission</div>
          <div id="live" style="min-height:48px;padding:10px 12px;background:#fff;border-radius:12px;
            border:1px dashed #D4C8E8;font-size:0.95rem;"></div>
        </div>
        <script>
          (function() {{
            const SR = window.SpeechRecognition || window.webkitSpeechRecognition
              || (window.parent && (window.parent.SpeechRecognition || window.parent.webkitSpeechRecognition));
            const live = document.getElementById('live');
            const status = document.getElementById('status');
            let rec = null, finalText = '';
            if (!SR) {{
              status.textContent = 'Live mic not supported — use the recorder below.';
              return;
            }}
            rec = new SR();
            rec.continuous = true;
            rec.interimResults = true;
            rec.lang = 'en-US';
            rec.onstart = () => status.textContent = 'Listening… speak clearly';
            rec.onerror = (e) => status.textContent = 'Mic: ' + e.error + ' — try the recorder below';
            rec.onend = () => status.textContent = 'Stopped — paste/copy into the answer box if needed';
            rec.onresult = (event) => {{
              let interim = '';
              for (let i = event.resultIndex; i < event.results.length; i++) {{
                const t = event.results[i][0].transcript;
                if (event.results[i].isFinal) finalText += t + ' ';
                else interim += t;
              }}
              live.textContent = (finalText + interim).trim();
            }};
            document.getElementById('micStart').onclick = () => {{
              finalText = ''; live.textContent = '';
              try {{ rec.start(); }} catch (e) {{ status.textContent = String(e); }}
            }};
            document.getElementById('micStop').onclick = () => {{ try {{ rec.stop(); }} catch (e) {{}} }};
            document.getElementById('micCopy').onclick = () => {{
              const t = live.textContent || '';
              if (navigator.clipboard) navigator.clipboard.writeText(t);
              status.textContent = 'Copied — paste into Your answer';
            }};
          }})();
        </script>
        """,
        height=200,
    )

    audio = st.audio_input("Record clip → convert to text (most reliable)", key=f"{key}_audio")
    if audio is not None:
        # Avoid re-transcribing the same clip on every rerun
        clip_id = hashlib.md5(audio.getvalue()).hexdigest()
        if st.session_state.get(f"{key}_clip_id") != clip_id:
            transcript = transcribe_audio(audio)
            st.session_state[f"{key}_clip_id"] = clip_id
            if transcript:
                st.session_state[f"{key}_transcript"] = transcript
                st.success(f"Heard: _{transcript}_")
            else:
                st.warning("Couldn't understand the audio — try again, speak closer to the mic.")

    return st.session_state.get(f"{key}_transcript")


def transcribe_audio(audio_file):
    """Transcribe Streamlit audio_input bytes via SpeechRecognition."""
    try:
        import speech_recognition as sr
    except ImportError:
        st.info("Install: `pip install SpeechRecognition`")
        return None

    try:
        data = audio_file.getvalue() if hasattr(audio_file, "getvalue") else audio_file.read()
        recognizer = sr.Recognizer()
        # Streamlit usually gives WAV; if not, still try
        with sr.AudioFile(io.BytesIO(data)) as source:
            audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data)
    except Exception as e:
        if "UnknownValueError" in type(e).__name__:
            return None
        st.caption(f"Voice note: {e}")
        return None


def voice_answer_box(key: str, placeholder: str = "Type or use voice…", height: int = 120) -> str:
    """Text area synced from last voice transcript when available."""
    text_key = f"{key}_text"
    transcript = st.session_state.get(f"{key}_transcript", "")
    if transcript and st.session_state.get(f"{key}_applied_transcript") != transcript:
        st.session_state[text_key] = transcript
        st.session_state[f"{key}_applied_transcript"] = transcript
    if text_key not in st.session_state:
        st.session_state[text_key] = ""
    return st.text_area(
        "Your answer",
        height=height,
        placeholder=placeholder,
        key=text_key,
    )
