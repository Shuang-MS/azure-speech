#!/bin/bash

source .venv/bin/activate && python3 -m streamlit run app.py --server.port 8000 --server.address 0.0.0.0