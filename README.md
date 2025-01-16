# Talkback Messenger

Talkback Messenger is a in an application that collects the InfoSec content you're interested in from [talkback.sh](https://talkback.sh/), and posts it to Slack in a digestible format.

<img src="/images/slack_screenshot.png" width="700">

The app can be scheduled to run looking for content from the past 1 to 24 hours, and has a Docker container available for scheduling execution. This means you can run it regularly to give you a constant feed of content.
# Contents

- [About Talkback](#about-talkback)
- [How it works](#how-it-works)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)

## About Talkback

---

Talkback is a project developed by [elttam](https://www.elttam.com/) to help the community be more efficient and effective at keeping up with cyber-security content.

It aggregates InfoSec resources from a number of sources, enriches them with metadata, including AI summaries and categorisation.

You can find out more information about Talkback via blog posts and conference talks at [elttam's website](https://www.elttam.com/blog/talkback-intro/)

## How it works

---

Talkback Slack Bot uses the [Talkback API](https://talkback.sh/api/), and the concept of subscriptions, to find relevant resources for you from Talkback, then post them to a Slack channel of your choice.

## Installation
### Prerequisites
#### Slack App with Bot Token
To use the Talkback Slack Bot, you will need to create a Slack App and Bot Token. You can find instructions on how to do this [here](https://api.slack.com/authentication/basics).






## Future additions
Possible future additions to the app include: 
- [ ] Add the ability to post to multiple channels
- [ ] Add posting to individual users via DM from the bot
- [ ] Add channels and users as destinations for specific subscriptions
- [ ] Add integration with Microsoft Teams