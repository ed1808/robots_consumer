# Robots Consumer

This is an application that let's you execute multiple web robots. If you don't have
worker processess but instead you have to execute some URL in the browser to realize some tasks,
this application maybe could help you.

If you want to contribute, feel free to do that.


## About the JSON file

The structure of the JSON file will be the next:

```
{
    "delay": 2,
    "robotsUrls": [
        "url1",
        "url2",
        "url3"
    ]
}
```

The **delay** will be the time in seconds between each request.

The **robotsUrls** will be an array that contains the urls to be requested.

## Usage

To use this application, you can create a virtual environment or you can also use it without one but, 
you must make sure that you have the packages specified in the requirements.txt file installed.

### Using a virtual environment

#### On Windows:

```
python -m venv venv
```

Once the venv has been created, install all packages specified in the requirements.txt

```
pip install requirements.txt
```

And when all the packages are installed, you can run the application now

```
python main.py
```

#### On macOS or Linux:

```
python3 -m venv venv
```

Once the venv has been created, install all packages specified in the requirements.txt

```
pip3 install requirements.txt
```

And when all the packages are installed, you can run the application now

```
python3 main.py
```

To stop the consumer, just press Ctrl+C to kill the process.
