# -*- coding: utf-8 -*-

import asyncio
from handlers.base import BaseHandler
from utilities.gaclient import GAcess
from pprint import pprint as pp
import time

class MainHandler(BaseHandler):

    service = None

    def initialize(self):
        service_account = self.settings['service_account_email']
        self.service = GAcess(service_account_email=service_account)

    def get(self):
        start_time = time.time()
        loop = asyncio.get_event_loop()
        tasks = [
            self._get_accounts(),
            self._get_accounts()
        ]
        try:
            loop.run_in_executor(None, tasks)
        finally:
            loop.close()

        finish_time = time.time()
        print("Recorded calculated in %s ms" % int((finish_time-start_time)*1000))
        import pdb
        pdb.set_trace()
        # pp(sources)
        # pp(accounts)

        data = {}
        # data['sources'] = sources
        # data['accounts'] = accounts
        self.render('index.html', **data)

    @asyncio.coroutine
    def _get_sources(self):
        results = self.service.get_people_sources()
        print("got sources")
        #return results

    @asyncio.coroutine
    def _get_accounts(self):
        results = self.service.get_sessions_results()
        print("got accounts")
        #return results