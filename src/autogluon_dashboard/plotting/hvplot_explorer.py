import io
import os

import hvplot
import pandas as pd
import panel as pn

from autogluon_dashboard.scripts.constants.aws_s3_constants import (
    AGG_FRAMEWORK_DEFAULT_CSV_PATH,
    PER_DATASET_DEFAULT_CSV_PATH,
)
from autogluon_dashboard.scripts.widget import Widget

dataset_file = os.environ.get("PER_DATASET_S3_PATH", PER_DATASET_DEFAULT_CSV_PATH)
aggregated_file = os.environ.get("AGG_DATASET_S3_PATH", AGG_FRAMEWORK_DEFAULT_CSV_PATH)
upload = Widget("upload", name="Upload file").create_widget()
select = Widget(
    "select",
    options={
        "Dataset File": dataset_file,
        "Aggregated File": aggregated_file,
    },
).create_widget()


def add_data(event):
    b = io.BytesIO()
    upload.save(b)
    b.seek(0)
    name = ".".join(upload.filename.split(".")[:-1])
    select.options[name] = b
    select.param.trigger("options")
    select.value = b


upload.param.watch(add_data, "filename")


def explore(csv):
    df = pd.read_csv(csv)
    explorer = hvplot.explorer(df)
    return pn.Column(
        explorer,
    )


widgets = pn.Column(
    "Select an existing dataset or upload one of your own CSV files and start exploring your data.",
    pn.Row(
        select,
        upload,
    ),
)

output = pn.panel(pn.bind(explore, select))
