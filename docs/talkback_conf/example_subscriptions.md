# Example Subscriptions
Let's look at some example scenarios and subscriptions to retrieve that data.

You can use these as a template to create your own subscriptions in the `talkback.yml` file. Remember that you can have multiple subscriptions under each key, and you can mix and match with filters and destinations to create a list of granular subscriptions.

> [!Note]
> I recommend reading the [Talkback Introduction](https://www.elttam.com/blog/talkback-intro/) to get a full understanding of how Talkback works before diving into building advanced subscriptions

**Scenario 1**:
> I want to receive all resources from Talkback that are related to the category `cloud security` and have a rank of 50 or higher. I want to post these resources to the channel `#cloud-security` (which I have collected the channel ID from) and to the user joe.bloggs@example.com`

To achieve this, we can create a subscription under the `categories` key formatted like this:

```yaml
slack:
  default_channel: ...
  default_user: ...
subscriptions:
  categories:
    - id: Cloud Security Posts
      query: cloud security
      filters:
        rank: 50
      slack_destinations:
        - channel: 
          - C01A2B3C4D5
        - user:
          - joe.bloggs@example.com 
```

**Scenario 2**:
> I want to receive blog posts and news articles from Talkback that are related to the topic `ransomware` and have a rank of 75 or higher. I want these resource to be posted to the default channel and user I have set in the configuration file.

To achieve this, we can create a subscription under the `topics` key formatted like this:

```yaml
slack:
  default_channel: C01A2B3C4D5
  default_user: UA1B2C3D4E5
subscriptions:
  topics:
    - id: Ransomware Posts
      query: ransomware
      filters:
        rank: 75
        resource_types:
          - post
          - news
``` 


**Scenario 3**:
> I want to receive resources relating to open source software and blog posts written by PaperMtn. I want to receive every resource from these sources, and I want these resources to be posted to the channel `#opensource` and to three users: alice@example.com, bob@example.com and mallory@example.com`

PaperMtn (Me!) publishes open source software on GitHub (https://github.com/PaperMtn), and blog posts on `papermtn.co.uk`. We can create two subscriptions under the `sources` key to achieve our goal:

```yaml
slack:
  default_channel: ...
  default_user: ...
subscriptions:
  sources:
    - id: Papermtn
      query: papermtn.co.uk
      filters:
        rank: 0
        resource_types:
          - post
          - oss
      slack_destinations:
        - channel:
            - C01A2B3C4D5
        - user:
            - alice@example.com
            - bob@example.com
            - mallory@example.com
    - id: GitHub PaperMtn
      query: github.com/PaperMtn
      filters:
        rank: 0
        resource_types:
          - post
          - oss
      slack_destinations:
        - channel:
            - C01A2B3C4D5
        - user:
            - alice@example.com
            - bob@example.com
            - mallory@example.com

```

**Scenario 4**:
> I want to receive all resources relating to two specific AWS vulnerabilities, regardless of rank:
> - `CVE-2025-0693`
> - `CVE-2024-8901`
> 
> Also, I want to get all posts and news articles relating to the vendor `Amazon`, but only if they are from a curated source. 
> 
> I want all of these resources to be posted to myself

To achieve this, we can create two subscriptions under the `vulnerabilities` key and one subscription under the `vendors` key:

```yaml
slack:
  default_channel: ...
  default_user: ...
subscriptions:
  vulnerabilities:
    - id: CVE-2025-0693
      query: CVE-2025-0693
      filters:
        rank: 0
      slack_destinations:
        - user:
            - papermtn@example.com
    - id: CVE-2024-8901
      query: CVE-2024-8901
      filters:
        rank: 0
      slack_destinations:
        - user:
            - papermtn@example.com
  vendors:
    - id: Amazon vendor posts
      query: amazon
      filters:
        resource_types:
          - post
          - news
        curated: true
      slack_destinations:
        - user:
            - papermtn@example.com
```

**Scenario 5**:
> I want to receive all posts and open source software that contain the string `slack` and `api` in proximity to each other in the content. I want to receive all resources, regardless of rank, and I want these resources to be posted to the default channel.

To achieve this, we can create a subscription under the `queries` key that makes use of the [Elasticsearch query syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax):

```yaml
slack:
  default_channel: C01A2B3C4D5
subscriptions:
  queries:
    - id: Slack API Posts
      query: 'content: "slack api"~5'
      filters:
        rank: 0
        resource_types:
          - post
          - oss
```