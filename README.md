## Linux production setup:

1. User account should be __operations__ for easy config settings
2. Install __pdftotxt__ : ```sudo apt install poppler-utils```
3. Install GitHub utility : ```sudo apt install gh```
4. Clone FreedomMailing from GitHub ```gh repo clone FreedomMailingIT/FreedomMailing```
5. Rename the created FreedomMailing program directory to FreedomMailing-v2:<br>```mv FreedomMailing FreedomMailing-v2```
6. Install __uv__ program: ```sudo pip3.x install uv```
7. Create virtual environment: ```uv venv --python 3.x```
8. Install site_packages in virtual environment: ```uv pip install -r pyproject.toml```
9. Copy credential files into ```.venv/lib/python3.x/site-packages/```
10. Activate virtual environment: ```source .venv/bin/activate```
11. Symbolicly link __py__ to the system python executable in __.venv/bin__ :<br>```cp .venv/bin/python .venv/bin/py```
12. If not already created, install __DropBox__ creating Dropbox dir with FreedomMailing sub-dir:<br>```mkdir ~/Dropbox/FreedomMailing```
13. Create __.job_execution.log__ files in __Dropbox__ and __test/data__ directories, then make them read/write
```
    touch ~/Dropbox/FreedomMailingData/.job_execution.log
	chmod 666 ~/Dropbox/FreedomMailingData/.job_execution.log
	touch ~/FreedomMailing-v2/tests/data/.job_execution.log
	chmod 666 ~/FreedomMailing-v2/tests/data/.job_execution.log
```

## Convenience:
- alias __venv__ :<br>```echo "alias venv='source .venv/bin/activate' && export PYTHONPATH=$PWD" >> ~/.bash_aliases```
- alias __xenv__ : ```echo "alias xenv='deactivate'" >> ~/.bash_aliases```
- alias __uvr__ : ```echo "alias uvr='uv run'" >> ~/.bashrc && source ~/.bashrc```

- alias __test_setup__ : ```echo "alias test_setup='export FM_FILES=tests'" >> ~/.bash_aliases```
- alias __test_teardown__ : ```echo "alias test_teardown='unset FM_FILES'" >> ~/.bash_aliases```

then ```source ~/.bashrc``` to reload bash to access the alias in current terminal session<br>
bash will automatically use the alias on each terminal session restart


## If testing:
- to setup:  ```export FM_FILES=tests```  _OR_  ```. scripts/test_setup.sh```
- to teardowm:  ```unset FM_FILES```  _OR_  ```. scripts/test_teardown.sh```
