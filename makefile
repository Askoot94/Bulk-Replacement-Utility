PYTHON = ${command:python.interpreterPath}

run: 
	$(PYTHON)
	pyinstaller main.spec --noconfirm