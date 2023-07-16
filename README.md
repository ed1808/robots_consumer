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