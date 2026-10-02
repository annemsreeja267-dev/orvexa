# Testing and Running the Enterprise Knowledge Assistant

## 1. Create and activate the virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation for this session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## 2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Verify Python source

```powershell
python -m compileall api src scripts tests
```

## 4. Run unit tests

```powershell
python -m unittest discover -s tests
```

## 5. Install/test Ollama

Install Ollama separately, then:

```powershell
ollama pull qwen2.5:7b
ollama run qwen2.5:7b
```

Type `/bye` to exit the model.

## 6. Build/test the RAG index

```powershell
python scripts/scan_documents.py
python scripts/test_pipeline.py
python scripts/show_registry_changes.py
```

The repository includes small demo documents under `data/WorldBank` so the project can be tested immediately.

## 7. Start the API

Terminal 1:

```powershell
python -m uvicorn api.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

Test:

- `GET /health`
- `GET /domains`
- `POST /login`
- `POST /query`

## 8. Start the Streamlit UI

Terminal 2:

```powershell
.\venv\Scripts\Activate.ps1
streamlit run streamlit_app.py
```

Open `http://localhost:8501`.

## Demo accounts

- `admin1 / admin123` — all documents
- `gov_emp_1 / gov123` — public + internal `govt_policy`
- `hr_emp_1 / hr123` — public + internal `hr1`
- `client1 / client123` — public only

## RBAC checks

1. Log in as `admin1` and query confidential government policy.
2. Log in as `gov_emp_1` and verify internal government policy is accessible.
3. Log in as `gov_emp_1` and verify confidential government policy is not accessible.
4. Log in as `client1` and verify only public information is returned.

The vector store and document registry are generated at runtime and are intentionally not included in the ZIP.
