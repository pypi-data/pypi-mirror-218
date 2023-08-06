# -*- coding: utf-8 -*-

"""
A Translation module.

You can translate text using this module.
"""
import re
import time
from random import choice, expovariate
from urllib.parse import urlencode, urlparse, urlunparse
from functools import wraps
from typing import Callable

import requests

from .models import Translated
from .constants import (USERAGENTS, DEFAULT_RAISE_EXCEPTION, BASE_URL,
                        DUMMY_DATA, LANGCODES, LANGUAGES, HEADERS, PHRASES)
from .exceptions import ConnectionException, BadResponseException


def _retry_on_connection_error(func: Callable) -> Callable:
    """Decorator to retry the function max_connection_attemps number of times.

    Herewith-decorated functions need an ``_attempt`` keyword argument.

    This is to decorate functions that do network requests that may fail.
    Functions that only use these for network access must not be decorated with this  decorator."""
    @wraps(func)
    def call(translator, *args, **kwargs):
        try:
            return func(translator, *args, **kwargs)
        except BadResponseException as err:
            error_string = f"{func.__name__}({', '.join([repr(arg) for arg in args])}): {err}"
            if (kwargs.get('_attempt') or 1) == translator.max_connection_attempts:
                raise ConnectionException(error_string) from None
            translator._error(error_string + " [retrying; skip with ^C]")
            try:
                if kwargs.get('_attempt'):
                    kwargs['_attempt'] += 1
                else:
                    kwargs['_attempt'] = 2
                translator._do_sleep()
                return call(translator, *args, **kwargs)
            except ConnectionException:
                translator._error("[skipped by user]")
                raise ConnectionException(error_string) from None
    return call


class TranslatorDuck:
    """Duckduckgo Translator API

    You have to create an instance of TranslatorDuck to use this API

    :param user_agent: the User-Agent header to send when making requests.
    :type user_agent: :class:`str`

    :param timeout: Definition of timeout for httpx library.
                    Will be used for every request.
    :type timeout: :class:`int`

    :param raise_exception: if `True` then raise exception if something goes wrong
    :type raise_exception: :class:`bool`

    :param headers: Headers for requests.
    :type headers: :class:`dict`

    :param query_string: Query string for vqd.
    :type query_string: :class:`str`

    :param max_connection_attempts: Maximum number of connection attempts until a
                                    request is aborted. Defaults to 3.
                                    Set this to 0 to retry infinitely.
    :type max_connection_attempts: :class:`int`
    """

    def __init__(
            self, useragent=None, raise_exception=DEFAULT_RAISE_EXCEPTION,
            timeout=5, headers=None, query_string=None, max_connection_attempts=3, sleep=True):

        self.timeout = timeout
        self.raise_exception = raise_exception
        self.sleep = sleep
        self.max_connection_attempts = max_connection_attempts

        self.headers = headers
        if not self.headers:
            self.headers = HEADERS

        self.useragent = useragent
        if self.useragent:
            self.headers['User-Agent'] = self.useragent


        self.query_string = query_string
        if not self.query_string:
            self.query_string = choice(PHRASES)

        self.vqd = self._get_vqd(self.query_string)

    @_retry_on_connection_error
    def _get_vqd(self, query_string) -> str:
        """Return vqd as string. Required for Duckduckgo api."""

        # For getting random vqd...
        query_params = {'q': query_string}

        # Build req url
        vqd_req_url = urlunparse(
            urlparse(BASE_URL)._replace(query=urlencode(query_params))
        )
        vqd_res = requests.get(vqd_req_url, headers=self.headers, timeout=self.timeout)

        vqd: str = ''

        vqd_list = re.findall('vqd="([^"]*)"', vqd_res.text)
        if vqd_list:
            vqd = vqd_list[0]

        return vqd

    def _change_vqd(self):
        new_phrase = choice(PHRASES)

        while self.query_string == new_phrase:
            new_phrase = choice(PHRASES)

        self.query_string = new_phrase
        self.vqd = self._get_vqd(self.query_string)

    def _change_useragent(self):
        new_useragent = choice(USERAGENTS)

        while self.headers['User-Agent'] == new_useragent:
            new_useragent = choice(USERAGENTS)

        self.headers['User-Agent'] = new_useragent

    @_retry_on_connection_error
    def _translate(self, text: str, dest: str, src: str, _attempt: int = 1):
        """Low-level communication for translation with duckduckgo.com."""
        # Max lenth is 1000 for data
        text = text.strip()[:1000]
        data = text[:text.rfind('.') + 1] if len(text) == 1000 else text

        # Set query params
        query_params = {
            'vqd': self.vqd,
            'query': self.query_string,
            'to': dest,
        }

        # if `from` is not in `query_params` then duckduckgo detects `from`
        if src:
            query_params.update({'from': src})

        # build `req_url` from `BASE_URL`
        req_url = urlunparse(
            urlparse(BASE_URL)._replace(query=urlencode(query_params), path='translation.js'))

        res = requests.post(req_url, data=data, timeout=self.timeout, headers=self.headers)

        if res.ok:
            return res.json(), res

        if self.raise_exception:
            exception_message = f'Unexpected status code "{res.status_code}" from {res.url}' \
                                f'\nResponse text is {res.text}'
            raise BadResponseException(exception_message)

        return DUMMY_DATA, res

    def _do_sleep(self):
        if self.sleep:
            time.sleep(min(expovariate(0.6), 10.0))

    def _error(self, msg: str):
        """Log a non-fatal error message to stderr, which is repeated at program termination.

        :param msg: Message to be printed."""
        print(msg)

    def translate(
            self, text: str, src: str='', dest: str='en',
            new_useragent: bool=False, new_vqd: bool=False):
        """Return translated text.

        :param text: Text to translate, if text length more than
                    1000 then splits first 1000.

        :param src: Source language.

        :param dest: Destionation language.

        :param new_useragent: if `True` then use new useragent for request.

        :param new_vqd: if `True` then use new new_vqd for request."""

        src = src.lower()
        dest = dest.lower()

        if src and src not in LANGUAGES:
            if src in LANGCODES:
                src = LANGCODES[src]
            else:
                raise ValueError('invalid source language')

        if dest not in LANGUAGES:
            if dest in LANGCODES:
                dest = LANGCODES[dest]
            else:
                raise ValueError('invalid destination language')


        ## I do not know what is vqd, but it seems like an identifier,
        # cause its required for translation, let user can reset it.
        if new_vqd:
            self._change_vqd()
        if new_useragent:
            self._change_useragent()

        data, response = self._translate(text, dest, src)

        translated = data['translated']
        detected = data['detected_language']

        result = Translated(
            src=src, dest=dest, text=translated, origin=text,
            detected=detected, response=response)

        return result
