# 🗝️ Drew's Cryptex — 6-Ring Cylinder Cipher & Divination App

A web application that transforms the physical 6-ring cylinder cipher into an interactive digital divination wheel and word-alignment game. Built with [Streamlit](https://streamlit.io/) and ready for one-click deployment on **Streamlit Community Cloud** and **GitHub**.

---

## 🌟 What is this Device?

Drew built the original physical mechanical 6-ring brass cipher device shown in the videos. This web application transforms Drew's physical hardware invention into an interactive digital software app (historically originating from Thomas Jefferson's 1795 wheel cipher and the Da Vinci Cryptex), customized with handwritten letter strips taped across each brass ring.

The letter sequence on each ring follows the **9-column Pythagorean numerological reduction alphabet**:
```
A J S | B K T | C L U | D M V | E N W | F O X | G P Y | H Q Z | I R
```
- Total letters: exactly 26 letters per ring (A through Z transposed by numerical vibration).
- When a word is dialed into the central reading line, the other 25 parallel rows around the cylinder shift by exact mathematical offsets, generating secondary anagrams, hidden words, and poetic "readings."

---

## ✨ Features

- **Antique Brass 3D Cylinder Visualizer:** Skeuomorphic display showing all 6 rings with depth shading, curved perspective, and glowing golden target pointers (`▶ [WORD] ◀`).
- **Manual Dial Controls:** Independent `▲` (step up) and `▼` (step down) buttons for each of the 6 rings to dial letters by hand.
- **Random Spin & Free Spin:** 
  - `🎲 Random Spin`: Instant randomized spin of all rings.
  - `⚡ Free Spin`: Continuous automated rolling mode that spins on its own until you click "Stop Free Spin."
- **Target Word Alignment:** Type any word (e.g., `SECRET`, `ORACLE`, `NATURE`, `DREAM`) and the cylinder automatically rotates all 6 rings into position.
- **The Cylinder Reading & Circumference Matrix Scanner:**
  - Scans all 26 rows across the 360° circumference against a 24,000+ English word dictionary.
  - Detects words of length 3, 4, 5, and 6 letters.
  - Generates a **Pythagorean Numerological Vibration** (Numbers 1–9 and Master Numbers 11, 22, 33) and an **Oracle Divination Interpretation** based on the central alignment and surrounding word echoes.
- **Word Hunt Game:** A puzzle mode challenging you to manipulate the cylinder to maximize discovered words and beat daily quests.
- **Custom Ring Configuration:** Switch between the **Device's Pythagorean Sequence**, **Standard A–Z**, or input your own custom 26-letter ring sequences.
- **Reading Log:** Save your favorite cylinder readings with timestamps and export them.

---

## 🚀 Quick Start (Run Locally)

1. **Clone or download this repository:**
   ```bash
   git clone https://github.com/<your-username>/cryptex-oracle.git
   cd cryptex-oracle
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Streamlit app:**
   ```bash
   streamlit run app.py
   ```
   The app will automatically open in your default browser at `http://localhost:8501`.

---

## 📦 How to Push to GitHub

1. **Initialize Git inside your project folder:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit of Cryptex Oracle app"
   ```

2. **Create a new repository on GitHub:**
   - Go to [github.com/new](https://github.com/new).
   - Name it `cryptex-oracle` (or any name you prefer).
   - Leave it **Public**.

3. **Link and push your local code:**
   ```bash
   git remote add origin https://github.com/<your-username>/cryptex-oracle.git
   git branch -M main
   git push -u origin main
   ```

---

## ☁️ How to Deploy Free on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with your GitHub account.
2. Click **"New app"**.
3. Select your repository: `<your-username>/cryptex-oracle`.
4. Branch: `main`.
5. Main file path: `app.py`.
6. Click **"Deploy!"**
Your app will be live on the web with a public URL you can share with anyone!

---

## 📁 Repository Structure

```
cryptex-oracle/
├── app.py              # Main Streamlit application
├── words.txt           # Clean 24,000+ English word dictionary
├── requirements.txt    # Python dependencies (streamlit>=1.28.0)
├── .gitignore          # Git ignore rules
└── README.md           # Documentation & instructions
```
