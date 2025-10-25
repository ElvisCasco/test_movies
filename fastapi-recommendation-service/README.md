# FastAPI Recommendation Service

This project is a FastAPI application that implements a recommendation engine using non-negative matrix factorization (NMF) from the sklearn library. The service allows users to train a recommendation model and stores each version of the model without overwriting previous versions.

## Project Structure

```
fastapi-recommendation-service
├── src
│   ├── main.py                  # Entry point of the FastAPI application
│   ├── api
│   │   └── v1
│   │       └── recommendation.py # API endpoint for the recommendation engine
│   ├── services
│   │   └── recommender.py       # Logic for training the recommendation model
│   ├── schemas
│   │   └── recommendation.py     # Data schemas for request and response validation
│   ├── core
│   │   └── config.py            # Configuration settings for the application
│   ├── db
│   │   └── storage.py           # Handles storage of trained models
│   └── utils
│       └── versioning.py        # Utility functions for model versioning
├── artifacts
│   └── models                   # Directory for storing trained models
├── tests
│   └── test_recommender.py      # Unit tests for the recommender service
├── requirements.txt             # Project dependencies
├── Dockerfile                   # Instructions for building a Docker image
├── .gitignore                   # Files and directories to ignore by Git
└── README.md                    # Documentation for the project
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd fastapi-recommendation-service
pip install -r requirements.txt
```

## Usage

To run the FastAPI application, execute the following command:

```bash
uvicorn src.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## API Endpoints

### Train Recommendation Model

- **Endpoint:** `POST /api/rest/v1/recommendation-engine`
- **Description:** Trains a recommendation model using non-negative matrix factorization and stores the model version.

### Documentation

Interactive API documentation can be accessed at `http://127.0.0.1:8000/docs`.

## Testing

To run the unit tests for the recommender service, use the following command:

```bash
pytest tests/test_recommender.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.