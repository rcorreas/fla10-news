#!/bin/bash
cd /Users/rcorreas/fla10_news
nohup python3 -m streamlit run app.py --server.port 8501 --server.headless true --browser.gatherUsageStats false > /tmp/streamlit.log 2>&1 &
echo "PID: $!"
echo "Acesse http://localhost:8501"
