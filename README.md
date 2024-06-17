## Create a virtual environment

- Use `python3 -m venv env` to create a virtual environment in the directory of your choice.

- You can use `source/bin/activate` to activate the virtual environment.

## Clone the repository

- Clone the repository in the above specified directory: `git clone https://github.com/adars124/LLM-Basic.git`

## Install the requirements

- Ensure the activation of virtual environment and install the requirements by using: `pip install -r requirements.txt`

**Note**: You should be in the directory of the cloned repository otherwise the requirements won't be installed.

## Get the token

- Go to this link and [get the token](https://makersuite.google.com/app/apikey)

- And follow the instructions to get the `GOOGLE_API_TOKEN`.

## Configure the project

- Create a `.env` file inside the main directory i.e. `LLM-Basic/.env`

- Add `GOOGLE_API_TOKEN=<your_token_here>` in the `.env` file.

## Start the project

- If everything specified above is successfully installed, you are good to go.

- Go inside the app directory: `cd app/`

- Run the project in a terminla using: `streamlit run main.py`

## Feedback

- Let me know if any issue persists. Thank you!

