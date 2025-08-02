# backend

The backend of NumRacer is built using Python, FastAPI, and PostgreSQL.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/achen318/num-racer.git
```

2. Change directory into the backend folder:

```bash
cd num-racer/backend
```

3. Create a virtual environment and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Upgrade `pip` and install dependencies:

```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run

To run the FastAPI server in development mode, run the following command in the `backend` directory:

```bash
fastapi dev main.py
```

For production mode, run the following command:

```bash
fastapi run main.py
```
