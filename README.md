# Connected Papers Crawler

## 基本描述
（找文献综述找麻了给自己写了一个脚本，在本地是好跑的但是大家用的话可能会遇到各种问题，sigh~~本来还要传上vercel但是vercel似乎不支持前后端交互，之后琢磨琢磨研究研究再继续改进doge~）。
这是一个自动化爬虫脚本，用于在 [Connected Papers](https://www.connectedpapers.com/) 网站上搜索文章，并爬取相关文章的详细信息。爬虫会模拟用户在网站上进行文章搜索，并在图谱页面中爬取相关的论文信息。最终，它将保存文章的信息到 Excel 文件，并下载相关的 PDF 文件。

## 功能

- 在 [Connected Papers](https://www.connectedpapers.com/) 上搜索指定的文章名称。
- 进入图谱页面，遍历相关文章并爬取其标题、作者、发表日期、所属学科、引用量等信息。
- 下载 PDF 文件并保存到指定目录。
- 将文章信息（标题、链接、作者、发表时间、学科、引用量）保存到 Excel 文件。

## 执行过程

1. 输入需要搜索的文章名称。
2. 输入保存文件的文件夹路径。
3. 脚本将自动打开浏览器，访问 [Connected Papers](https://www.connectedpapers.com/)。
4. 在搜索框中输入文章名称并执行搜索。
5. 脚本将自动点击相关的文章，并在图谱页面中爬取相关论文的详细信息。
6. 将爬取的论文信息保存到 Excel 文件，并下载 PDF 文件。

## 依赖环境和安装

本爬虫脚本依赖以下环境和库：

- Python 3.x
- [Selenium](https://pypi.org/project/selenium/) 用于自动化浏览器操作
- [pandas](https://pypi.org/project/pandas/) 用于数据处理和 Excel 文件操作
- [requests](https://pypi.org/project/requests/) 用于下载 PDF 文件

### 安装步骤

1. 安装 Python 依赖：

    ```bash
    pip install selenium pandas requests
    ```

2. 下载并配置 [ChromeDriver](https://sites.google.com/chromium.org/driver/)（确保与 Chrome 版本匹配）。

3. 根据脚本中 `chrome_driver_path` 的设置，修改为你本地的 `chromedriver` 路径。

4. 运行脚本：

    ```bash
    python crawler.py
    ```

## 当前版本

**版本 1.0**

- 支持通过 [Connected Papers](https://www.connectedpapers.com/) 网站搜索并爬取单个网页中的文章信息。
- 登录步骤是虚拟的，实际上并不执行登录，直接执行搜索功能。
- 由于 [Connected Papers](https://www.connectedpapers.com/) 网站提供免费的额度，因此不需要额外的登录步骤。

## 注意事项

- 本脚本仅支持爬取 [Connected Papers](https://www.connectedpapers.com/) 网站上的文章。
- 当前版本在执行过程中将直接搜索并获取数据，不需要进行任何用户登录。
- 网站的限制可能会影响爬取的频率，因此建议在使用时适当控制爬取频率，避免触发反爬虫机制。

# Connected Papers Crawler

## Overview

This is an automated crawler script designed to search for articles on [Connected Papers](https://www.connectedpapers.com/) and scrape related article details. The crawler simulates a user searching for articles on the website and scrapes information from the graph page. It then saves the article details to an Excel file and downloads the related PDF files.

## Features

- Search for a specified article title on [Connected Papers](https://www.connectedpapers.com/).
- Navigate to the graph page, traverse related articles, and scrape details such as title, authors, publication date, subject, citation count, etc.
- Download PDF files and save them to a specified directory.
- Save article information (title, link, authors, publication date, subject, citation count) to an Excel file.

## Execution Process

1. Input the article title to search for.
2. Input the folder path where the file should be saved.
3. The script will automatically open a browser and visit [Connected Papers](https://www.connectedpapers.com/).
4. The script will input the article title into the search bar and execute the search.
5. It will then click on the relevant articles and scrape detailed information from the graph page.
6. The scraped article details will be saved to an Excel file, and PDF files will be downloaded.

## Dependencies and Installation

This crawler script requires the following environment and libraries:

- Python 3.x
- [Selenium](https://pypi.org/project/selenium/) for browser automation
- [pandas](https://pypi.org/project/pandas/) for data processing and Excel file handling
- [requests](https://pypi.org/project/requests/) for downloading PDF files

### Installation Steps

1. Install the Python dependencies:

    ```bash
    pip install selenium pandas requests
    ```

2. Download and configure [ChromeDriver](https://sites.google.com/chromium.org/driver/) (make sure it's compatible with your Chrome version).

3. In the script, update the `chrome_driver_path` variable to match the path of your local `chromedriver`.

4. Run the script:

    ```bash
    python crawler.py
    ```

## Current Version

**Version 1.0**

- Supports searching and scraping article information from a single page on [Connected Papers](https://www.connectedpapers.com/).
- The login step is virtual and does not require an actual login; it directly executes the search function.
- Since [Connected Papers](https://www.connectedpapers.com/) provides a free usage quota, there is no need for an additional login step.

## Notes

- This script only supports scraping articles from the [Connected Papers](https://www.connectedpapers.com/) website.
- The current version will directly search and collect data without requiring any user login.
- Website restrictions may affect the crawling frequency, so it is recommended to control the crawl rate appropriately to avoid triggering anti-crawling mechanisms.


## License

MIT License
