#!/bin/bash

LAPTOP_DISPLAY="eDP-1"
LOG_FILE="/tmp/hypr-lid-switch.log"

log_message() {
    echo "$(date): $1" >> "$LOG_FILE"
}

get_lid_state() {
    STATE_FILE=$(find /proc/acpi/button/lid/*/state | head -n 1)

    if [[ -n "$STATE_FILE" ]]; then  # The STATE_FILE is non-zero
        cat "$STATE_FILE" 2>/dev/null | grep -q "closed" && echo "closed" || echo "open"
    else
        echo "STATE_FILE_NOT_FOUND"
    fi
}

get_external_display() {
    # Dynamically get the external display name
    hyprctl monitors | grep -E "^Monitor (DP|HDMI|USB-C)" | grep -v "$LAPTOP_DISPLAY" | head -1 | cut -d' ' -f2
}

handle_lid_close() {
    log_message "Lid closed - checking for external monitor"
    
    CURRENT_EXTERNAL=$(get_external_display)
    if [[ -n "$CURRENT_EXTERNAL" ]]; then
        log_message "External monitor detected: $CURRENT_EXTERNAL, disabling laptop display"
        hyprctl keyword monitor "$LAPTOP_DISPLAY,disable" || log_message "Failed to disable laptop display"
        log_message "Laptop display disabled, $CURRENT_EXTERNAL remains as primary"
    else
        log_message "No external monitor detected, hibernating system"
        systemctl hibernate
    fi
}

handle_lid_open() {
    log_message "Lid opened - re-enabling laptop display"
    
    CURRENT_EXTERNAL=$(get_external_display)
    if [[ -n "$CURRENT_EXTERNAL" ]]; then
        log_message "External monitor detected: $CURRENT_EXTERNAL, setting up dual monitor configuration"
        hyprctl keyword monitor "$LAPTOP_DISPLAY" || log_message "Failed to enable laptop display"
        log_message "Dual monitor setup restored with $CURRENT_EXTERNAL"
    else
        log_message "No external monitor, enabling laptop display only"
        hyprctl keyword monitor "$LAPTOP_DISPLAY" || log_message "Failed to enable laptop display"
    fi
}

case "$1" in
    "close")
        handle_lid_close
        ;;
    "open")
        handle_lid_open
        ;;
    *)
        lid_state=$(get_lid_state)
        log_message "Auto-detecting lid state: $lid_state"
        
        if [[ "$lid_state" == "closed" ]]; then
            handle_lid_close
        else
            handle_lid_open
        fi
        ;;
esac
