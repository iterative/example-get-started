# DVC Get Started

This is an auto-generated repository for use in https://dvc.org/doc/get-started.
Please report any issues in its source project,
[example-repos-dev](https://github.com/iterative/example-repos-dev).

![](https://dvc.org/static/img/example-flow-2x.png)

_Get Started_ is a step-by-step introduction into basic DVC concepts. It doesn't
go into details much, but provides links and expandable sections to learn more.

> Note that this project
[imports](https://dvc.org/doc/commands-reference/import) a dataset from
https://github.com/iterative/dataset-registry.

The idea of the project is a simplified version of the
[Tutorial](https://dvc.org/doc/tutorial). It explores the natural language
processing (NLP) problem of predicting tags for a given StackOverflow question.
For example, we want one classifier which can predict a post that is about the
Python language by tagging it `python`.

## Installation

Start by cloning the project:

```console
$ git clone https://github.com/iterative/example-get-started
$ cd example-get-started
```

Now let's install the requirements. But before we do that, we **strongly**
recommend creating a virtual environment with a tool such as
[virtualenv](https://virtualenv.pypa.io/en/stable/):

```console
$ virtualenv -p python3 .env
$ source .env/bin/activate
$ pip install -r src/requirements.txt
```

This DVC project comes with a preconfigured DVC
[remote storage](https://dvc.org/doc/commands-reference/remote) that holds raw
data (input), intermediate, and final results that are produced. This is a
read-only HTTP remote.

```console
$ dvc remote list
storage https://remote.dvc.org/get-started
```

You can run [`dvc pull`](https://man.dvc.org/pull) to download the data:

```console
$ dvc pull
```

## Running in your environment

Run [`dvc repro`](https://man.dvc.org/repro) to reproduce the
[pipeline](https://dvc.org/doc/commands-reference/pipeline):

```console
$ dvc repro evaluate.dvc
```

> `dvc repro` requires a target [stage file](https://man.dvc.org/run)
> ([DVC-file](https://dvc.org/doc/user-guide/dvc-file-format)) to reconstruct
> and regenerate a pipeline. In this case we use `evaluate.dvc`, the last stage
> in this project's pipeline.

If you'd like to test commands like [`dvc push`](https://man.dvc.org/push),
that require write access to the remote storage, the easiest way would be to set
up a "local remote" on your file system:

> This kind of remote is located in the local file system, but is external to
> the DVC project.

```console
$ mkdir -P /tmp/dvc-storage
$ dvc remote add local /tmp/dvc-storage
```

You should now be able to run:

```console
$ dvc push -r local
```

## Existing stages

This project with the help of the Git tags reflects the sequence of actions that
are run in the DVC [get started](https://dvc.org/doc/get-started) guide. Feel
free to checkout one of them and play with the DVC commands having the
playground ready.

- `0-empty`: Empty Git repository initialized.
- `1-initialize`: DVC has been initialized. `.dvc/` with the cache directory
  created.
- `2-remote`: Remote HTTP storage initialized. It's a shared read only storage
  that contains all data artifacts produced during next steps.
- `3-add-file`: Raw data file `data.xml` downloaded and put under DVC control
  with [`dvc add`](https://man.dvc.org/add). First DVC-file (`.dvc` file
  extension) created.
- `4-source`: Source code downloaded and put under Git control.
- `5-preparation`: First stage file (DVC-file) created using
  [`dvc run`](https://man.dvc.org/run). It transforms XML data into TSV.
- `6-featurization`: Feature extraction stage created. It takes data in TSV
  format and produces two `.pkl` files that contain serialized feature matrices.
- `7-train`: Model training stage created. It produces `model.pkl` file – the
  actual result that can then get deployed to an app that implements NLP
  classification.
- `8-evaluate`: Evaluation stage. Runs the model on a test dataset to produce
  its performance AUC value. The result is dumped into a DVC metric file so that
  we can compare it with other experiments later.
- `9-bigrams-model`: Bigrams experiment, code has been modified to extract more
  features. We run [`dvc repro`](https://man.dvc.org/repro) for the first time
  to illustrate how DVC can reuse cached files and detect changes along the
  computational graph, regenerating the model with the updated data.
- `10-bigrams-experiment`: Reproduce the evaluation stage with the bigrams based
  model.

There are two additional tags:

- `baseline-experiment`: First end-to-end result that we have performance metric
  for.
- `bigrams-experiment`: Second experiment (model trained using bigrams
  features).

These tags can be used to illustrate `-a` or `-T` options across different
[DVC commands](https://man.dvc.org/).

## Project structure

The data files, DVC-files, and results change as stages are created one by one.
After cloning and using [`dvc pull`](https://man.dvc.org/pull) to download data
under DVC control, the workspace should look like this:

```console
$ tree
.
├── auc.metric            # <-- DVC metric compares baseline and bigrams
├── data                  # <-- Directory with raw and intermediate data
│   ├── features          # <-- Extracted feature matrices
│   │   ├── test.pkl
│   │   └── train.pkl
│   └── prepared          # <-- Processed dataset (split and TSV formatted)
│       ├── test.tsv
│       └── train.tsv
│   ├── data.xml          # <-- Initial XML StackOverflow dataset (raw data)
│   ├── data.xml.dvc
├── evaluate.dvc          # <-- DVC-files in the project root describe pipeline
├── featurize.dvc
├── model.pkl
├── prepare.dvc
├── src                   # <-- Source code to run the pipeline stages
│   ├── evaluate.py
│   ├── featurization.py
│   ├── prepare.py
│   └── train.py
│   └── requirements.txt  # <-- Python dependencies needed in the project
└── train.dvc
```
