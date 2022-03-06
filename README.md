NOTE: Archived.  Since this was written, many releases of Elastic have happened.  With them is included authorization and helm scripts for installing on Kubernetes, which was not available when this was written.  The information in this guide is outdated.

# Elasticsearch-Kubed

The purpose of this project is to provide starter files for deploying a high performance Elasticsearch cluster on Kubernetes running on either GCP or AWS.  

The configuration files will generally be targeted at deployments with at least two nodes, four or more CPUs, and fifteen or more GBs of memory.  However, for the purposes of testing the components with less hardware available, there is also a profile that will run on a single node Kubernetes cluster which you can easily set up with minikube.  If you really wanted to run Elasticsearch on a single computer, you would just use one container to do it.  Our Elasticsearch cluster will have three master nodes, and multiple data and ingest nodes, which you can adjust the number of to meet your hardware requirements.

## Related Blog Post

There is a blog post that walks people through setting up an ES cluster using this repo.  You can find that post through the link below:

[High Performance ELK with Kubernetes](https://engineering.udacity.com/high-performance-elk-with-kubernetes-part-1-1d09f41a4ce2)

Note that the blog post was originally written for ES 6.3, while this repo has been updated several times to use newer versions of the Elastic Stack.  I don't think there is anything in the blog post that needs to be updated as a result of updates.  However, if you come across something confusing in the blog post, perhaps as a result of the updates to this repo, please open a GitHub issue to let me know about it.

### minikube

To test the configuration on MaxOS X, `minikube` can be installed to launch a local one node Kubernetes cluster.  When starting minikube, increase the default machine size:

`minikube start --memory 8192 --disk-size 50g --cpus 4`
