import ctc.rpc
import json
import random
import requests

from functools import partial


HEADERS = {'Content-Type': 'application/json', 'User-Agent': 'flood'}
post = partial(requests.post, headers=HEADERS)


def get_latest_block(url):
    data = json.dumps(ctc.rpc.construct_eth_block_number())
    return int(post(url=url, data=data).json()['result'], base=16)


def request_block(block, url):
    data = json.dumps(ctc.rpc.construct_eth_get_block_by_number(block))
    return post(url=url, data=data)


def get_block_and_ensure_it_exists(nodes, block):
    responses = list(map(partial(request_block, block), nodes))

    assert(all(map(lambda resp: resp.status_code == 200, responses)))

    return responses[0]


def get_block_range_and_tx(nodes):
    block_range = 50
    node_urls = list(map(lambda node: node['url'], nodes.values()))

    latest = get_latest_block(node_urls[0])

    start_block = latest - 150
    end_block = start_block + block_range

    response = get_block_and_ensure_it_exists(node_urls, start_block)
    get_block_and_ensure_it_exists(node_urls, end_block)

    return response.json()['result'], start_block, end_block