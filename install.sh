mv data.py /usr/local/bin/system-data/main.py
touch /usr/local/bin/system-data
chmod +x /usr/local/bin/system-data
echo "python3 /usr/local/bin/system-data/main.py" > /usr/local/bin/system-data
echo "system-data" >> $HOME/.bashrc
echo "All done"
