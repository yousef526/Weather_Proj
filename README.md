
# Weather Project

This project retrieves weather data for random cities in Egypt using the OpenWeather API.

## Project Structure

- **dags/**: Contains the Directed Acyclic Graphs (DAGs) for Apache Airflow workflows.
- **logs/**: Stores log files generated during workflow executions.
- **Dockerfile**: Defines the Docker image for the project environment.
- **docker-compose.yaml**: Configures services for the project using Docker Compose.
- **.gitattributes**: Manages Git attributes for the repository.

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- An OpenWeather API key. You can obtain one by signing up at [OpenWeather](https://openweathermap.org/api).

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yousef526/Weather_Proj.git
   cd Weather_Proj
   ```

2. **Configure Environment Variables**:
   - Create a `.env` file in the project root directory.
   - Add the following line to the `.env` file, replacing `your_api_key` with your actual OpenWeather API key:
     ```
     OPENWEATHER_API_KEY=your_api_key
     ```

3. **Build and Start the Services**:
   - Run the following command to build the Docker images and start the services:
     ```bash
     docker-compose up --build
     ```

4. **Access the Airflow Web Interface**:
   - Once the services are running, access the Airflow web interface by navigating to `http://localhost:8080` in your web browser.
   - Log in using the default credentials:
     - **Username**: `airflow`
     - **Password**: `airflow`

5. **Trigger the DAG**:
   - In the Airflow web interface, locate the DAG responsible for fetching weather data.
   - Trigger the DAG to start the data retrieval process.

## Notes

- Ensure that the `dags/` directory contains the necessary Python scripts defining your Airflow DAGs for fetching weather data.
- The `logs/` directory will accumulate log files over time. Regular maintenance is recommended to manage disk space.
- For any issues or contributions, please refer to the repository's issue tracker on GitHub.
