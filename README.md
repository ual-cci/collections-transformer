# Collections Transformer

Code for the project "Transforming Collections" undertaken at UAL "Towards a National Collection (TaNC)". LLM-powered application designed to assist users working with collections and datasets. This project is the preliminary design for a platform that focuses on usability and inclusion in the GLAM sector.

Version of the website is currently active at https://collectionstransforming.com/


## Application Setup

```bash
# Start by installing MongoDB, nvm, Miniconda
# Create conda environment
conda env create --name collections_transformer --file=environment.yml
conda activate collections_transformer

# Setup Python environment
cd server/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run backend and frontend
cd ..
screen -S backend -d -m ./run_backend.sh
screen -S frontend -d -m ./run_frontend_dev.sh
```

See server/requirements.txt and client/package.json for a full set of requirements.


## Supporting services & APIs

Authentication uses Auth0. You can use an existing Auth0 Tenant. (1) Create an account on Auth0 (https://auth0.com/signup), (2) Create a new tenant, (3) Create a new application, (4) Add relevant URLs to the application settings on Auth0, (5) Add your application's credentials to the .env files in the client folder.

You can choose between different AI model sources to run the app. Create an .env file in the server folder and follow env.template.

Models used for inference are gpt4-o for OpenAI API and meta-llama/Llama-3.2-11B-Vision for HuggingFace. Alter the keys on the environment files respectively. For Azure the user might need to add Endpoints via Azure AI Studio. For HuggingFace (after repository permission) create an access token.



## Local Deployment

(1) Navigate to client folder  
(2) Activate conda environment `conda activate collections_transformer`  
(3) Add .env.local file with relevant credentials (eg. Auth0). See env.local.template for reference.  

* .env.local (For sensitive data such as API keys.)
* .env.development (For credentials specific to local development.)
* .env.production (For credentials specific to your production server.)
* .env.azure-dev (available via `npm run dev-azure`)
* .env.azure-prod (available via `npm run build-azure`, `npm run start-azure`)
* .env.openai-dev (available via `npm run dev-openai`)
* .env.openai-prod (available via `npm run build-openai`, `npm run start-openai`)


### Server Setup
1. Navigate to server folder
2. Activate virtual environment: `source venv/bin/activate`
3. Run Flask app: `python3 app.py`\
\
Options (you can change the defaults in server/app.py):
* -m or --model : Sets the model source (default: "openai"). Choose between "azure" or "openai" or "huggingface" depending on what you've set up.
* -p or --port : Sets the port (eg. 8000, 8080)
* -r or --reload : Sets the server to reload automatically when files are changed. (true or false, default is true)

4. Check http://localhost:8080

## Production Deployment
The following instructions are based on our set up - running two versions of the app from the same codebase

* The OpenAI-driven app will be available at port 3000 and supported by the API service at port 8080
* The Azure-driven app will be available at port 3005 and supported by the API service at port 8085


#### For OpenAI:
```
gunicorn -b 0.0.0.0:8080 -k gevent --workers=12 'app:app(model="openai")' --timeout 600 --preload
```

#### For Azure:
```
gunicorn -b 0.0.0.0:8085 -k gevent --workers=12 'app:app(model="azure", port=8085)' --timeout 600 --preload
```

## Useful MongoDB commands

#### Start Mongosh
```
$ mongosh
$ use my_database
$ show collections

# Inspect dataset by name
$ db.dataset.find({"name": "set_1"})

# Count datasets
$ db.dataset.countDocuments()

# Make dataset public
$ db.dataset.updateOne({name:DATASET_NAME},{$set:{"users":[]}})
$ db.dataset.updateOne({name:DATASET_NAME}, {$unset:{"owner":1}})

# Share dataset
$ db.dataset.updateOne({name:DATASET_NAME},{$set:{"users":[AUTH0_ID_1, AUTH0_ID_2]}})
```



## References

(1) Previous development and version control: https://github.com/ual-cci/transforming-collections-ml-analyser/  
(2) Final Report - Transforming Collections: Reimagining Art, Nation and Heritage: https://zenodo.org/records/14772312  
(3) Project's reference: https://www.arts.ac.uk/ual-decolonising-arts-institute/projects/transforming-collections
