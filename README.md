# Scripts_sh
Various Bash Scripts

#1 wallhaven.sh 
Uses curl to download images from wallhaven. 
\
Go to wallhaven > select picture > right click > copy image address > run the wallhaven script via terminal > CTRL + SHIFT + V to paste the URL > press enter > do the same process for the next image > press CTRL + D when finished. 
\
Make sure to edit the text of the file for the directory (DIR) you want the script to download the files to. 
\
Use chmod +x to make the file an executable after creating it. 
\
------------------------------------------------------------------------------------------------------------------------------------------------------------
#2 ghostty-theme-switcher.sh
Takes all the themes (currently) listed for the ghostty terminal emulator via (ghostty +list-themes)
\
Run the CMD above to view the themes then run the script > search for theme name > select number > enter. This script will auto-apply theme changes to (CONFIG_FILE="$HOME/.config/ghostty/config.ghostty")
\
Feel free to edit the DIR path. 
\
Use chmod +x to make the file an executable after creating it. 
\
Exit > Open new terminal to view the applied theme changes
------------------------------------------------------------------------------------------------------------------------------------------------------------
