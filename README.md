# Scripts_sh / py
A collection of helpful Bash and Python scripts.

---

### **1. wallhaven.sh**
> **Description:** Downloads images directly from Wallhaven using `curl`.

*   **How to use:**
    1. Go to [Wallhaven](https://wallhaven.cc) and select a picture.
    2. Right-click the image and select **Copy image address**.
    3. Run the script: `./wallhaven.sh`.
    4. Press `CTRL + SHIFT + V` to paste the URL and hit **Enter**.
    5. Repeat for more images or press `CTRL + D` when finished.

*   **Setup:**
    *   Edit the `DIR` variable in the script to set your download folder.
    *   Make the script executable: `chmod +x wallhaven.sh`.

---

### **2. ghostty-theme-switcher.sh**
> **Description:** Quickly browse and apply themes for the Ghostty terminal emulator.

*   **How to use:**
    1. Run the script: `./ghostty-theme-switcher.sh`.
    2. Search for a theme name or scroll the list.
    3. Select the number and press **Enter**.
    4. Open a new terminal to see the changes.

*   **Setup:**
    *   Updates config at: `$HOME/.config/ghostty/config`.
    *   Make the script executable: `chmod +x ghostty-theme-switcher.sh`.

---

### **3. pkg-explorer.py**
> **Description:** An interactive Arch Linux package explorer. Search `pacman` packages by name, description, or dependencies (similar to `apropos`).

*   **How to use:**
    1. Activate your environment: `source ./pkg-env/bin/activate`.
    2. Run the script: `python pkg-explorer.py`.
    3. Enter a search term (e.g., "blender") to see the version, description, and dependencies.

*   **Setup:**
    1. **Create Environment:** `python3 -m venv pkg-env`
    2. **Activate:**
        *   **Bash/Zsh:** `source ./pkg-env/bin/activate`
        *   **Fish:** `source ./pkg-env/bin/activate.fish`
    3. **Install Dependencies:** `pip install rich`
    4. **Create File:** Save your code as `pkg-explorer.py`.
 
<img width="1247" height="355" alt="Screenshot_20260503_170057" src="https://github.com/user-attachments/assets/01d41b93-7bbc-4c7b-ba9e-73cfa52c0ec1" />

---
