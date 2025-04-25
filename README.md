# LinkedInBot

Web browser automation to create more leads for your Linkedin profile! Use sparingly because overuse can result in bans.

## Installation with Docker

1. Requirements: </br>
   Docker >= 20.10

2. Clone repo and build image

```bash
git clone https://github.com/Pedro-Ponteiro/Linkedin_ProfileVisits_Booster.git
cd LinkedinBot
docker build -t pedroponteiro/linkedinbot:0.1 .
```

## Customization

1. Create a secrets.prod.json file inside "container_data" folder (see secrets.example.json)

2. You can specify people you don't want to visit in should_not_visit.txt (one linkedin link per line)


## Usage

```python
docker run -it --rm -v ${PWD}/container_data:/app/container_data --shm-size="2g" pedroponteiro/linkedinbot:0.1 python linkedinbot/start.py
```

## Debugging

After counting the number of profiles found at the "My Network" Page, the driver saves a screenshot at "container_data" which is bind mounted (meaning you can see the image in the host computer)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

For Forks, please don't commit directly to "main" branch.

## License

[MIT](https://choosealicense.com/licenses/mit/)
