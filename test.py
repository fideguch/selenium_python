#Chromiumとseleniumをインストール
!apt-get update
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
!pip install selenium
!pip install pandas
print("Step1: 前処理（必要なパッケージなどのインストール）完了")

#ライブラリをインポート
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
import pandas as pd
from google.colab import files
import time

# ブラウザをheadlessモード実行
options = webdriver.ChromeOptions()
options.add_argument('--headless') # CLIで起動する場合は必須
options.add_argument('--no-sandbox') # sandboxモードを解除する理由は不明。なんかないとクラッシュするらしい。
options.add_argument('--disable-dev-shm-usage') #
chrome_service = fs.Service(executable_path="'chromedriver',options="+options)
driver = webdriver.Chrome(service=chrome_service)
driver.implicitly_wait(10) # 要素が見つかるまでの待機時間
print("\nStep2: ライブラリのインポート&ブラウザの設定完了")

# ブラウザをheadlessモード実行
options = webdriver.ChromeOptions()
options.add_argument('--headless') # CLIで起動する場合は必須
options.add_argument('--no-sandbox') # sandboxモードを解除する理由は不明。なんかないとクラッシュするらしい。
options.add_argument('--disable-dev-shm-usage') #
driver = webdriver.Chrome('chromedriver',options=options)
driver.implicitly_wait(10) # 要素が見つかるまでの待機時間
print("\nStep2: ライブラリのインポート&ブラウザの設定完了")

# 取得するデータ一覧
data = {
	'媒体名': [],
	'求人タイトル': [],
	'企業名': [],
	'職種': [],
	'給与': [],
	'勤務地': [],
	'仕事内容': [],
	'雇用形態': [],
	'求める人物像': [],
	'その他の情報': [],
	'対象URL': []
}

values = []

# 辞書型のdataに配列で確保した値を加える
def add_values(d, v, s):
	i = 0
	d['媒体名'].append(source_media)
	d['求人タイトル'].append(v[i])
	d['企業名'].append(v[i+1])
	d['職種'].append(v[i+1])
	d['給与'].append(v[i+1])
	d['勤務地'].append(v[i+1])
	d['仕事内容'].append(v[i+1])
	d['雇用形態'].append(v[i+1])
	d['求める人物像'].append(v[i+1])
	d['その他の情報'].append(v[i+1])
	d['対象URL'].append(v[i+1])
	return d

#---------------------------------------------------------------------------------------

attack_keyword = 'ホテル フロント'


source_media = "indeed"

# indeed
# サイトアクセス
driver.get("https://jp.indeed.com/")
time.sleep(3)
# 検索結果ページに遷移
indeed_input_what = driver.find_element_by_xpath("//*[@id='text-input-what']")
indeed_input_what.send_keys(attack_keyword)
indeed_input_what.submit()
print(driver.current_url)

# 最終ページまでのループ文
# XPathで全要素取得
elements = driver.find_elements_by_xpath("//div[@id='mosaic-provider-jobcards']/a")
for element in elements:
	# 詳細を開く
	element.click()
	print(driver.current_url)
	# iframe内にdriverを移動
	driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
	# 求人タイトル
	tmp = driver.find_element_by_xpath("//h1")
	values.append(tmp.text)
	# 企業名
	tmp = driver.find_element_by_xpath("//div[contains(@class,'jobsearch-JobInfoHeader-subtitle')]/div/div[2]")
	values.append(tmp.text)
	# 職種
	tmp = driver.find_element_by_xpath("//*[@id='salaryInfoAndJobType']/span[2]")
	values.append(tmp.text)
	# 給与
	tmp = driver.find_element_by_xpath("//*[@id='salaryInfoAndJobType']/span[1]")
	values.append(tmp.text)
	# 勤務地
	tmp = driver.find_element_by_xpath("//body/div[1]/div[1]/div[1]/div/div/div/div[1]/div/div[1]/div[1]/div[1]/div[2]/div/div/div/div[2]/div")
	values.append(tmp.text)
	# 仕事内容
	values.append('-')
	# 求める人物像
	values.append('-')
	# その他の情報
	tmp = driver.find_element_by_xpath("//div[@id='jobDescriptionText']")
	values.append(tmp.text)
	# 対象URL
	values.append(driver.current_url)
	# iframeから戻る
	driver.switch_to.default_content()
	# dataにvaluesを追記
	data = add_values(data, values)
	# valuesを初期化
	values = []
print(data)



# print("\nStepN: データ抽出完了")
# # pandasでDataFrameを整形しCSV形式で吐き出す
# df = pd.DataFrame(data, columns=['媒体名', '求人タイトル', '企業名', '職種', '給与', '勤務地', '仕事内容', '雇用形態', '求める人物像','その他の情報', '対象URL'])

# df.to_csv('各媒体求人情報.csv',index=False)
# files.download('各媒体求人情報.csv')

driver.quit()

print("\nStepN: ドライバ終了 & CSV化完了")
