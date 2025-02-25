import os
class Config:
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')
    base_url = os.environ.get('URL').strip()
    refresh_interval = int(os.environ.get('REFRESH_INTERVAL'))