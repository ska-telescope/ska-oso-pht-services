.venv\Scripts\isort --line-length 88 src/ tests/
.venv\Scripts\black --line-length 88 --extend-exclude "(src/ska_oso_pht_services/generated|src/ska_oso_pht_services/openapi/__submodules__)" src/ tests/
.venv\Scripts\flake8 --max-line-length 88 src/ tests/
.venv\Scripts\pylint --max-line-length 88 src/ tests/