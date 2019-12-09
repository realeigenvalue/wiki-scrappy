import scrapy.cmdline
def main():
    scrapy.cmdline.execute(argv=['scrapy', 'runspider', 'wikipedia.py', '-o', 'data.json'])

if __name__ == '__main__':
    main()