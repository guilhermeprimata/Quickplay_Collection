from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
changed = []

# Toxic Stench: an old Tone.js implementation survived after external dependencies
# were removed. Replace it with self-contained WebAudio SFX and make the common
# collection sound preference the single source of truth.
path = ROOT / "campo_minado.html"
text = path.read_text(encoding="utf-8")
if "Tone.start()" in text:
    replacement = r'''        // --- Sound Synthesis (self-contained WebAudio) ---
        let soundsReady = false;
        let audioCtx = null;
        let sfxMaster = null;
        let animationFrameId;

        function soundAllowed() {
            try {
                const prefs = JSON.parse(localStorage.getItem('ppg_platform_prefs_v1') || '{}');
                return prefs.sound !== false;
            } catch (_) {
                return true;
            }
        }

        async function initSounds() {
            if (!audioCtx) {
                const AudioCtor = window.AudioContext || window.webkitAudioContext;
                if (!AudioCtor) return;
                audioCtx = new AudioCtor();
                sfxMaster = audioCtx.createGain();
                sfxMaster.gain.value = 0.18;
                sfxMaster.connect(audioCtx.destination);
            }
            if (audioCtx.state === 'suspended') await audioCtx.resume();
            soundsReady = true;
        }

        function synthTone(freq, duration = 0.08, type = 'sine', volume = 0.10, delay = 0, endFreq = null) {
            if (!soundsReady || !audioCtx || !soundAllowed()) return;
            const t = audioCtx.currentTime + delay;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, t);
            if (endFreq) osc.frequency.exponentialRampToValueAtTime(Math.max(25, endFreq), t + duration);
            gain.gain.setValueAtTime(Math.max(0.0001, volume), t);
            gain.gain.exponentialRampToValueAtTime(0.0001, t + duration);
            osc.connect(gain);
            gain.connect(sfxMaster);
            osc.start(t);
            osc.stop(t + duration + 0.02);
        }

        function playClickSound() {
            synthTone(520, 0.055, 'sine', 0.075, 0, 610);
        }
        function playFlagSound() {
            synthTone(660, 0.075, 'triangle', 0.095, 0, 820);
        }
        function playBombSound() {
            synthTone(105, 0.42, 'sawtooth', 0.16, 0, 42);
            synthTone(62, 0.55, 'square', 0.08, 0.025, 30);
        }
        function playWinSound() {
            [523.25,659.25,783.99,1046.5].forEach((f,i)=>synthTone(f,0.20,'triangle',0.085,i*0.12));
            synthTone(1318.51,0.38,'sine',0.075,0.54);
        }
        function playGameOverSound() {
            [392,329.63,261.63,196].forEach((f,i)=>synthTone(f,0.30,'sawtooth',0.065,i*0.18,f*0.72));
        }


        // --- Game Variables ---'''
    text, count = re.subn(
        r"        // --- Sound Synthesis \(Tone\.js\) ---.*?        // --- Game Variables ---",
        replacement,
        text,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise SystemExit("campo_minado.html: Tone.js block anchor mismatch")

    # Remove all pieces of the obsolete secondary sound control. The PPG toolbar
    # is already present and its persisted preference is read by soundAllowed().
    text = re.sub(r'^\s*const toggleSoundBtn\s*=.*?;.*?\n', '', text, count=1, flags=re.M)
    text = re.sub(r'^\s*updateSoundButtonText\(\);.*?\n', '', text, count=1, flags=re.M)
    text = re.sub(
        r"\n\s*// Event listener para o novo botão de som.*?(?=\n\s*window\.addEventListener\('resize')",
        "\n",
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(r'\n\s*<button id="toggle-sound-btn">.*?</button>\s*(?:<!--.*?-->)?', '', text, count=1, flags=re.S)

    if "Tone." in text or "toggleSoundBtn" in text or 'id="toggle-sound-btn"' in text:
        leftovers=[]
        if "Tone." in text: leftovers.append("Tone")
        if "toggleSoundBtn" in text: leftovers.append("toggleSoundBtn")
        if 'id="toggle-sound-btn"' in text: leftovers.append("toggle-sound-btn")
        raise SystemExit("campo_minado.html: legacy sound dependency/control survived repair: " + ",".join(leftovers))
    path.write_text(text, encoding="utf-8")
    changed.append("campo_minado.html: replaced missing Tone.js runtime with WebAudio SFX and removed duplicate sound control")

# Pixel Bomber: normalize the display/title to the collection's official short name.
path = ROOT / "pixel_bomberman.html"
text = path.read_text(encoding="utf-8")
new = text.replace("<title>Pixel Bomberman</title>", "<title>Pixel Bomber</title>").replace("<h2>Pixel Bomberman</h2>", "<h2>Pixel Bomber</h2>")
if new != text:
    path.write_text(new, encoding="utf-8")
    changed.append("pixel_bomberman.html: normalized display name to Pixel Bomber")

print("RUNTIME_REPAIRS_OK changes=" + str(len(changed)))
for item in changed:
    print("-", item)
