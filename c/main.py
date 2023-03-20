from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from apscheduler.schedulers.twisted import TwistedScheduler
from c.spider import TrackerSpider
from c.log import  log


def main():
    # https://stackoverflow.com/questions/44228851/scrapy-on-a-schedule
    settings = get_project_settings()
    # if verbose: log.setLevel(logging.DEBUG)
    settings['LOG_ENABLED'] = True

    process = CrawlerProcess(settings)
    sched = TwistedScheduler()

    process.crawl(TrackerSpider, soldNum_min=1000, Ids=1)
    sched.add_job(process.crawl, 'interval', args=[TrackerSpider], kwargs={'soldNum_min': 1000, 'Ids': 1},seconds=10)
    sched.add_job(sched.print_jobs, 'interval',seconds=10)

    log.info('开始商品价格追踪')
    sched.start()
    process.start(False)


if __name__ == '__main__':
    main()
