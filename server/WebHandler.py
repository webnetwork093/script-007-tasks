from aiohttp import web
import json
import os
import server.FileService as FileService


class WebHandler:
    """aiohttp handler with coroutines."""

    def __init__(self) -> None:
        pass

    async def handle(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Basic coroutine for connection testing.

        Args:
            request (Request): aiohttp request.

        Returns:
            Response: JSON response with status.
        """

        return web.json_response(data={
            'status': 'success'
        })

    async def change_dir(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for changing working directory with files.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                "path": "string. Directory path. Required",
            }.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.
        """

        data = await request.json()
        path = data.get("path")

        try:
            FileService.change_dir(os.path.join(os.getcwd(), path))

            return web.json_response(data={
                'status': 'success',
                'message': 'path ' + path + ' successfully processed'
            })
        except (ValueError, RuntimeError) as err:
            data = {
                    'status': 'error',
                    'message': str(err)
                   }
            raise web.HTTPBadRequest(body=json.dumps(data))


    async def get_files(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for getting info about all files in working directory.

        Args:
            request (Request): aiohttp request.

        Returns:
            Response: JSON response with success status and data or error status and error message.
        """


        return web.json_response(data={
                                        'status': 'success',
                                        'files': [f.get("name") for f in FileService.get_files()],
                                      }, dumps=json.dumps)


    async def get_file_data(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for getting full info about file in working directory.

        Args:
            request (Request): aiohttp request, contains filename and is_signed parameters.

        Returns:
            Response: JSON response with success status and data or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.
        """

        if request.match_info.get('filename') is None:
            raise web.HTTPBadRequest(body="No filename")

        try:
            data = FileService.get_file_data(os.path.join(os.getcwd(),request.match_info.get('filename')), False)

            return web.json_response(data={
                'status': 'success',
                'data': json.loads(json.dumps(data))
            })
        except (ValueError, RuntimeError) as err:
            data = {
                    'status': 'error',
                    'message': str(err)
                   }
            raise web.HTTPBadRequest(body=json.dumps(data))


    async def create_file(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for creating file.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                'filename': 'string. filename',
                'content': 'string. Content string. Optional',
            }.

        Returns:
            Response: JSON response with success status and data or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.
        """

        data = await request.json()
        filename = data.get("filename", None)
        content = data.get("content", "")

        if filename is None:
            raise web.HTTPBadRequest(body="No filename")

        try:
            data = FileService.create_file(os.path.join(os.getcwd(), filename), content)

            return web.json_response(data={
                'status': 'success',
                'data': json.loads(json.dumps(data))
            })
        except (ValueError, RuntimeError) as err:
            data = {
                    'status': 'error',
                    'message': str(err)
                   }
            raise web.HTTPBadRequest(body=json.dumps(data))

    async def delete_file(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for deleting file.

        Args:
            request (Request): aiohttp request, contains filename.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.

        """

        if request.match_info.get('filename') is None:
            raise web.HTTPBadRequest(body="No filename")

        try:
            FileService.delete_file(os.path.join(os.getcwd(), request.match_info.get('filename')))

            return web.json_response(data={
                'status': 'success',
            })
        except (ValueError, RuntimeError) as err:
            data = {
                    'status': 'error',
                    'message': str(err)
                   }
            raise web.HTTPBadRequest(body=json.dumps(data))
