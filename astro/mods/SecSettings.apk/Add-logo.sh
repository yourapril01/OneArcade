#!/bin/bash

# Because apktool.sh runs this via (cd "$WORK_DIR" && . "$SCRIPT"), 
# the current directory ($PWD) is already the decompiled APK folder.
DECOMPILED_DIR="$PWD"

# $P_DIR is inherited from apktool.sh and points exactly to your patch folder
PATCH_RES="$P_DIR/res"

# Apktool always uses the standard root res/ directory
TARGET_RES="$DECOMPILED_DIR/res"

echo "Applying Custom Logo resources..."

# If the target res directory exists, copy the files over
if [[ -d "$TARGET_RES" ]]; then
    
    # Ensure the source patch folder actually has a res directory before copying
    if [[ -d "$PATCH_RES" ]]; then
        cp -rf "$PATCH_RES/"* "$TARGET_RES/"
        echo "Logo files copied successfully to $TARGET_RES!"
    else
        echo "Warning: No res folder found in patch directory ($PATCH_RES)"
    fi
else
    echo "Error: No res directory found in $DECOMPILED_DIR"
fi
