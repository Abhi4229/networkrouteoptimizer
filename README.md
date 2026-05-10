# 1. install dependencies
pip install -r requirements.txt

# 2. start the server
uvicorn app.main:app --reload

# 3. open the docs
# go to http://127.0.0.1:8000/docs in your browser
