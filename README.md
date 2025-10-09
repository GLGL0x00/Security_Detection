## Security Detection: Face, Weapon, and Criminal Recognition (Real-time)

An end-to-end system that detects weapons (guns/knives), recognizes faces, and maintains a persistent list of criminals. The system triggers alarms and captures evidence on criminal detection.

### Problem Description
Traditional CCTV lacks real-time context. This project fuses face recognition and weapon detection to: (1) flag unknown individuals holding weapons, (2) enforce per-user weapon permissions, and (3) instantly alert on known criminals with visual evidence.

### How It Works (Overview)
The pipeline combines a YOLO-based detector with LBPH face recognition, maintaining user modes and a criminals registry.

![System Architecture](Diagram.png)

### Core Logic: Three Cases
- **Unknown person holding weapon (gun/knife)**: Add to `criminals.json` for future detection.
- **Known person with modes (allowed / not allowed)**: If not allowed and holding weapon → add to criminals.
- **Criminal detected (with or without weapon)**: Play alarm and capture screenshot.

### Model Components
- **Face Recognition**: YOLO face detection + LBPH recognizer (`trainneruser.yml`).
- **Weapon Detection**: YOLO model detecting guns and knives.
- **Criminal Registry**: `criminals.json` maintained by the pipeline and `tracker.py`.

---

## Confusion Matrix
Below is the normalized confusion matrix for the weapon detector. Use it to understand class-wise performance and common confusions.

![Confusion Matrix](confusion_matrix_normalized.png)

---

## Real-time Demo
- Weapon model demo (guns/knives): [YouTube link pending]
- Full pipeline demo (faces + modes + alarm + screenshots): [YouTube link pending]

> Once links are available, replace the placeholders above. Optionally add short GIF previews under `static/img/`.


### Gun Detection Example


<div align="center">

<img src="screenshots\criminal.128.1.jpg" alt="gun1" style="width: 200px; height: 400px; object-fit: cover; margin: 5px;" />
<img src="screenshots\criminal.128.2.jpg" alt="gun2" style="width: 200px; height: 400px; object-fit: cover; margin: 5px;" />
<img src="screenshots\criminal.128.3.jpg" alt="gun3" style="width: 200px; height: 400px; object-fit: cover; margin: 5px;" />
<img src="screenshots\criminal.128.4.jpg" alt="gun4" style="width: 200px; height: 400px; object-fit: cover; margin: 5px;" />
<img src="screenshots\criminal.128.148.jpg" alt="gun5" style="width: 200px; height: 400px; object-fit: cover; margin: 5px;" />
<img src="screenshots\criminal.128.213.jpg" alt="gun6" style="width: 200px; height: 400px; object-fit: cover; margin: 5px;" />

</div>


### Knife Detection Example

https://github.com/UDJAT74/Security_Dtection/assets/128726786/knife_tracker.mp4

### Sample Real-time Screenshots

<div align="center">

<img src="screenshots/criminal.110.1.jpg" alt="shot1" style="width: 200px; height: 200px; object-fit: cover; margin: 5px;" />
<img src="screenshots/criminal.110.6.jpg" alt="shot2" style="width: 200px; height: 200px; object-fit: cover; margin: 5px;" />
<img src="screenshots/criminal.110.23.jpg" alt="shot3" style="width: 200px; height: 200px; object-fit: cover; margin: 5px;" />

<img src="screenshots/criminal.110.44.jpg" alt="shot4" style="width: 200px; height: 200px; object-fit: cover; margin: 5px;" />
<img src="screenshots/criminal.110.166.jpg" alt="shot5" style="width: 200px; height: 200px; object-fit: cover; margin: 5px;" />
<img src="screenshots/criminal.110.656.jpg" alt="shot6" style="width: 200px; height: 200px; object-fit: cover; margin: 5px;" />

</div>

---

## Quick Start

### Requirements
Install Python 3.9+ and dependencies:

```bash
pip install -r requirments.txt
```

### Prepare Data
- Ensure `users.json` and `trainneruser.yml` exist for known users.
- Use `create.py` to register a new user (captures 60 face images and retrains).

### Run
- Register user: `python create.py`
- Recognize / monitor users: `python detector.py`
- Criminal capture flow (screenshots + retrain): `python tracker.py`
- Weapon-only demo: `python weaponDetect.py`
- Combined live demo (faces + weapons): use `live_detection()` in `detector.py`

---

## Project Structure (Key Files)

```
create.py           # Register user and retrain
detector.py         # Face recognition, criminals, live detection
tracker.py          # Hand/object overlap, capture screenshots, update criminals
weaponDetect.py     # Weapon-only detection demo
trainner.py         # Training utilities (LBPH)
users.json          # Known users with modes (allowed / not allowed)
criminals.json      # Criminal registry
models/             # Model weights (YOLO)
static/, templates/ # Web/static assets (if applicable)
```

---

## Streamlit App (TODO)
- Live monitoring dashboard
- Recent detections and screenshots
- Toggle user modes (allowed/not allowed)
- Start/stop camera pipelines

---

## Ethics & Disclaimer
Use responsibly and comply with local laws and privacy regulations. Models may exhibit bias or errors; always keep a human in the loop for critical decisions.

## License
MIT (or update to your chosen license)

## Contributors
Supervisor: Dr/Wael Zakriya
1. [Ahmed Abdelgelel](https://github.com/Ahmed-abdelgalil)
2. [Ahmed Salem](https://github.com/el3amed74)
3. [Youssef Tarek](https://github.com/yousseftarek2001)
4. [Mohamed Medhat](https://github.com/mohamedmedhat1)

## Contributing
Contributions are welcome! Feel free to open issues or PRs.
