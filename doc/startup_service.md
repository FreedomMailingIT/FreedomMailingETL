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
Environment="PYTHONPATH=.:src"
Environment="PATH=/home/operations/.local/bin:/home/operations/FreedomMailingETL/.env/bin:/usr/bin:/bin"
