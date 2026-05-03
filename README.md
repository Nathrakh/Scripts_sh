Scripts_sh
A collection of helpful Bash and Python scripts.

1. wallhaven.sh
Downloads images directly from Wallhaven using curl.

How to use:

Go to Wallhaven and select a picture.

Right-click the image and select Copy image address.

Run the script: ./wallhaven.sh.

Press CTRL + SHIFT + V to paste the URL and hit Enter.

Repeat for more images or press CTRL + D when finished.

Setup:

Edit the DIR variable in the script to set your download folder.

Make the script executable: chmod +x wallhaven.sh.

2. ghostty-theme-switcher.sh
Quickly browse and apply themes for the Ghostty terminal emulator.

How to use:

Run the script: ./ghostty-theme-switcher.sh.

Search for a theme name or scroll the list.

Select the number and press Enter.

Open a new terminal to see the changes.

Setup:

Updates config at: $HOME/.config/ghostty/config.

Make the script executable: chmod +x ghostty-theme-switcher.sh.

3. pkg-explorer.py
An interactive Arch Linux package explorer. Search pacman packages by name, description, or dependencies (similar to apropos).

How to use:

Activate your environment (e.g., source ./pkg-env/bin/activate).

Run the script: python pkg-explorer.py.

Enter a search term (e.g., "blender") to see the version, description, and dependencies.

Setup:

Create a virtual environment: python3 -m venv pkg-env.

Activate it:

Bash/Zsh: source ./pkg-env/bin/activate

Fish: source ./pkg-env/bin/activate.fish

Install the required library: pip install rich.

Create pkg-explorer.py and paste the script code.
