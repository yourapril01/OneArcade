#TEE have things of bootloader
#We are building using latest firmware (latest binary and one ui 8)
# Latest unlockeable BL is based on binary I (one ui 7) so, we can use OneUI 8 vendor with vendor/tee folder from OneUI 7 (binary I)
# Requires one ui 7 libsec-ril.so to have working ril
REMOVE "vendor" "tee"

# Enable RAW Support
# Before: [cbz r0, #0x15612a]
# After: [nop]
HEX_PATCH "$WORKSPACE/vendor/lib/libexynoscamera3.so" "f0b12649" "00bf2649"

# Before: [tbz w8, #0, 0x59d448]
# After: [nop]
HEX_PATCH "$WORKSPACE/vendor/lib64/libexynoscamera3.so" "88020036610d00f0" "1f2003d5610d00f0"
