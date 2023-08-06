"""Endpoint serving."""
from __future__ import annotations

import asyncio
import dataclasses
import json
import logging
import os
import uuid

try:
    import quart
    import uvicorn
    import uvloop
    from quart import request
    from quart import Response
except ImportError as e:  # pragma: no cover
    # Usually we would just print a warning, but this file requires
    # quart to be available to register functions to a top-level blueprint.
    raise ImportError(
        f'{e}. To enable endpoint serving, install proxystore with '
        '"pip install proxystore[endpoints]".',
    ) from e

from proxystore.endpoint.config import EndpointConfig
from proxystore.endpoint.constants import MAX_CHUNK_LENGTH
from proxystore.endpoint.endpoint import Endpoint
from proxystore.endpoint.exceptions import PeerRequestError
from proxystore.endpoint.storage import SQLiteStorage
from proxystore.utils import chunk_bytes

logger = logging.getLogger(__name__)

routes_blueprint = quart.Blueprint('routes', __name__)


def create_app(
    endpoint: Endpoint,
    max_content_length: int | None = None,
    body_timeout: int = 300,
) -> quart.Quart:
    """Create quart app for endpoint and registers routes.

    Args:
        endpoint: Initialized endpoint to forward quart routes to.
        max_content_length: Max request body size in bytes.
        body_timeout: Number of seconds to wait for the body to be
            completely received.

    Returns:
        Quart app.
    """
    app = quart.Quart(__name__)

    app.config['endpoint'] = endpoint

    app.register_blueprint(routes_blueprint, url_prefix='')

    logger.info(
        'Quart routes registered to endpoint '
        f'{endpoint.uuid} ({endpoint.name})',
    )

    app.config['MAX_CONTENT_LENGTH'] = max_content_length
    app.config['BODY_TIMEOUT'] = body_timeout

    return app


def serve(
    config: EndpointConfig,
    *,
    log_level: int | str = logging.INFO,
    log_file: str | None = None,
    use_uvloop: bool = True,
) -> None:
    """Initialize endpoint and serve Quart app.

    Warning:
        This function does not return until the Quart app is terminated.

    Args:
        config: Configuration object.
        log_level: Logging level of endpoint.
        log_file: Optional file path to append log to.
        use_uvloop: Install uvloop as the default event loop implementation.
    """
    if config.host is None:
        raise ValueError('EndpointConfig has NoneType as host.')

    if log_file is not None:
        parent_dir = os.path.dirname(log_file)
        if not os.path.isdir(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        logging.getLogger().handlers.append(logging.FileHandler(log_file))

    for handler in logging.getLogger().handlers:
        handler.setFormatter(
            logging.Formatter(
                '[%(asctime)s.%(msecs)03d] %(levelname)-5s (%(name)s) :: '
                '%(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
            ),
        )
    logging.getLogger().setLevel(log_level)

    kwargs = dataclasses.asdict(config)
    # These are the only two EndpointConfig attributes not passed to the
    # Endpoint constructor
    kwargs.pop('host', None)
    kwargs.pop('port', None)

    database_path = kwargs.pop('database_path', None)
    storage: SQLiteStorage | None
    if database_path is not None:
        logger.info(
            f'Using SQLite database for storage (path: {database_path})',
        )
        storage = SQLiteStorage(database_path)
    else:
        logger.warning(
            'Database path not provided. Data will not be persisted',
        )
        storage = None

    endpoint = Endpoint(**kwargs, storage=storage)
    app = create_app(endpoint)

    if use_uvloop:  # pragma: no cover
        logger.info('Installing uvloop as default event loop')
        uvloop.install()
    else:
        logger.warning(
            'Not installing uvloop. Uvicorn may override and install anyways',
        )

    server_config = uvicorn.Config(
        app,
        host=config.host,
        port=config.port,
        log_config=None,
        log_level=logger.level,
        access_log=False,
    )
    server = uvicorn.Server(server_config)

    logger.info(
        f'Serving endpoint {endpoint.uuid} ({endpoint.name}) on '
        f'{config.host}:{config.port}',
    )
    logger.info(f'Config: {config}')
    asyncio.run(server.serve())


@routes_blueprint.before_app_serving
async def _startup() -> None:
    endpoint = quart.current_app.config['endpoint']
    await endpoint.async_init()


@routes_blueprint.after_app_serving
async def _shutdown() -> None:
    endpoint = quart.current_app.config['endpoint']
    await endpoint.close()


@routes_blueprint.route('/')
async def _home() -> tuple[str, int]:
    return ('', 200)


@routes_blueprint.route('/endpoint', methods=['GET'])
async def _endpoint_() -> Response:
    endpoint = quart.current_app.config['endpoint']
    return Response(
        json.dumps({'uuid': str(endpoint.uuid)}),
        200,
        content_type='application/json',
    )


@routes_blueprint.route('/evict', methods=['POST'])
async def _evict() -> Response:
    key = request.args.get('key', None)
    if key is None:
        return Response('request missing key', 400)

    endpoint_uuid: str | uuid.UUID | None = request.args.get(
        'endpoint',
        None,
    )
    endpoint = quart.current_app.config['endpoint']
    if isinstance(endpoint_uuid, str):
        try:
            endpoint_uuid = uuid.UUID(endpoint_uuid, version=4)
        except ValueError:
            return Response(f'{endpoint_uuid} is not a valid UUID4', 400)

    try:
        await endpoint.evict(key=key, endpoint=endpoint_uuid)
        return Response('', 200)
    except PeerRequestError as e:
        return Response(str(e), 400)


@routes_blueprint.route('/exists', methods=['GET'])
async def _exists() -> Response:
    key = request.args.get('key', None)
    if key is None:
        return Response('request missing key', 400)

    endpoint_uuid: str | uuid.UUID | None = request.args.get(
        'endpoint',
        None,
    )
    endpoint = quart.current_app.config['endpoint']
    if isinstance(endpoint_uuid, str):
        try:
            endpoint_uuid = uuid.UUID(endpoint_uuid, version=4)
        except ValueError:
            return Response(f'{endpoint_uuid} is not a valid UUID4', 400)

    try:
        exists = await endpoint.exists(key=key, endpoint=endpoint_uuid)
        return Response(
            json.dumps({'exists': exists}),
            200,
            content_type='application/json',
        )
    except PeerRequestError as e:
        return Response(str(e), 400)


@routes_blueprint.route('/get', methods=['GET'])
async def _get() -> Response:
    key = request.args.get('key', None)
    if key is None:
        return Response('request missing key', 400)

    endpoint_uuid: str | uuid.UUID | None = request.args.get(
        'endpoint',
        None,
    )
    endpoint = quart.current_app.config['endpoint']
    if isinstance(endpoint_uuid, str):
        try:
            endpoint_uuid = uuid.UUID(endpoint_uuid, version=4)
        except ValueError:
            return Response(f'{endpoint_uuid} is not a valid UUID4', 400)

    try:
        data = await endpoint.get(key=key, endpoint=endpoint_uuid)
    except PeerRequestError as e:
        return Response(str(e), 400)

    if data is not None:
        return Response(
            response=chunk_bytes(data, MAX_CHUNK_LENGTH),
            content_type='application/octet-stream',
        )
    else:
        return Response('', 400)


@routes_blueprint.route('/set', methods=['POST'])
async def _set() -> Response:
    key = request.args.get('key', None)
    if key is None:
        return Response('request missing key', 400)

    endpoint_uuid: str | uuid.UUID | None = request.args.get(
        'endpoint',
        None,
    )
    endpoint = quart.current_app.config['endpoint']
    if isinstance(endpoint_uuid, str):
        try:
            endpoint_uuid = uuid.UUID(endpoint_uuid, version=4)
        except ValueError:
            return Response(f'{endpoint_uuid} is not a valid UUID4', 400)

    data = bytearray()
    # Note: tests/endpoint/serve_test.py::test_empty_chunked_data handles
    # the branching case for where the code in the for loop is not executed
    # but coverage is not detecting that hence the pragma here
    async for chunk in request.body:  # pragma: no branch
        data += chunk

    if len(data) == 0:
        return Response('Received empty payload', 400)

    try:
        await endpoint.set(key=key, data=bytes(data), endpoint=endpoint_uuid)
    except PeerRequestError as e:
        return Response(str(e), 400)
    else:
        return Response('', 200)
