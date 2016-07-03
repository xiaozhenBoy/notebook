# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from scrapy import signals
from scrapy.signalmanager import SignalManager
from scrapy.responsetypes import responsetypes
from scrapy.xlib.pydispatch import dispatcher
from selenium import webdriver
from six.moves import queue
from twisted.internet import defer, threads
from twisted.python.failure import Failure
from scrapy.http import HtmlResponse

class PhantomJSMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # if request.meta.has_key('PhantomJS'):# 如果设置了PhantomJS参数，才执行下面的代码
        if True:
            # log.msg('PhantomJS Requesting: '+request.url, level=log.WARNING)
            service_args = ['--load-images=false', '--disk-cache=true']
            if request.meta.has_key('proxy'): # 如果设置了代理(由代理中间件设置)
                # log.msg('PhantomJS proxy:'+request.meta['proxy'][7:], level=log.WARNING)
                service_args.append('--proxy='+request.meta['proxy'][7:])
            try:
                driver = webdriver.PhantomJS() # (executable_path = '/usr/local/bin/phantomjs', service_args = service_args)
                driver.get(request.url)
                content = driver.page_source.encode('utf-8')
                url = driver.current_url.encode('utf-8')
                driver.quit()
                if content == '<html><head></head><body></body></html>':# 内容为空，当成503错误。交给重试中间件处理
                    return HtmlResponse(request.url, encoding = 'utf-8', status = 503, body = '')
                else: # 返回response对象
                    return HtmlResponse(url, encoding = 'utf-8', status = 200, body = content)

            except Exception, e: # 请求异常，当成500错误。交给重试中间件处理
                # log.msg('PhantomJS Exception!', level=log.WARNING)
                return HtmlResponse(request.url, encoding = 'utf-8', status = 503, body = '')
        else:
            # log.msg('Common Requesting: '+request.url, level=log.WARNING)
            pass

class PhantomJSDownloadHandler(object):

    def __init__(self, settings):
        self.options = settings.get('PHANTOMJS_OPTIONS', {})

        max_run = settings.get('PHANTOMJS_MAXRUN', 10)
        self.sem = defer.DeferredSemaphore(max_run)
        self.queue = queue.LifoQueue(max_run)

        SignalManager(dispatcher.Any).connect(self._close, signal=signals.spider_closed)

    def download_request(self, request, spider):
        """use semaphore to guard a phantomjs pool"""
        return self.sem.run(self._wait_request, request, spider)

    def _wait_request(self, request, spider):
        try:
            driver = self.queue.get_nowait()
        except queue.Empty:
            driver = webdriver.PhantomJS(**self.options)

        driver.get(request.url)
        # ghostdriver won't response when switch window until page is loaded
        dfd = threads.deferToThread(lambda: driver.switch_to.window(driver.current_window_handle))
        dfd.addCallback(self._response, driver, spider)
        return dfd

    def _response(self, _, driver, spider):
        body = driver.execute_script("return document.documentElement.innerHTML")
        if body.startswith("<head></head>"):  # cannot access response header in Selenium
            body = driver.execute_script("return document.documentElement.textContent")
        url = driver.current_url
        respcls = responsetypes.from_args(url=url, body=body[:100].encode('utf8'))
        resp = respcls(url=url, body=body, encoding="utf-8")

        response_failed = getattr(spider, "response_failed", None)
        if response_failed and callable(response_failed) and response_failed(resp, driver):
            driver.close()
            return defer.fail(Failure())
        else:
            self.queue.put(driver)
            return defer.succeed(resp)

    def _close(self):
        while not self.queue.empty():
            driver = self.queue.get_nowait()
            driver.close()
