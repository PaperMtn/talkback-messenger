# Creating a Talkback Messenger Configuration File

The `talkback.yml` file contains the configuration for Talkback Messenger, and defines the subscriptions for the content you want to receive from Talkback. You will need to provide the path to this file when running Talkback Messenger.

This section will walk you through the file layout, and what each section does.

## Configuration File Structure and Terminology

The `talkback.yml` file is YAML formatted, and must contain certain keys in order to be valid. The following shows the format required of the YAML file:

```yaml
---
slack:
  default_channel: #REQUIRED (Slack Channel ID)
  default_user: #OPTIONAL (email address OR Slack User ID)
subscriptions: #REQUIRED - All subscriptions go under this key
  categories:
    - id: #REQUIRED (Human-readable name)
      query: #REQUIRED (Search query)
      filters: #OPTIONAL
        rank: 20 #OPTIONAL
        resource_types: #OPTIONAL
          - post
        curated: #OPTIONAL
      slack_destinations: #OPTIONAL
        users: #OPTIONAL
          - # Slack User ID or email address
        channels: #OPTIONAL
          - # Slack Channel ID
```
This diagram gives a more visual way of understanding the structure of the file, and an introduction to the terminology used:

<img src="/images/talkback_yml_diagram.png" width="800">

### Slack Default Destinations
Requirements:
- The `slack` key is REQUIRED
- The `slack` key MUST contain a `default_channel`
- The `slack` key MAY contain a `default_user`
- The `default_channel` value MUST be a Slack Channel ID
- The `default_user` value can be either a Slack User ID OR an email address

This section contains the default destinations for posting resources to Slack. You can optionally specify a user (by either their Slack email address or User ID), but you must specify a channel (by its Slack Channel ID). 

If a subscription does not have a destination specified, it will use the default destinations.

> [!Note]
> Currently Talkback Messanger only supports Slack notifications. This may be expanded in the future to include other messaging platforms.

### Subscription Types
Requirements:
- The `subscriptions` key is REQUIRED
- There MUST be at least one sub-key with a subscription type defined

Subscription types are a logical grouping of subscriptions for specific resources. They are defined by including the sub-key under the `subscriptions` key.

The current options for subscription types are:
- `categories`
  - Return resources based on the category they have been assigned by Talkback
- `topics`
  - Return resources based on the topic they have been assigned by Talkback
- `sources`
  - Resources based on the source of the resource. E.g. DarkReading, KrebsOnSecurity 
- `vendors`
  - Resources relating to a specific vendor or product E.g. Google, Amazon
- `vulnerabilities`
  - Resources relating to a specific CVE
- `queries`
  - Resources returned by a specific string query

Within each subscription type, you can define multiple subscriptions that will return content of that type.
### Subscription Definition
Requirements:
- The subscription definition MUST contain an `id` key
- The subscription definition MUST contain a `query` key
- The subscription definition MAY contain a `filters` key
- The subscription definition MAY contain a `slack_destinations` key

#### Subscription Metadata
##### ID
The `id` key is a human-readable name for the subscription and is used for logging and debugging purposes.
##### Query
The `query` key is the search query that will be used to find resources from Talkback. This query varies based on the subscription type the signature is for:
- `categories`:
  - The category name, e.g `application security`, `cloud security`
  - You can find a list of current categories on Talkback [here](https://talkback.sh/categories/)
- `topics`:
  - The topic name, e.g `ransomware`, `phishing`
  - You can search the list of topics on Talkback [here](https://talkback.sh/topics/)
- `sources`:
  - The domain of the source you want to subscribe to, e.g `darkreading.com`, `papermtn.co.uk`
- `vendors`:
  - The vendor name, e.g `google`, `microsoft`
- `vulnerabilities`:
  - The CVE ID, e.g `CVE-2024-12857`
- `queries`:
  - A string query that will be used to search for resources, the same as you would in the Talkback GUI
  - Talkback uses indexes resources to Elasticsearch, so you can [query search syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax)
  - For more information on writing queries, I would highly recommend reading the introduction to Talkback [here](https://www.elttam.com/blog/talkback-intro/)
#### Subscription Filters
Requirements:
- The `filters` key MAY contain a `rank` key
- The `filters` key MAY contain a `resource_types` key
- The `filters` key MAY contain a `curated` key

Although, if none of the above are specified, the filters key should not be included in the subscription definition.

##### Rank
Talkback assigns a rank to each resource based on a number of criteria, such as the reputation of the source. It is a number between 0 and 100, with 100 being the highest rank.

You can filter resources you want to subscribe to based on this rank. Resources will only be returned if they are ranked equal to or higher than the rank you specify.

> [!TIP]
> If you want to receive all resources for a subscription, you can set the rank to `0`

> [!NOTE]
> If you don't define a rank filter, Talkback Messanger will return resources with a rank of 80 or higher by default. If you want to receive more resources for a subscription, you should define a rank value and set it lower.
##### Resource Types
You can filter which resources you want to receive by the resource type. The current resource types are:
- `post`
- `news`
- `oss`
  - Short for Open Source Software
- `video`
- `paper`
- `slides`
- `n_a`

Under the `resource_types` key, you can specify a list of resource types you want to receive for the subscription:
    
``` yaml
...
filters:
  resource_types:
    - post
    - news
    - oss
```

> [!NOTE] 
> If you don't specify any resource types, all resource types will be returned.

> [!IMPORTANT]
> Make sure to use the exact values for the resource types as shown above. Note that N/A is `n_a` and not `n/a`.
##### Curated
Talkback maintains a list of curators, popular sources in the InfoSec community that are known for producing high-quality content. Content from these sources is given a `curated` marker.

You can use this boolean filter to only receive resources that have been marked as `curated` by Talkback.

The list of current curators can be found [here](https://talkback.sh/about/)
#### Subscription Slack Destinations
Requirements:
- The `slack_destinations` key MAY contain a `users` key
- The `slack_destinations` key MAY contain a `channels` key
- Values in the `users` key can be either Slack User IDs OR email addresses
- Values in the `channels` key MUST be Slack Channel IDs
- You MAY enter multiple values in the `users` and `channels` keys

If you don't specify any destinations, the subscription will use the default destinations specified in the `slack` key.

In the `slack_destinations` key, you can define users and channels you want to send matches for the subscription to. This allows you to be granular with what subscriptions get posted where.

Example:
```yaml
...
slack_destinations:
  users:
    - U01A2B3C4D5E
    - papermtn@example.com
    - tobias.funke@example.com
  channels:
    - C01A2B3C4D5E
```

> [!NOTE]
> Any subscription where Slack destinations are not specified will use the default destinations specified in the `slack` key.

> [!IMPORTANT]
> Defining destinations in the subscription will override the default destinations specified in the `slack` key for that subscription.

## Example Subscriptions
You can find some example subscription definitions [here](./example_subscriptions.md).

There is also an example configuration file [here](./example_talkback.yml) that you can use as a template for your own configuration.