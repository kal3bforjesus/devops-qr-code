# ☁️ Cloud-Native QR Code Generator

A production-grade, fully automated DevOps project demonstrating a secure CI/CD and GitOps pipeline built on Microsoft Azure. This application generates QR codes and stores them in the cloud, but the true focus of this project is the **engineering, automation, and security** behind the deployment.

## 🏗️ Architecture & Workflow

This project utilizes a modern GitOps workflow to ensure zero-downtime, secure, and automated deployments:

1. **Code Push:** A developer pushes code to the `main` branch on GitHub.
2. **CI/CD & DevSecOps:** GitHub Actions automatically triggers a pipeline that builds the Docker images and runs **Trivy** to scan for critical security vulnerabilities.
3. **Container Registry:** Once the images pass the security scan, they are pushed to a private **Azure Container Registry (ACR)**.
4. **Manifest Update:** The pipeline automatically updates the Kubernetes YAML manifests with the new image tags and commits them back to the repository.
5. **GitOps Sync:** **ArgoCD** detects the manifest changes in the `k8s/` directory and automatically synchronizes the **Azure Kubernetes Service (AKS)** cluster to the new state.
6. **Internal Routing:** The Next.js frontend receives user input and proxies the request internally to the FastAPI backend using Kubernetes DNS. The backend is completely hidden from the public internet.
7. **Cloud Storage:** The backend generates the QR code and securely uploads it to **Azure Blob Storage**.

## 🛡️ Key DevOps Best Practices Implemented

* **Zero-Trust Networking:** The backend API uses a `ClusterIP` (no public internet exposure). The Next.js frontend acts as a Backend-for-Frontend (BFF) proxy, eliminating CORS issues, hardcoded IPs, and external attack vectors.
* **Infrastructure as Code (IaC):** The entire Azure environment (AKS, ACR, Blob Storage, Resource Groups) is provisioned and managed via Terraform.
* **GitOps:** The cluster state is entirely declarative and version-controlled. Manual `kubectl apply` commands are avoided in production.
* **Shift-Left Security:** Trivy scans all Docker images for HIGH and CRITICAL vulnerabilities *before* they are allowed to reach the container registry.
* **Secret Management:** Sensitive credentials (Azure keys, GitHub tokens) are managed via GitHub Secrets and Kubernetes Secrets, and are never stored in plain text in the repository.
* **Observability:** Utilized the official Kubernetes Dashboard for real-time visual monitoring of pod health, resource metrics, and log aggregation.
* **Cost Optimization:** The entire environment is ephemeral. It can be spun up or torn down in minutes using `terraform apply` and `terraform destroy` to manage cloud spend.

## 🛠️ Technology Stack

| Category | Technologies |
| :--- | :--- |
| **Cloud Provider** | Microsoft Azure |
| **Infrastructure as Code** | Terraform |
| **Container Orchestration** | Kubernetes (AKS) |
| **Container Registry** | Azure Container Registry (ACR) |
| **GitOps** | ArgoCD |
| **CI/CD & Security** | GitHub Actions, Trivy |
| **Observability** | Kubernetes Dashboard |
| **Frontend** | Next.js (React) |
| **Backend** | Python (FastAPI) |
| **Storage** | Azure Blob Storage |
| **Containerization** | Docker |

##  Project Structure

```text
devops-qr-code/
├── .github/workflows/      # GitHub Actions CI/CD & DevSecOps pipeline
├── api/                    # FastAPI Backend application
├── front-end-nextjs/       # Next.js Frontend application
├── k8s/                    # Kubernetes manifests (Deployments, Services)
├── terraform/              # Terraform Infrastructure as Code (IaC)
└── README.md