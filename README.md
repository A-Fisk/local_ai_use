# Repo for local ai api use

- Want to access open ai + claude api to see how that works outside of
  running server like openwebui


## Instructions for anthropic
- development docs [here](https://docs.anthropic.com/en/home)
- create developer account
- get api key
- set api key in your terminal
`export ANTHROPIC_API_KEY='your-api-key'`
- create environment with `anthropic` package
    - have done in environment variable here 
- call the api in a python script
    - example in /anthropic/claude_use.py
- can modify the system prompt, max_tokens, and temperature 

### Extended thinking 
- in order to allow thinking just add thinking block to the messages call
```
    "thinking": {
        "type": "enabled",
        "budget_tokens": 200
    },
```




## TODO
- how to do multi-turn conversations?
- set input message to be command line argument 
