
## Install dependencies:

```
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
```
Set the OPENAI_API_KEY value in .env to your own key

## Build knowledge base:

Put your PDF files in pfd/

```
  python knowledge_base.py
```

## Run:

```
  streamlit run app.py
```
