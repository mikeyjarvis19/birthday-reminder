# Example Docker run commands

## Windows
```
docker run --rm -it  -v C:\Dev\pdp\BirthdayReminder\pushover_credentials.json:/pushover_credentials.json -v C:\Dev\pdp\BirthdayReminder\credentials.json:/credentials.json -v C:\Dev\pdp\BirthdayReminder\token.pickle:/token.pickle -t birthdayreminder:latest
```

## Linux
#### Interactive
```
docker run --rm -it  -v /home/pi/birthday-reminder/pushover_credentials.json:/pushover_credentials.json -v /home/pi/birthday-reminder/credentials.json:/credentials.json -v /home/pi/birthday-reminder/token.pickle:/token.pickle -t mikeyjarvis19/birthday-reminder:latest
```
#### Detatched
```
docker run -d -v /home/pi/birthday-reminder/pushover_credentials.json:/pushover_credentials.json -v /home/pi/birthday-reminder/credentials.json:/credentials.json -v /home/pi/birthday-reminder/token.pickle:/token.pickle -t mikeyjarvis19/birthday-reminder:latest
```

# Command to build and push Docker image:
```
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t mikeyjarvis19/birthday-reminder:latest --push .
```