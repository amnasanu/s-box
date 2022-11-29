[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/project/sbox
ExecStart=/home/ubuntu/project/sboxgit/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          code_keen.wsgi:application

[Install]
WantedBy=multi-user.target