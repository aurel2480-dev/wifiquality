import time
import subprocess
import os

def get_wifi_info():
    try:
        # Exécute la commande netsh pour récupérer l'état du Wi-Fi
        output = subprocess.check_output(
            ["netsh", "wlan", "show", "interfaces"], 
            encoding="cp850", 
            errors="ignore"
        )
        
        info = {}
        for line in output.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                info[key.strip()] = value.strip()
                
        # Extraction des métriques clés
        ssid = info.get("SSID", "Non connecté")
        signal = info.get("Signal", "0%").replace("%", "")
        rx_rate = info.get("Vitesse de réception (Mbit/s)", info.get("Receive rate (Mbps)", "N/A"))
        tx_rate = info.get("Vitesse de transmission (Mbit/s)", info.get("Transmit rate (Mbps)", "N/A"))
        channel = info.get("Canal", info.get("Channel", "N/A"))
        
        return {
            "ssid": ssid,
            "signal": int(signal) if signal.isdigit() else 0,
            "rx_rate": rx_rate,
            "tx_rate": tx_rate,
            "channel": channel
        }
    except Exception:
        return None

def quality_label(signal):
    if signal >= 80:
        return "Excellente"
    elif signal >= 60:
        return "Bonne"
    elif signal >= 40:
        return "Moyenne"
    elif signal >= 20:
        return "Faible"
    else:
        return "Très instable / Critique"

def main():
    # Activation du support des séquences ANSI sous Windows CMD si nécessaire
    if os.name == 'nt':
        os.system('')

    print("=== Surveillance Wi-Fi en temps réel (Ctrl+C pour quitter) ===\n")
    
    try:
        while True:
            wifi = get_wifi_info()
            
            # Séquence ANSI pour repositionner le curseur en haut à gauche et effacer l'écran
            # Évite d'appeler 'cls' ou 'clear' et résout l'erreur 'unknown terminal type'
            print("\033[H\033[2J", end="")
            
            print("=== Surveillance Wi-Fi en temps réel (Ctrl+C pour quitter) ===\n")

            if wifi and wifi["ssid"] != "Non connecté":
                qualite = quality_label(wifi["signal"])
                bars = "█" * (wifi["signal"] // 10) + "░" * (10 - (wifi["signal"] // 10))
                
                print(f"Réseau SSID : {wifi['ssid']}")
                print(f"Canal       : {wifi['channel']}")
                print(f"Signal      : [{bars}] {wifi['signal']}% ({qualite})")
                print(f"Débit TX/RX : {wifi['tx_rate']} / {wifi['rx_rate']}")
            else:
                print("Aucune connexion Wi-Fi active détectée.")
                
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nSurveillance arrêtée.")

if __name__ == "__main__":
    main()
