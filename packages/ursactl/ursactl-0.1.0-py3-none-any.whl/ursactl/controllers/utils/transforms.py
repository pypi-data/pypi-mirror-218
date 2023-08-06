"""
Utilities for working with transforms in the CLI.
"""
import json
import yaml


def load_from_markdown(source):
    info = {}
    content = list(source)
    if content[0] == "---\n":
        split_at = len(content)
        # get metadata from header
        for i in range(1, len(content)-1):
            if content[i] == "---\n":
                split_at = i
                break
        raw_yaml = "".join(content[1:split_at])
        content = content[split_at+1:]
        info = yaml.load(raw_yaml, Loader=yaml.Loader)

    info['configurationSchema'] = None
    info['description'] = ''

    name, content = _get_name(content)
    chunks = _split_into_chunks(content)

    # first chunk is the description if it doesn't have a '##' at the start
    if not chunks[0][0].startswith('## '):
        info['description'] = "".join(chunks[0])
        chunks = chunks[1:]

    info['name'] = name

    for chunk in chunks:
        _update_info_from_chunk(info, chunk)

    return info


def _update_info_from_chunk(info, chunk):
    if chunk[0].startswith('## Metadata'):
        info.update(yaml.load("".join(chunk[1:]), Loader=yaml.Loader))
    if chunk[0].startswith('## Configuration Schema'):
        # we need the ```yaml ... ``` parts (or json)
        source = _find_fenced_block(chunk[1:], "yaml")
        if source is not None:
            info['configurationSchema'] = yaml.load("".join(source), Loader=yaml.Loader)
        else:
            source = _find_fenced_block(chunk[1:], "json")
            if source is not None:
                info['configurationSchema'] = json.loads("".join(source))
    if chunk[0].startswith('## Implementation'):
        # we need the ```lua ... ``` parts
        lua = _find_fenced_block(chunk[1:], "lua")
        if lua is not None:
            info['implementation'] = "".join(lua)


def _get_name(content):
    name = None
    # the first top-level header is the name of the transform
    for i in range(0, len(content)-1):
        if content[i].startswith('# '):
            name = content[i][2:].strip()
            content = content[i+1:]
            break
    return name, content


def _split_into_chunks(content):
    chunks = []
    chunk = []
    for line in content:
        if line.startswith('## '):
            if len(chunk) > 0:
                chunks.append(chunk)
            chunk = []
        chunk.append(line)
    if len(chunk) > 0:
        chunks.append(chunk)
    return chunks


def _find_fenced_block(chunk, tag):
    buffer = []
    started = False
    for line in chunk:
        if not started and line == f'```{tag}\n':
            started = True
            continue
        if started and line == '```\n':
            return buffer
        if started:
            buffer.append(line)
    return None
