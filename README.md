# Elasticsearch-Kubed

The purpose of this project is to provide starter files for deploying a high performance Elasticsearch cluster on Kubernetes running on either GCP or AWS.  

The configuration files will generally be targeted at deployments with at least two nodes, four or more CPUs, and fifteen or more GBs of memory.  However, for the purposes of testing the components with less hardware available, there is also a profile that will run on a single node Kubernetes cluster which you can easily set up with minikube.  If you really wanted to run Elasticsearch on a single computer, you would just use one container to do it.  Our Elasticsearch cluster will have three master nodes, and multiple data and ingest nodes, which you can adjust the number of to meet your hardware requirements.

## Related Blog Post

There is a blog post that walks people through setting up an ES cluster using this repo.  You can find that post through the link below:

[High Performance ELK with Kubernetes](https://engineering.udacity.com/high-performance-elk-with-kubernetes-part-1-1d09f41a4ce2)

### minikube

To test the configuration on MaxOS X, `minikube` can be installed to launch a local one node Kubernetes cluster.  When starting minikube, increase the default machine size:

`minikube start --memory 8192 --disk-size 50g --cpus 4`
