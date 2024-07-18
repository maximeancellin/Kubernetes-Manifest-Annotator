import json
import argparse
from ruamel.yaml import YAML
import os

def load_openapi(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def get_description(schema, property_name):
    """Récupère la description d'une propriété à partir du schéma."""
    if 'properties' in schema and property_name in schema['properties']:
        return schema['properties'][property_name].get('description', '')
    return ''

def get_schema(schema, property_name, openapi):
    """Récupère le schéma pour une propriété, suivant les références si nécessaire."""
    if 'properties' in schema and property_name in schema['properties']:
        prop_schema = schema['properties'][property_name]
        if '$ref' in prop_schema:
            ref = prop_schema['$ref']
            ref_key = ref.split('/')[-1]
            return openapi['definitions'].get(ref_key, {})
        return prop_schema
    return {}

def annotate_manifest(manifest, schema, openapi):
    """Annoter le manifest Kubernetes avec des commentaires basés sur les descriptions OpenAPI."""
    for key, value in manifest.items():
        if key in schema.get('properties', {}):
            description = get_description(schema, key)
            if description:
                manifest.yaml_set_comment_before_after_key(key, before=description)
            prop_schema = get_schema(schema, key, openapi)
            if isinstance(value, dict):
                annotate_manifest(value, prop_schema, openapi)
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                for item in value:
                    annotate_manifest(item, prop_schema['items'], openapi)

def main():
    parser = argparse.ArgumentParser(description="Annotate Kubernetes manifests with OpenAPI descriptions.")
    parser.add_argument("manifest", help="Path to the Kubernetes manifest file")
    parser.add_argument("--openapi", default="openapi.json", help="Path to the OpenAPI JSON file (default: openapi.json)")
    parser.add_argument("--output", help="Path to the output file (default: annotated_<input_filename>)")

    args = parser.parse_args()

    openapi = load_openapi(args.openapi)

    yaml = YAML()
    yaml.preserve_quotes = True

    # Charger le manifest Kubernetes
    with open(args.manifest, 'r') as f:
        manifest = yaml.load(f)

    # Récupérer le schéma pour le type de ressource (par exemple, Deployment)
    resource_kind = manifest['kind']
    api_version = manifest['apiVersion'].split('/')[0]
    if api_version == 'apps':
        schema_key = f"io.k8s.api.apps.v1.{resource_kind}"
    else:
        schema_key = f"io.k8s.api.{api_version}.{resource_kind}"

    if schema_key in openapi['definitions']:
        schema = openapi['definitions'][schema_key]
        annotate_manifest(manifest, schema, openapi)
    else:
        print(f"Schema for {resource_kind} not found in OpenAPI definitions.")

    # Déterminer le nom du fichier de sortie
    output_file = args.output if args.output else 'annotated_' + os.path.basename(args.manifest)

    # Créer le dossier de sortie s'il n'existe pas
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Sauvegarder le manifest annoté dans le fichier de sortie
    with open(output_file, 'w') as f:
        yaml.dump(manifest, f)

    print(f"Annotated manifest saved to {output_file}")

if __name__ == '__main__':
    main()
