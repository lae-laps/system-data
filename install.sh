# Este script instala automáticamente el programa system-wide como utilidad a demás de incluirlo en el ~/.bashrc

if [ "$EUID" -ne 0 ]; then
    echo "[*] ~ Please run as root"
    exit
fi

mv data.py /usr/local/bin/system-data/main.py
touch /usr/local/bin/system-data
chmod +x /usr/local/bin/system-data
echo "python3 /usr/local/bin/system-data/main.py" > /usr/local/bin/system-data
echo "system-data" >> $HOME/.bashrc
echo "All done"
