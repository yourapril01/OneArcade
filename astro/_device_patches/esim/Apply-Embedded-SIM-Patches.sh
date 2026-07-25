
if GET_FEATURE DEVICE_HAVE_ESIM_SUPPORT == true; then
    LOG_BEGIN "Device supports eSIM, adding blobs"
    
    ADD_FROM_FW "pa3q" "system" "priv-app/EsimKeyString"
    ADD_FROM_FW "pa3q" "system" "priv-app/EuiccService"

    ADD_FROM_FW "pa3q" "system" "etc/permissions/privapp-permissions-com.samsung.android.app.esimkeystring.xml"
    ADD_FROM_FW "pa3q" "system" "etc/permissions/privapp-permissions-com.samsung.euicc.xml"
    ADD_FROM_FW "pa3q" "system" "etc/sysconfig/preinstalled-packages-com.samsung.android.app.esimkeystring.xml"
    ADD_FROM_FW "pa3q" "system" "etc/sysconfig/preinstalled-packages-com.samsung.euicc.xml"

    FF_IF_DIFF "stock" "COMMON_CONFIG_EMBEDDED_SIM_SLOTSWITCH"

        LOG_END "eSIM blobs added"
        
    else
    LOG_BEGIN "Device doesnt supports eSIM, proceed to nuke eSIM blobs"
    
    SILENT REMOVE "system" "etc/permissions/privapp-permissions-com.samsung.android.app.esimkeystring.xml"
    SILENT REMOVE "system" "etc/permissions/privapp-permissions-com.samsung.android.app.telephonyui.esimclient.xml"
    SILENT REMOVE "system" "etc/permissions/privapp-permissions-com.samsung.euicc.xml"
    SILENT REMOVE "system" "etc/permissions/privapp-permissions-com.samsung.euicc.mep.xml"
    SILENT REMOVE "system" "etc/sysconfig/preinstalled-packages-com.samsung.android.app.esimkeystring.xml"
    SILENT REMOVE "system" "etc/sysconfig/preinstalled-packages-com.samsung.euicc.xml"
    SILENT REMOVE "system" "priv-app/EsimKeyString"
    SILENT REMOVE "system" "priv-app/EuiccService"
    SILENT REMOVE "system" "priv-app/EsimClient"
    
        LOG_END "No eSIM blobs left, success nuked eSIM support"

fi
