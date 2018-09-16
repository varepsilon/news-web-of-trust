#! /usr/bin/env python3

import json
import subprocess
import sys
import time
import random

random.seed(42)

if __name__ == '__main__':
    with open('./users_json') as f:
        users = json.load(f)
    user_ids = list(users.keys())
    FAKE_NEWS_PROB = 0.3
    AVG_SUPPORT_SIZE = 3
    ONE_FLIP_PROB = 0.3  # probability that one vote is contradictory

    urls = []
    group = None
    with open('./testdata/news_urls.txt') as f:
        for line in f:
            if line.startswith('http'):
                url = line.rstrip()
                urls.append((group, url))
                print(url)

                vote = 0 if random.random() < FAKE_NEWS_PROB else 1
                num_users = random.randint(AVG_SUPPORT_SIZE - 1, AVG_SUPPORT_SIZE + 1)
                flip = random.random() < ONE_FLIP_PROB

                users = random.sample(user_ids, num_users)
                votes = [vote] * num_users
                if flip:
                    votes[0] = 1 - votes[0]
                for u, v in zip(users, votes):
                    command = 'curl http://localhost:8000/vote -d "url={}" -d "user={}" -d "ranking={}" -X PUT'.format(
                        url, u, v)
                    subprocess.call(command, shell=True)
    #             time.sleep(0.5)
            else:
                group = line.rstrip()
                print(group)
