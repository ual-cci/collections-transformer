# Collections Transformer

LLM-powered platform designed to assist users working with collections and datasets. This project is the preliminary design of a project that focuses on analysis and ML-powered inference in the GLAM sector. Code for the project "Transforming Collections" undertaken at UAL "Towards a National Collection (TaNC)"

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

Authentication uses Auth0. You can use an existing Auth0 Tenant. Create an .env file in the server folder with keys.

```
NEXT_PUBLIC_SERVER_URL = ""
AUTH0_SECRET = "{AUTH0 SECRET}"
AUTH0_ISSUER_BASE_URL = "{YOUR TENANT URL}"
AUTH0_CLIENT_ID = "{AUTH0 CLIENT ID}"
AUTH0_CLIENT_SECRET = "{AUTH0 CLIENT SECRET}"
AUTH0_DOMAIN = "{YOUR TENANT URL}"
```

Models used for inference are gpt4-o for OpenAI API. Alter the keys on the environment files respectively. For Azure the user might add Endpoints via Azure AI Studio. For HuggingFace (after repository permission) create an access token.


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

Previous repository: https://github.com/ual-cci/transforming-collections-ml-analyser/   

Final Report Transforming Collections: https://zenodo.org/records/14772312  

Project Media: https://www.arts.ac.uk/ual-decolonising-arts-institute/projects/transforming-collections
