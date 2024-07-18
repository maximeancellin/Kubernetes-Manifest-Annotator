# Kubernetes Manifest Annotator

This Python script annotates Kubernetes manifest files using descriptions provided by OpenAPI references.

## Features

- **Automatic Annotation:** Adds comments in Kubernetes manifest YAML files based on OpenAPI descriptions.
- **Handling of Subresources:** Recursive tracking of OpenAPI references to annotate subresources such as container specifications.
- **Customizable:** Ability to specify the output file and automatic creation of the output directory if necessary.

## Requirements

- Python 3.x
- Python library: `ruamel.yaml` (automatically installed via `requirements.txt`)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/kubernetes-manifest-annotator.git
   cd kubernetes-manifest-annotator
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

First generate the `openapi.json` file:
```bash
kubectl get --raw /openapi/v2 > openapi.json
```

To annotate a Kubernetes manifest file, use the following command:

```bash
python annotate_manifests.py path/to/deployment.yaml [--openapi path/to/openapi.json] [--output path/to/output.yaml]
```

- `path/to/deployment.yaml`: Path to the Kubernetes manifest file you want to annotate.
- `--openapi path/to/openapi.json` (optional): Path to the OpenAPI JSON file containing API descriptions.
- `--output path/to/output.yaml` (optional): Path to the annotated output file. If not specified, the script will use `annotated_<original_filename>.yaml`.

Example:

```bash
python annotate_manifests.py examples/deployment.yaml --openapi openapi_definitions/kubernetes.json --output examples/output/deployment_annotated.yaml
```

## Contributing

Contributions are welcome! For bugs, suggestions for improvement, or new features, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
