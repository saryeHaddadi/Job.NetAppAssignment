venv_dir = venv
python_executable = python3.10

.PHONY: install_requirements serve test

# Create virtualenv if does not exist
${venv_dir}:
	@echo "Creating venv at ${venv_dir}..."
	${python_executable} -m venv ${venv_dir}

install_requirements: ${venv_dir}
	@echo "Install requirements..."
	${venv_dir}/bin/pip install -r requirements.txt

serve: install_requirements
	@echo "Run Flask application locally..."
	export FLASK_ENV=development
	${venv_dir}/bin/${python_executable} main.py

test: install_requirements
	${venv_dir}/bin/${python_executable} -m pytest
