# Modify and start the service immediately and enable it for future boots:
sudo nano /etc/systemd/system/FreedomMailing_setup.service
sudo systemctl enable --now FreedomMailing_setup.service

# Reload modified service
sudo systemctl daemon-reload
sudo systemctl restart FreedomMailing_setup.service
    -or-
sudo systemctl start FreedomMailing_setup.service


# Debug journal of service execution
sudo journalctl -u FreedomMailing_setup.service -b

# Pertinent env variables needed service execution
PYTHONPATH=.:src
PATH=/home/operations/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin

    -but-

# Location of uv (all that is needed for service execution)
/home/operations/.local/bin/uv
