# Project Jarvis: Desktop Voice Automation 🎙️⚡

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Architecture](https://img.shields.io/badge/Architecture-Hybrid%20Edge%2FCloud-orange)

> **A latency-optimized voice assistant that combines offline wake-word detection (Porcupine) with high-accuracy speech recognition (Whisper) to automate system tasks.**

---

## 📝 Overview
**Project Jarvis** is a Python-based voice assistant designed to streamline desktop interaction. Unlike standard assistants that require constant cloud connectivity, Jarvis uses a **hybrid pipeline**:
1.  **Edge Processing:** Runs a lightweight, offline wake-word engine (`Picovoice Porcupine`) to monitor for the keyword "Jarvis" with near-zero latency and CPU usage.
2.  **Local/Cloud Inference:** Triggers the heavier `OpenAI Whisper` model only when activated for high-precision command recognition.

This architecture enables a **"Follow-Up Mode"**, allowing the user to issue multiple commands in a conversational loop without repeating the wake word every time.

---

## ✨ Key Features

### 🧠 **Smart Interaction Loop**
- **Zero-Latency Wake Word:** Instant activation using `Picovoice Porcupine`.
- **Follow-Up Mode:** After activation, Jarvis enters a **30-second active listening window**, allowing for natural, continuous conversation without constant wake-word repetition.

### ⚡ **System Automation**
- **App Launcher:** Direct path mapping to launch complex executables (Valorant, Steam, Opera GX) via voice.
- **Media Control:** "Open YouTube", "Launch Spotify".
- **Information Retrieval:** Integrated Wikipedia and Google Search for instant query answers.

### 🎙️ **High-Fidelity ASR**
- Utilizes **OpenAI Whisper (Base Model)** for robust speech-to-text conversion, handling accents and fast speech significantly better than traditional libraries.

---

## 🛠️ Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Wake Word** | `Picovoice Porcupine` | Offline, low-power keyword detection. |
| **STT Engine** | `OpenAI Whisper` | High-accuracy speech-to-text transcription. |
| **Audio Capture** | `PyAudio` | Real-time microphone stream handling. |
| **TTS Engine** | `pyttsx3` | Offline Text-to-Speech synthesis for responses. |
| **Process Mgmt** | `os` / `subprocess` | Direct Windows process execution. |

---

## 🏗️ Architecture Flow

1.  **Standby Phase:** The system listens *only* for the specific keyword "Jarvis" using Porcupine (low resource usage).
2.  **Activation:** Upon detection, it triggers the `PyAudio` stream to record the user's command.
3.  **Transcription:** The audio is passed to the `Whisper` model to convert speech to text.
4.  **Intent Parsing:** The text is analyzed for keywords (e.g., "Launch", "Search", "Time").
5.  **Execution:** The corresponding Python function executes the system task (e.g., `os.startfile(path)`).
6.  **Active Loop:** The system resets a 30-second timer, waiting for the next command without requiring the wake word again.

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/Subhan206/project-jarvis.git](https://github.com/Subhan206/project-jarvis.git)
cd project-jarvis
