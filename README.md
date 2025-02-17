### How to start the app

1. **Get an API Key:**

    - Sign up for an API key from OpenWeatherMap.
    - Once you have your API key, create a `.env` file in the root directory of your project and add the following line to it:
    
    ```env
    OPENWA_KEY=your_openaq_api_key
    ```

2. **Create a virtual environment:**

    ```sh
    python3 -m venv venv
    ```

3. **Activate the virtual environment:**

    - **For Bash:**
    
        ```sh
        source venv/bin/activate
        ```

    - **For PowerShell:**
    
        ```sh
        .\venv\bin\Activate.ps1
        ```

4. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

5. **Run the app:**

    ```sh
    python main.py
    ```

6. **Test the app:**

    Input a city of your choice to the app and see the output.
