from datetime import datetime
from . import IWorkflow
import ruamel.yaml


def generate(workflow: IWorkflow, filename: str):
    workflow_dict = workflow.to_dict()
    yaml = ruamel.yaml.YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml_string = yaml.dump(workflow_dict, sort_keys=False)

    print(
        f"""
echo -e "# Generated automatically on {datetime.now().isoformat()} using pyactions

cat <<EOF > {filename}
{yaml_string}
EOF
"""
    )
