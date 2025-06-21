
# Step 1 : Set up VM 
1. Create a new VM 
python -m venv .venv

2. Windows PowerShell: (activate VM)
.venv\Scripts\Activate.ps1

3. Install dependencies
pip install -r requirements.txt

4. Run adk 
type : "adk" in terminal


# Step 2: Set up google API 
1. Create an account in Google Cloud https://cloud.google.com/?hl=en
2. Create a new project
3. Go to https://aistudio.google.com/apikey
4. Create an API key
5. Assign key to the project
6. Ensure the Google API Key is included in all .env files

