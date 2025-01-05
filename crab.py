import os
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_crawler(article_name, work_dir, email=None, password=None):
    """
    爬虫主函数
    :param article_name: 需要搜索的文章名称
    :param work_dir: 保存文件的文件夹路径
    :param email: 登录邮箱（可选）
    :param password: 登录密码（可选）
    """
    # 创建工作目录下的文件路径
    excel_path = os.path.join(work_dir, "link.xlsx")  # Excel 文件路径
    pdf_dir = os.path.join(work_dir, "papers")  # PDF 文件夹路径

    # 检查并创建 PDF 文件夹
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    # 初始化链接存储，如果文件存在则读取
    if os.path.exists(excel_path):
        try:
            links_df = pd.read_excel(excel_path)
            # 确保包含所需的列
            required_columns = ["Title", "URL", "Authors", "Publication Date", "Discipline", "Citations"]
            for col in required_columns:
                if col not in links_df.columns:
                    links_df[col] = None  # 添加缺失的列
        except Exception as e:
            print(f"读取 Excel 文件时出错: {e}。重新初始化 DataFrame。")
            links_df = pd.DataFrame(columns=["Title", "URL", "Authors", "Publication Date", "Discipline", "Citations"])
    else:
        links_df = pd.DataFrame(columns=["Title", "URL", "Authors", "Publication Date", "Discipline", "Citations"])

    # 调试输出
    print("Initialized links_df columns:", links_df.columns)
    print(links_df.head())

    # 设置 ChromeDriver 路径
    chrome_driver_path = "D:/chrome_driver/chromedriver-win64/chromedriver.exe"  # 替换为实际路径
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 如果不需要显示浏览器窗口，可以加上这个选项
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 打开目标网站
        driver.get("https://www.connectedpapers.com/")

        # 等待页面加载
        wait = WebDriverWait(driver, 10)  # 最多等待 10 秒

        # 登录逻辑（先检查是否存在登录按钮）
        try:
            login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.navbar-button")))
            print("Login button detected. Proceeding to login...")
            login_button.click()

            # 如果没有提供邮箱和密码，则从控制台获取
            if email is None:
                email = input("请输入登录邮箱: ")
            if password is None:
                password = input("请输入登录密码: ")

            # 点击 Google 登录按钮
            google_login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.outlined-slot span")))
            print("Google login button found. Clicking to continue...")
            google_login_button.click()

            # 输入邮箱
            email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
            email_input.send_keys(email)
            print("Email entered.")

            # 点击下一步
            next_button = driver.find_element(By.CSS_SELECTOR, "button[type='button']")
            next_button.click()
            print("Clicked 'Next' button for email.")

            # 等待输入密码
            password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
            password_input.send_keys(password)
            print("Password entered.")

            # 提交登录
            login_submit = driver.find_element(By.CSS_SELECTOR, "button[type='button']")
            login_submit.click()
            print("Login submitted.")
            time.sleep(5)

        except Exception as e:
            print(f"No login button detected or login failed: {e}. Proceeding without login...")

        # 搜索文章
        try:
            search_box = wait.until(EC.presence_of_element_located((By.ID, "searchbar-input")))
            print("Search box found, proceeding with search.")
            search_box.send_keys(article_name)
            search_box.send_keys("\n")
            print("搜索内容已提交")

            # 等待搜索结果加载
            time.sleep(5)

            # 修改：使用新的选择器定位搜索结果
            try:
                # 等待搜索结果出现
                search_results = wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-v-b70c9f7a].paper-title"))
                )
                print(f"找到 {len(search_results)} 个搜索结果")

                # 遍历搜索结果，找到最匹配的文章
                found = False
                for result in search_results:
                    title_text = result.text.strip()
                    print(f"检查搜索结果: {title_text}")
                    
                    # 如果标题完全匹配或包含搜索关键词
                    if article_name.lower() in title_text.lower():
                        print(f"找到匹配文章: {title_text}")
                        # 点击文章标题
                        driver.execute_script("arguments[0].click();", result)
                        found = True
                        print("已点击文章，等待图谱加载...")
                        time.sleep(5)  # 等待图谱加载
                        break

                if not found:
                    print("未找到完全匹配的文章，点击第一个结果")
                    if search_results:
                        driver.execute_script("arguments[0].click();", search_results[0])
                        print(f"已点击第一个搜索结果: {search_results[0].text}")
                        time.sleep(5)  # 等待图谱加载
                    else:
                        raise Exception("没有找到任何搜索结果")

            except Exception as e:
                print(f"处理搜索结果时出错: {e}")
                raise

        except Exception as e:
            print(f"搜索过程出错: {e}")
            raise

        # 等待图像页面加载
        time.sleep(5)

        # 遍历图像页面中的文章节点
        try:
            # 找到所有文章节点
            articles = driver.find_elements(By.CSS_SELECTOR, "circle.node-circle")
            print(f"找到 {len(articles)} 篇文章。")

            for index, article in enumerate(articles):
                try:
                    title_element = article.find_element(By.TAG_NAME, "title")
                    title = title_element.text.strip()
                    print(f"正在处理第 {index + 1}/{len(articles)} 篇文章: {title}")
                except Exception as e:
                    print(f"提取第 {index + 1} 篇文章标题时出错: {e}")
                    continue

                # 修改点击逻辑
                try:
                    # 滚动到元素位置
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", article)
                    time.sleep(2)  # 增加等待时间

                    # 使用JavaScript直接触发点击事件
                    driver.execute_script("""
                        var evt = new MouseEvent('click', {
                            bubbles: true,
                            cancelable: true,
                            view: window
                        });
                        arguments[0].dispatchEvent(evt);
                    """, article)
                    
                    print(f"成功点击文章: {title}")
                    time.sleep(3)  # 增加点击后的等待时间

                    # 等待侧边栏加载
                    container = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.abstractbox"))
                    )
                    
                    # 提取文章信息
                    try:
                        title_element = container.find_element(By.CSS_SELECTOR, "a.title_link")
                        article_title = title_element.text.strip()
                        article_link = title_element.get_attribute("href")
                        print(f"标题: {article_title}")
                        print(f"文章链接: {article_link}")

                        # 提取作者信息
                        try:
                            authors_element = container.find_element(By.CSS_SELECTOR, "div.metadata > div > div")
                            authors = authors_element.text.strip()
                            print(f"作者: {authors}")
                        except Exception as e:
                            authors = "N/A"
                            print(f"提取作者信息时出错: {e}")

                        # 提取发表时间和所属学科
                        try:
                            publication_element = container.find_element(By.CSS_SELECTOR, "div.metadata.publication")
                            publication_info = publication_element.text.strip()
                            publication_date, discipline = publication_info.split(", ", 1)
                            print(f"发表时间: {publication_date}, 所属学科: {discipline}")
                        except Exception as e:
                            publication_date, discipline = "N/A", "N/A"
                            print(f"提取发表时间和所属学科时出错: {e}")

                        # 提取引用量
                        try:
                            citation_element = container.find_element(By.CSS_SELECTOR, "div.metadata:nth-child(1)")
                            citations = citation_element.text.strip()
                            print(f"引用量: {citations}")
                        except Exception as e:
                            citations = "N/A"
                            print(f"提取引用量时出错: {e}")

                        # PDF 下载逻辑
                        try:
                            pdf_buttons = container.find_elements(By.CSS_SELECTOR, "a.open-in-icon[href$='.pdf']")
                            if pdf_buttons:
                                pdf_link = pdf_buttons[0].get_attribute("href")
                                print(f"PDF链接: {pdf_link}")
                                
                                # 检查 PDF 是否已下载
                                filename = f"{article_title}.pdf".replace('/', '_').replace('\\', '_').replace(':', '_')
                                pdf_path = os.path.join(pdf_dir, filename)
                                
                                if not os.path.exists(pdf_path):
                                    headers = {
                                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                                        "Accept": "application/pdf"
                                    }
                                    response = requests.get(pdf_link, headers=headers, stream=True, timeout=15)
                                    if response.status_code == 200:
                                        with open(pdf_path, 'wb') as f:
                                            for chunk in response.iter_content(chunk_size=1024):
                                                f.write(chunk)
                                        print(f"PDF 下载成功: {pdf_path}")
                                    else:
                                        print(f"PDF 下载失败，状态码: {response.status_code}")
                                else:
                                    print(f"PDF 已存在: {pdf_path}")
                            else:
                                print(f"文章没有 PDF 下载按钮: {article_title}")

                        except Exception as e:
                            print(f"下载 PDF 时出错: {e}")

                        # 检查文章是否已经存在于 Excel
                        if article_link not in links_df["URL"].values:
                            # 保存到 Excel
                            try:
                                new_row = pd.DataFrame({
                                    "Title": [article_title],
                                    "URL": [article_link],
                                    "Authors": [authors],
                                    "Publication Date": [publication_date],
                                    "Discipline": [discipline],
                                    "Citations": [citations]
                                })
                                links_df = pd.concat([links_df, new_row], ignore_index=True)
                                links_df.to_excel(excel_path, index=False)
                                print(f"成功保存到 Excel: {article_title}")
                            except Exception as e:
                                print(f"保存到 Excel 时出错: {e}")
                        else:
                            print(f"文章已存在于 Excel: {article_title}")

                    except Exception as e:
                        print(f"提取文章信息时出错: {str(e)}")
                        continue

                except Exception as e:
                    print(f"处理文章 {title} 时出错: {e}")
                    continue

        except Exception as e:
            print(f"查找文章时出错: {e}")

    finally:
        driver.quit()

    return {
        "success": True,
        "message": "爬取完成",
        "data": {
            "excel_path": excel_path,
            "pdf_dir": pdf_dir
        }
    }

if __name__ == "__main__":
    # 直接运行时的代码
    article_name = input("请输入需要搜索的文章名称: ")
    work_dir = input("请输入保存文件的文件夹路径（例如 D:/path）：").strip()
    
    result = run_crawler(article_name, work_dir)
    print(result)
