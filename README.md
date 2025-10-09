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
- **Face Recognition**: YOLOv8 face detection + LBPH recognizer (`trainneruser.yml`).
- **Weapon Detection**: YOLOv8 model detecting guns and knives.
- **Criminal Registry**: `criminals.json` maintained by the pipeline and `tracker.py`.

---
## Real-time Demo
- Weapon model demo (guns/knives): [[YouTube link](https://youtube.com/playlist?list=PLo_W0PgQBsKIjS82sSxyWH7cXOqnm9D6x&si=Bpqi2vPinoDJo2AS)]
- Full pipeline demo (faces + modes + alarm + screenshots): [YouTube link pending]


### Gun Detection Screenshots Example


<div align="center">

<img src="screenshots\criminal.128.1.jpg" alt="gun1" style="width: 200px; height: 400px; object-fit: cover; margin: 5px;" />
<img src="screenshots\criminal.128.2.jpg" alt="gun2" style="width: 200px; height: 400px; object-fit: cover; margin: 5px;" />
<img src="screenshots\criminal.128.3.jpg" alt="gun3" style="width: 200px; height: 400px; object-fit: cover; margin: 5px;" />
<img src="screenshots\criminal.128.4.jpg" alt="gun4" style="width: 200px; height: 400px; object-fit: cover; margin: 5px;" />
<img src="screenshots\criminal.128.148.jpg" alt="gun5" style="width: 200px; height: 400px; object-fit: cover; margin: 5px;" />
<img src="screenshots\criminal.128.213.jpg" alt="gun6" style="width: 200px; height: 400px; object-fit: cover; margin: 5px;" />

</div>


### Knife Detection Screenshots Example

<div align="center">

<img src="screenshots/criminal.110.1.jpg" alt="shot1" style="width: 200px; height: 300px; object-fit: cover; margin: 5px;" />
<img src="screenshots/criminal.110.23.jpg" alt="shot3" style="width: 200px; height: 300px; object-fit: cover; margin: 5px;" />

<img src="screenshots/criminal.110.44.jpg" alt="shot4" style="width: 200px; height: 300px; object-fit: cover; margin: 5px;" />
<img src="screenshots/criminal.110.166.jpg" alt="shot5" style="width: 200px; height: 300px; object-fit: cover; margin: 5px;" />
<img src="screenshots/criminal.110.656.jpg" alt="shot6" style="width: 200px; height: 300px; object-fit: cover; margin: 5px;" />

</div>

---

## Confusion Matrix
Below is the normalized confusion matrix for the weapon detector. Use it to understand class-wise performance and common confusions.

![Confusion Matrix](confusion_matrix_normalized.png)

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
  
### GUI
 ![image](https://github.com/UDJAT74/Security_Dtection/assets/128726786/347d417c-bae2-4bab-97f1-a67613a9d417)

### Run
- Use GUI: `pyhton GUI.py`  
- Register user: `python create.py` or click on `Create` button in GUI
- Recognize / monitor users: use `detector()` in `detector.py` or click on `live face Detect` button in GUI
- Criminal capture flow (screenshots + retrain): `python tracker.py`
- Weapon-only demo: `python weaponDetect.py` or click on `live weapon` button in GUI
- Combined live demo (faces + weapons): use `live_detection()` in `detector.py` or click on `live Detection ` button in GUI

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

## Ethics & Disclaimer
Use responsibly and comply with local laws and privacy regulations. Models may exhibit bias or errors; always keep a human in the loop for critical decisions.

---

## Contributors
Supervisor: Dr/Wael Zakriya
1. [Ahmed Abdelgelel](https://github.com/GLGL0x00)
2. [Ahmed Salem](https://github.com/el3amed74)
3. [Youssef Tarek](https://github.com/yousseftarek2001)
4. [Mohamed Medhat](https://github.com/mohamedmedhat1)

## Contributing
Contributions are welcome! Feel free to open issues or PRs.
