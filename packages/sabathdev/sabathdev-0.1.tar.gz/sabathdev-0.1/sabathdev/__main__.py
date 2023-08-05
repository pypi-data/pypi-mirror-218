import os
import sys
import subprocess

def run_command(command):
    try:
        print(f"Running: {command}")
        result = subprocess.run(command, shell=True, check=True, text=True)
        print("Command finished successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

benchmark_repos = {
    "MNIST_tf_keras": {
        "url": "https://github.com/tokey-tahmid/sciml-bench.git",
        "benchmark_dir": "/data/ttahmid/sciml-bench",
        "dataset_dir": "/data/ttahmid/sabath-datasets/sciml-bench/data/MNIST",
        "commands": {
            "install": "pip install .",
            "list": "sciml-bench list",
            "run": "sciml-bench run --output_dir output_root_dir/results MNIST_tf_keras",
            "download": "sciml-bench download MNIST"
        }
    },
    "MNIST_torch": {
        "url": "https://github.com/tokey-tahmid/sciml-bench.git",
        "benchmark_dir": "/data/ttahmid/sciml-bench",
        "dataset_dir": "/data/ttahmid/sabath-datasets/sciml-bench/data/MNIST",
        "commands": {
            "install": "pip install .",
            "list": "sciml-bench list",
            "run": "sciml-bench run --output_dir output_root_dir/results MNIST_torch",
            "download": "sciml-bench download MNIST"
        }
    },
    "em_denoise": {
        "url": "https://github.com/tokey-tahmid/sciml-bench.git",
        "benchmark_dir": "/data/ttahmid/sciml-bench",
        "dataset_dir": "/data/ttahmid/sabath-datasets/sciml-bench/data/em_graphene_sim",
        "commands": {
            "install": "pip install .",
            "list": "sciml-bench list",
            "run": "sciml-bench run --output_dir output_root_dir/results em_denoise",
            "download": "sciml-bench download em_graphene_sim"
        }
    },
    "dms_structure": {
        "url": "https://github.com/tokey-tahmid/sciml-bench.git",
        "benchmark_dir": "/data/ttahmid/sciml-bench",
        "dataset_dir": "/data/ttahmid/sabath-datasets/sciml-bench/data/dms_sim",
        "commands": {
            "install": "pip install .",
            "list": "sciml-bench list",
            "run": "sciml-bench run --output_dir output_root_dir/results dms_structure",
            "download": "sciml-bench download dms_sim"
        }
    },
    "slstr_cloud": {
        "url": "https://github.com/tokey-tahmid/sciml-bench.git",
        "benchmark_dir": "/data/ttahmid/sciml-bench",
        "dataset_dir": "/data/ttahmid/sabath-datasets/sciml/data/slstr_cloud_ds1",
        "commands": {
            "install": "pip install .",
            "list": "sciml-bench list",
            "run": "sciml-bench run --output_dir output_root_dir/results slstr_cloud",
            # "run": "sciml-bench run --dataset_dir /data/ttahmid/sabath-datasets/sciml/data/slstr_cloud_ds1 --output_dir /data/ttahmid/sabath-datasets/sciml/results slstr_cloud",
            "download": "sciml-bench download slstr_cloud_ds1"
        }
    },
    "cosmoflow": {
        "url": "https://github.com/tokey-tahmid/cosmoflow-benchmark.git",
        "benchmark_dir": "/data/ttahmid/cosmoflow-benchmark",
        "dataset_dir": "/data/ttahmid/sabath-datasets/cosmoflow/cosmoUniverse_2019_05_4parE_tf_v2",
        "commands": {
            "install": "",
            "list": "",
            "run": "python train.py configs/cosmo.yaml",
            "download": "wget https://portal.nersc.gov/project/dasrepo/cosmoflow-benchmark/cosmoUniverse_2019_05_4parE_tf_v2_mini.tar"
        }
    }
    # Add more benchmarks here...
}
if len(sys.argv) > 2:
    benchmark_name = sys.argv[1]
    dataset_name = sys.argv[2]

    repo_info = benchmark_repos.get(benchmark_name)
    if repo_info is None:
        print(f"Unknown benchmark: {benchmark_name}")
        sys.exit(1)

    repo_url = repo_info["url"]
    repo_dir = repo_info["benchmark_dir"]
    data_dir = repo_info["dataset_dir"]
    commands = repo_info["commands"]

    if not os.path.exists(repo_dir):
        run_command(f"git clone {repo_url} {repo_dir}")
        os.chdir(repo_dir)
        run_command(commands["install"])
        run_command(commands["list"])
    else:
        os.chdir(repo_dir)
    if not os.path.exists(data_dir):
        run_command(commands["download"])
        run_command(commands["run"])
    else:
        run_command(commands["run"])
else:
    print("Usage: python3 __main__.py <benchmark_name> <dataset_name>")
