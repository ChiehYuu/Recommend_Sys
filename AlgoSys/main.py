import yaml
from .core.reg import RegressionModelMixer


def load_config(config_path):
    with open(config_path, 'r') as stream:
        config = yaml.safe_load(stream)
    return config


def main():
    config = load_config('config.yaml')

    model_names = config['model_names']
    hyperparameters = config['hyperparameters']
    data = ...  # Load your data here

    mixer = RegressionModelMixer(model_names, hyperparameters, data)

    # Assuming you have some test data X_test
    result = mixer.get_ensemble_result(X_test)
    print(result)


if __name__ == "__main__":
    main()
