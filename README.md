# Talkback Messenger
![Python 2.7 and 3 compatible](https://img.shields.io/pypi/pyversions/talkback-messenger)
![PyPI version](https://img.shields.io/pypi/v/talkback-messenger.svg)
![License: MIT](https://img.shields.io/pypi/l/talkback-messenger.svg)

Talkback Messenger is an application that finds the InfoSec content you're interested in from [talkback.sh](https://talkback.sh/), and posts it to Slack in a digestible format.

<img src="/images/slack_message.png" width="600">

The app can be scheduled to run looking for content from the past 1 to 24 hours, and has a Docker container available for scheduling execution. This means you can run it regularly to give you a constant feed of content.

> [!Note]
> Talkback Messenger is currently in beta. If you use it and find any bugs, please [open an issue](https://github.com/PaperMtn/talkback-messenger/issues)

# Contents

- [About Talkback](#about-talkback)
- [How it works](#how-it-works)
- [Requirements](#requirements)
  - [Slack App](#slack-app-with-bot-token)
  - [Talkback API](#talkback-api-token)
  - [Configuration File](#configuration-file)
- [Installation](#installation)
- [Usage](#usage)
  - [Docker/Containerised](#dockercontainerised)
- [Future additions](#future-additions)

## About Talkback

Talkback is a project developed by [Elttam](https://www.elttam.com/) to help the community be more efficient and effective at keeping up with cyber-security content.

It aggregates InfoSec resources from a number of sources and enriches them with metadata, including AI summaries and categorisation.

You can find out more information about Talkback via blog posts and conference talks at [Elttam's website](https://www.elttam.com/blog/talkback-intro/)

## How it works

Talkback Messenger uses the [Talkback API](https://talkback.sh/api/) to collect content, and then enriches this with information that isn't available using the API by scraping the resource webpage.

Using the concept of subscriptions, Talkback Messenger is able to find resources that are relevant to you. These resources, if they meet the criteria you've set in your subscription, are then posted the Slack users/channels of your choice.

The messages contain a digestible summary of the content, leveraging Talkback's AI summarisation and categorisation, as well as links to the original resource.

## Requirements
### Slack App with Bot Token
You will need to create a Slack App and Bot Token to use with Talkback Messenger. You can find instructions on how to do this [here](https://api.slack.com/authentication/basics).

Your app will require the following scopes:
```
"chat:write",
"chat:write.public",
"links:write",
"im:write",
"users:read",
"users:read.email"
```

I've included an app manifest file that you can use to create your app in the directory [docs/slack/app_manifest.json](docs/slack/app_manifest.json). There is also an [app icon](./images/talkback_icon.png) you can use.

Once you've installed your Slack app, generate and safely store your bot token.

Pass the token to Talkback Messenger using the `SLACK_API_TOKEN` environment variable.

> [!Note]
> To post to private Slack channels, you will need to first add the bot to the channel.

### Talkback Email and Password
You will also need to pass the email and password of your Talkback account to Talkback Messenger, which are used to generate a token at runtime. This can be done using the `TALKBACK_EMAIL` and `TALKBACK_PASSWORD` environment variables.

> [!Note]
> You can generate API tokens via the Talkback interface, but these expire after 7 days, with no programmatic way of refreshing them. To work around this, Elttam have added the ability to generate a token using your email and password.

### Configuration File
Lastly, you will need to generate a `talkback.yml` configuration file. This file defines what content you want to collect from Talkback, and where you want to post it. In-depth instructions on how to create this file can be found [here](./docs/talkback_conf).

An example configuration has also been included in the directory [docs/talkback_conf](docs/talkback_conf/example_talkback.yml).
## Installation
Talkback Messanger can be installed via pipx from PyPi:

```bash
pipx install talkback-messanger
```

There is also a Docker container available on DockerHub:

```bash
docker pull papermtn/talkback-messenger
```

## Usage

Remember to load the required environment variables:
- `SLACK_API_TOKEN`
- `TALKBACK_EMAIL`
- `TALKBACK_PASSWORD`

Talkback Messenger can be run from the command line with the following options:
```bash
usage: talkback-messenger [-h] [-v] [--config CONFIG] --timeframe {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24} [--debug]

Talkback Messenger

options:
  -h, --help            show this help message and exit
  -v, --version         show programs version number and exit
  --config CONFIG       Path to the configuration file. Do not use if you are running in a container and have mounted the config file
  --timeframe {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24}
                        How many hours back to search (1-24)
  --debug, -d           Turn on debug level logging
```

Example:
```bash
talkback-messenger --config /path/to/talkback.yml --timeframe 1
```

### Docker/Containerised
Talkback Messanger has been designed to also run in a container, meaning you can schedule it to run at regular intervals to keep you up to date with the latest content.

You will need to pass the configuration file to the container by mounting it as a volume. Talkback Messenger will look for the configuration file at `/etc/talkback-messenger/talkback.yml`.

To run the Docker container, you can use the following command:
```bash
docker run -v /path/to/talkback.yml:/etc/talkback-messenger/talkback.yml papermtn/talkback-messenger --timeframe 1
```

> [!Important]
> The config file must be mounted in the following path: `/etc/talkback-messenger/talkback.yml`
> 
> The `--config` option is not required if you are running the container and have mounted the configuration file.
> 
> Make sure you pass the required environment variables to the container in a secure manner:
> - `SLACK_API_TOKEN`
> - `TALKBACK_EMAIL`
> - `TALKBACK_PASSWORD`

## Future additions
Talkback Messenger is a work in progress, and currently in pre-release.

Possible future additions to the app include: 
- [x] Add the ability to post to multiple channels
- [x] Add posting to individual users via DM from the bot
- [x] Add channels and users as destinations for specific subscriptions
- [ ] Add integration with Microsoft Teams

If you have any suggestions or feature requests, please feel free to open an issue.