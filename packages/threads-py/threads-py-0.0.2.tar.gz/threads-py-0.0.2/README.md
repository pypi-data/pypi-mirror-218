# [<img src="./.github/logo.jpg" width="36" height="36" />](https://github.com/junhoyeo) threads-py

> Unofficial, Reverse-Engineered Python client for Meta's Threads.

## Installation

```bash
pip install threads-py
```

## Usages

```python
from threadspy import ThreadsAPI

api = ThreadsAPI()

username = "{username}"

# get a user id
user_id = api.get_user_id_from_username(username)
print(user_id)

# get a profile info
profile = api.get_user_profile(username, user_id=user_id)
print(profile)

# get a profile's threads tab
threads = api.get_user_profile_threads(username, user_id=user_id)
print(threads)

# get a profile's replies tab
replies = api.get_user_profile_replies(username, user_id=user_id)
print(replies)

# 3-ways to get the {post_id}
thread_id = "CuX_UYABrr7"
post_id = api.get_post_id_from_thread_id(thread_id)
print(post_id)

post_url = "https://www.threads.net/t/CuX_UYABrr7/?igshid=MzRlODBiNWFlZA=="
post_id = api.get_post_id_from_url(post_url)
print(post_id)

thread_id = "CuX_UYABrr7"
post_id = api.get_post_id_from_thread_id(thread_id)
print(post_id)

# get threads info
thread = api.get_threads(post_id)
print(thread)

# get who liked a thread
linkers = api.get_thread_likers(post_id)
print(linkers)
```

## [<img src="./.github/emojis/pushpin.png" width="30" height="30" />](https://github.com/junhoyeo) Roadmap

- [x] ✅ Read public data
  - [x] ✅ Fetch UserID(`314216`) via username(`zuck`)
  - [x] ✅ Read User Profile Info
  - [x] ✅ Read list of User Threads
  - [x] ✅ Read list of User Repiles
  - [x] ✅ Fetch PostID(`3140957200974444958`) via PostURL(`https://www.threads.net/t/CuW6-7KyXme`)
  - [x] ✅ Read Threads via PostID
  - [x] ✅ Read Likers in Thread via PostID
  - [ ] 🚧 Read User Followers
  - [ ] 🚧 Read User Followings
- [ ] 🚧 LangChain Agent
  - [ ] 🚧 Link Threads & LLaMa
  - [ ] 🚧 Provide statistical analysis of posts in Threads
- [ ] 🚧 Read private data
- [ ] 🚧 Write data (i.e. write automated Threads)

## License

<p align="center">
  <a href="https://github.com/junhoyeo">
    <img src="./.github/labtocat.png" width="256" height="256">
  </a>
</p>

<p align="center">
  <strong>MIT © <a href="https://github.com/junhoyeo">Junho Yeo</a></strong>
</p>

If you find this project intriguing, **please consider starring it(⭐)** or following me on [GitHub](https://github.com/junhoyeo) (I wouldn't say [Threads](https://www.threads.net/@_junhoyeo)).