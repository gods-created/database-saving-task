# DatabaseSavingTask

Welcome to the **DatabaseSavingTask Project**! This repository contains the source code and documentation for managing and tracking tasks efficiently.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

The project was created to copy files from the S3 basket and send them to email using AWS SES. Final purpose: deployment as a lambda function and periodic execution via EventBridge Schedule.

## Features

- Receiving files
- Sending files to email in a single message

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/gods-created-created/database-saving-task.git
    ```
2. Navigate to the project directory:
    ```bash
    cd database-saving-task
    ```
3. Install dependencies:
    ```bash
    python - m pip install -r requirements.txt
    ```

## Usage

Start the application:
```bash
python lambda_function.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).