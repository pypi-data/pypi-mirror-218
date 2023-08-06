from __future__ import annotations

from pathlib import Path

from fastapi import Request


def find_parent_file(folder: Path, filename: str) -> Path:
    if not folder.is_dir():
        raise NotADirectoryError(f'{folder=} is not a directory')
    if folder == folder.parent:
        raise FileNotFoundError(f'{filename=} is not found')
    for item in folder.iterdir():
        if item.name == filename:
            return item
    return find_parent_file(folder.parent, filename)


def get_client_address(request: Request) -> str:
    client_address = request.headers.get('x-azure-clientip')
    if client_address:
        return client_address
    return request.headers.get('x-client-ip', request.client.host)
