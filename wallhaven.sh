#!/usr/bin/env bash
set -euo pipefail

DOWNLOAD_DIR="/home/$USER/Pictures/Wallpapers"
mkdir -p "$DOWNLOAD_DIR"

# Dependencies
for cmd in curl sha1sum file; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "Error: '$cmd' is required but not installed."
        exit 1
    fi
done

shopt -s nocasematch

download_image() {
    local url="$1"
    local idx="$2"
    local total="$3"

    # 1. TRIM whitespace/carriage returns 
    # (Using native bash to avoid xargs parsing errors on URLs with quotes/ampersands)
    url="${url#"${url%%[![:space:]]*}"}" # Trim leading whitespace
    url="${url%"${url##*[![:space:]]}"}" # Trim trailing whitespace
    url="${url//$'\r'/}"                 # Remove carriage returns

    [[ -z "$url" ]] && return 1

    if [[ ! "$url" =~ ^https?:// ]]; then
        echo "[$idx/$total] Skipped invalid URL (Format Error): '$url'"
        return 1
    fi

    local clean_url="${url%%\?*}"
    local filename
    filename="$(basename "$clean_url")"

    # Ensure filename isn't just the domain or empty
    if [[ ! "$filename" =~ \.(jpg|jpeg|png|gif|webp)$ ]]; then
        filename="$(printf '%s' "$url" | sha1sum | awk '{print $1}').jpg"
    fi

    local target="$DOWNLOAD_DIR/$filename"

    if [[ -e "$target" ]]; then
        target="${target%.*}_$(date +%s).${target##*.}"
    fi

    echo "[$idx/$total] Downloading: $url"

    # 2. Use a more robust User-Agent
    if curl -fSL \
        --retry 3 \
        --retry-delay 2 \
        --connect-timeout 10 \
        --max-time 60 \
        -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
        --progress-bar \
        "$url" -o "$target"; then

        if [[ -s "$target" ]]; then
            local mime
            mime=$(file --mime-type -b "$target")

            if [[ "$mime" =~ ^image/ ]]; then
                echo "[$idx/$total] Saved: $(basename "$target")"
                return 0
            else
                echo "[$idx/$total] Error: Downloaded file is not an image ($mime)"
            fi
        fi

        rm -f "$target"
        return 1
    else
        echo "[$idx/$total] Download failed (Check URL or Connection)"
        return 1
    fi
}

success=0
failed=0
urls=()

# ---------- INPUT HANDLING ----------
if [[ $# -gt 0 ]]; then
    urls=("$@")
elif [[ ! -t 0 ]]; then
    mapfile -t urls
else
    echo "Paste URLs (one per line). Press Ctrl+D when finished:"
    mapfile -t urls
fi

# Clean empty entries
cleaned=()
for u in "${urls[@]}"; do
    [[ -z "$u" ]] && continue
    cleaned+=("$u")
done
urls=("${cleaned[@]}")

total=${#urls[@]}
[[ $total -eq 0 ]] && { echo "No URLs provided."; exit 0; }

echo "Processing $total URL(s)..."
count=0
for url in "${urls[@]}"; do
    # FIXED: Pre-increment prevents evaluating to 0 and triggering set -e
    ((++count)) 
    if download_image "$url" "$count" "$total"; then
        ((++success))
    else
        ((++failed))
    fi
done

echo -e "\nBatch complete | Success: $success | Failed: $failed"
