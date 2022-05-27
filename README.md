# Anyway ETL

This project includes the following components:

* anyway-etl: A Python library and CLI which handles ETL processing tasks
* airflow: An airflow server which executes and manages the processing tasks

See the Anyway Docker docs for the easiest method to use and develop tasks.

For more advanced documentation see the [docs](docs) directory.

## Continuous Deployment

* Every push to `main` branch causes deployment to the Kubernetes cluster's `anyway-dev` environment
    * Except for changes to the `anyway` dependency, which is picked up automatically
      by the Airflow server and don't require a deployment
* Every [release](https://github.com/hasadna/anyway-etl/releases) causes deployment 
  to the Kubernetes cluster's `anyway` environment (the production environment)

## Testing on dev environment before merging

To test changes on dev environment before merging them to main branch - 
edit the `airflow-scheduler` deployment on `anyway-dev` namespace and set
`ANYWAY_ETL_BRANCH` env var to the name of the branch with changes you want
to test. Once testing is done, revert back to `main`.
