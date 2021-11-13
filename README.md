# LinkedInBot

Web browser automation to create more leads for your Linkedin profile! Use sparingly because overuse can result in bans.

## Installation with Docker

1. Requirements: </br>
   Docker 20.10.10

2. Clone repo and build image

```bash
git clone https://github.com/Pedro-Ponteiro/LinkedinBot.git
cd LinkedinBot
docker build -t pedroponteiro/linkedinbot:0.1 .
```

3. Create a secrets.prod.json file inside "container_data" folder (see secrets.example.json)

```python
{
    "username": "your_username@email.com",  # your username
    "password": "your_password",  # your password
    "job_titles": [
        "job_title_of_people_i_want_to_connect",
        "ceo"
    ],
    "profile_visits": 50, # number of profiles to visit
    "connect_with": 25 # number of profiles to connect
}
```

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

## Results after one week

![image](https://user-images.githubusercontent.com/48108738/138418903-0bde6dc2-b84e-4762-adf4-a7f0b6181f2f.png)
