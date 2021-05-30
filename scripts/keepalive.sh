pgrep -x python3 >/dev/null && echo "Process found" &&  exit || echo "Process not found" && sudo nohup python3 /home/ubuntu/TwitterStreamerTemplate/code/scrap_tweet.py
