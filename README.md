# Talkback Messenger

Talkback Messenger is a in an application that collects the InfoSec content you're interested in from [talkback.sh](https://talkback.sh/), and posts it to Slack in a digestible format.

<img src="/images/slack_screenshot.png" width="700">

The app can be scheduled to run looking for content from the past 1 to 24 hours, and has a Docker container available for scheduling execution. This means you can run it regularly to give you a constant feed of content.
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

---

Talkback is a project developed by [elttam](https://www.elttam.com/) to help the community be more efficient and effective at keeping up with cyber-security content.

It aggregates InfoSec resources from a number of sources, enriches them with metadata, including AI summaries and categorisation.

You can find out more information about Talkback via blog posts and conference talks at [elttam's website](https://www.elttam.com/blog/talkback-intro/)

## How it works

---

Talkback Messenger uses the [Talkback API](https://talkback.sh/api/), and the concept of subscriptions, to find relevant resources for you from Talkback, then post them to a Slack channel of your choice.

## Requirements
### Slack App with Bot Token
To use the Talkback Messenger, you will need to create a Slack App and Bot Token. You can find instructions on how to do this [here](https://api.slack.com/authentication/basics).

Your app will require the following scopes:
```text
"chat:write",
"chat:write.public",
"links:write",
"im:write",
"users:read",
"users:read.email"
```

I've included an app manifest file that you can use to create your app in the directory [docs/slack/app_manifest.json](docs/slack/app_manifest.json).

Once you've installed your Slack app, generate and safely store your bot token.

### Talkback API Token
You will also need an API token for Talkback. You can find instructions on how to do this [here](https://talkback.sh/api/v1/help/).

Generate and store the JWT for use with Talkback Messenger.

### Configuration File
Finally, you will also need to generate a `talkback.conf` configuration file. This file defines what content you want to collect from Talkback, and where you want to post it. In-depth instructions on how to create this file can be found [here](./docs/talkback_conf).

An example configuration has also been included in the directory [docs/talkback_conf](docs/talkback_conf/example_talkback.conf).
## Installation
## Usage
### Docker/Containerised





## Future additions
Possible future additions to the app include: 
- [x] Add the ability to post to multiple channels
- [x] Add posting to individual users via DM from the bot
- [x] Add channels and users as destinations for specific subscriptions
- [ ] Add integration with Microsoft Teams