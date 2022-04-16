attack_keyword = 'リクルート'
max_data = 30

#---------------------------------------------------------------------------------------

#Chromiumとseleniumをインストール
!apt-get update
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
!pip install selenium
!pip install pandas
print("Step1: 前処理（必要なパッケージなどのインストール）完了")

#ライブラリをインポート
from turtle import title
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
import pandas as pd
from google.colab import files
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
#debug
import pprint
import re
# URLを取得するモジュールの import
import urllib.request

# ブラウザをheadlessモード実行
options = webdriver.ChromeOptions()
options.add_argument('--headless') # CLIで起動する場合は必須
options.add_argument('--no-sandbox') # sandboxモードを解除する理由は不明。なんかないとクラッシュするらしい。
options.add_argument('--disable-dev-shm-usage') #
driver = webdriver.Chrome('chromedriver',options=options)
driver.implicitly_wait(10) # 要素が見つかるまでの待機時間
print("\nStep2: ライブラリのインポート&ブラウザの設定完了")

#actions = ActionChains(driver)

#---------------------------------------------------------------------------------------

# 取得するデータ一覧
data = {
	'媒体名': [],
	'求人タイトル(職種)': [],
	'企業名': [],
	'給与': [],
	'勤務地': [],
	'雇用形態': [],
	'その他の情報': [],
	'対象URL': []
}

values = []

# 辞書型のdataに配列で確保した値を加える
def add_values(d, v):
	i = 0
	d['媒体名'].append(source_media)
	d['求人タイトル(職種)'].append(v[i])
	d['企業名'].append(v[i+1])
	d['給与'].append(v[i+2])
	d['勤務地'].append(v[i+3])
	d['雇用形態'].append(v[i+4])
	d['その他の情報'].append(v[i+5])
	d['対象URL'].append(v[i+6])
	return d

# 抽出できているか確認する関数
def chek_values(values):
	flag = True
	for v in values:
		if v == None or v == "":
			flag = False
	return flag

# URLチェック関数
def check_url(url):
	flag = True
	regex = r'[^\x00-\x7F]'
	matchedList = re.findall(regex,url)
	for m in matchedList:
		url = url.replace(m, urllib.parse.quote_plus(m, encoding="utf-8"))
	try:
		f = urllib.request.urlopen(url)
		print('取得可能:', url)
		f.close()
	except urllib.request.HTTPError:
		print('このURLは存在しません:', url)
		flag = False
	return flag


# indeed
source_media = "indeed"

p = 0
# 最終ページor欲しいデータ数に応じてwhile文を回す
while True:
	if len(data["対象URL"]) >= max_data:
		print("\nStepN: "+str(max_data)+"個のデータを取得完了")
		break
	# 対象ページを取得
	print("start_page p="+str(p))
	print("try to get: https://jp.indeed.com/jobs?q="+attack_keyword+"&start="+str(p))
	driver.get("https://jp.indeed.com/jobs?q="+attack_keyword+"&start="+str(p))
	p += 10
	time.sleep(1.5)

	print("現在の求人一覧URL: "+driver.current_url+"\n")
	# XPathで全要素取得
	elements = driver.find_elements(By.XPATH ,"//div[@class='job_seen_beacon']")
	n = 0
	# 求人タイトル(職種)
	titles = driver.find_elements(By.XPATH ,"//div[@class='job_seen_beacon']//h2/span")
	ts = 0
	# 企業名
	company_names = driver.find_elements(By.XPATH ,"//div[@class='job_seen_beacon']//table[@class='jobCard_mainContent']/tbody/tr/td[@class='resultContent']/div[@class='heading6 company_location tapItem-gutter companyInfo']/span[@class='companyName']")
	cn = 0
	# 給与
	salaries = driver.find_elements(By.XPATH ,"//div[@class='job_seen_beacon']//div[@class='heading6 tapItem-gutter metadataContainer']/div[@class='metadata salary-snippet-container']/div[@class='salary-snippet']/span")
	sa = 0
	# 勤務地
	locations = driver.find_elements(By.XPATH ,"//div[@class='job_seen_beacon']//div[@class='heading6 company_location tapItem-gutter companyInfo']/div[@class='companyLocation']")
	lo = 0
	# 雇用形態
	employments = driver.find_elements(By.XPATH ,"//div[@class='job_seen_beacon']//table[@class='jobCard_mainContent']/tbody/tr/td[@class='resultContent']/div[@class='heading6 tapItem-gutter metadataContainer']/div[@class='metadata']")
	em = 0
	# その他の情報
	other_info = driver.find_elements(By.XPATH ,"//div[@class='job_seen_beacon']//table[@class='jobCardShelfContainer']/tbody/tr[@class='underShelfFooter']/td/div[@class='heading6 tapItem-gutter result-footer']/div[@class='job-snippet']")
	oi = 0
	# URL
	links = driver.find_elements(By.XPATH, "//div[@id='mosaic-zone-jobcards']/div[@id='mosaic-provider-jobcards']/a") #.get_attribute("href")

	# elementsの各要素(element)の文字列をキーとし、各要素がキーに含まれるか判定。含まれていればvalueに追記する。
	while n < len(elements):

		key = elements[n].text

		# 求人タイトル(職種)
		if (titles[ts].text in key):
			values.append(titles[ts].text)
			if (len(titles) > ts + 1):
				ts += 1
		else:
			values.append("-")
		# 企業名
		if (company_names[cn].text in key):
			values.append(company_names[cn].text)
			if (len(company_names) > cn + 1):
				cn += 1
		else:
			values.append("-")
		# 給与
		if (salaries[sa].text in key):
			values.append(salaries[sa].text)
			if (len(salaries) > sa + 1):
				sa += 1
		else:
			values.append("-")
		# 勤務地
		if (locations[lo].text in key):
			values.append(locations[lo].text)
			if (len(locations) > lo + 1):
				lo += 1
		else:
			values.append("-")
		# 雇用形態
		if (employments[em].text in key):
			values.append(employments[em].text)
			if (len(employments) > em + 1):
				em += 1
		else:
			values.append("-")
		# その他の情報
		if (other_info[oi].text in key):
			values.append(other_info[oi].text)
			if (len(other_info) > oi + 1):
				oi += 1
		else:
			values.append("-")
		# URL
		values.append(links[n].get_attribute("href"))

		# 空データがなければdataにvaluesを追記
		if chek_values(values) == True:
			data = add_values(data, values)
		# valuesを初期化
		values = []
		n += 1
	# 次ページのURLがなければ終了する
	next_url = ("https://jp.indeed.com/jobs?q="+attack_keyword+"&start="+str(p))
	if not check_url(next_url) == True:
		print("\nStepN: 最終ページまで取得完了")
		break

print("\nStepN: データ抽出完了")

# pandasでDataFrameを整形しCSV形式で吐き出す
df = pd.DataFrame(data, columns=['媒体名', '求人タイトル(職種)', '企業名', '給与', '勤務地', '雇用形態', 'その他の情報', '対象URL'])

df.to_csv('各媒体求人情報.csv',index=False, encoding="utf_8_sig")
files.download('各媒体求人情報.csv')

driver.quit()

print("\nStepN: ドライバ終了 & CSV化完了")
