# Scripts_sh
A collection of helpful Bash scripts.

---

### **1. wallhaven.sh**
Downloads images directly from Wallhaven using `curl`.

**How to use:**
1. Go to [Wallhaven](https://wallhaven.cc) and select a picture.
2. Right-click the image and select **Copy image address**.
3. Run the script in your terminal: `./wallhaven.sh`.
4. Press `CTRL + SHIFT + V` to paste the URL and hit **Enter**.
5. Repeat for more images or press `CTRL + D` when finished.

**Setup:**
*   Edit the `DIR` variable in the script to set your preferred download folder.
*   Make the script executable: `chmod +x wallhaven.sh`.

---

### **2. ghostty-theme-switcher.sh**
Quickly browse and apply themes for the Ghostty terminal emulator.

**How to use:**
1. Run the script: `./ghostty-theme-switcher.sh`.
2. Search for a theme name or scroll the list.
3. Select the corresponding number and press **Enter**.
4. Close your terminal and open a new one to see the changes.

**Setup:**
*   This script automatically updates your config at: `$HOME/.config/ghostty/config`.
*   You can edit the `CONFIG_FILE` path inside the script if yours is located elsewhere.
*   Make the script executable: `chmod +x ghostty-theme-switcher.sh`.
