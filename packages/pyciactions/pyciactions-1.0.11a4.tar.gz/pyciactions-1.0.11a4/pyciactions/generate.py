import yaml
from datetime import datetime
from . import IWorkflow


def generate(workflow: IWorkflow, filename: str):
    workflow_dict = workflow.to_dict()
    yaml_string = yaml.dump(workflow_dict, sort_keys=False)

    print(
        """
echo -e "# Generated automatically on {datetime.now().isoformat()} using pyactions

cat <<EOF > {filename}
{yaml_string}
EOF
"""
    )
