import yaml
from datetime import datetime
from . import IWorkflow


def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, str_presenter)

yaml.representer.SafeRepresenter.add_representer(str, str_presenter)


def generate(workflow: IWorkflow, filename: str):
    workflow_dict = workflow.to_dict()
    yaml_string = yaml.dump(workflow_dict, sort_keys=False)
    print(
        f"""
echo -e '# Generated automatically on {datetime.now().isoformat()} using pyactions'

cat <<'EOF' > {filename}
{yaml_string}
EOF
"""
    )
