import requests
from bs4 import BeautifulSoup


response = requests.get("https://worldbeyblade.org/Forum-Tournament-Reports")
soup = BeautifulSoup(response.content, "html.parser")

print("Status Code:", response.status_code)


#Grab all reports

reports = soup.find_all('a')
links = []
tournament_list = []


#Process reports
for report in reports:
    href = report.get('href')
    if href.startswith("Thread-"):
        title = href[7:]
        title = title.replace("-", " ")
        ending_char = title.find("&action")
        title = title[:ending_char]
        href = "https://worldbeyblade.org/" + href


        test_dupe = href.split("&action")[0]

        if test_dupe not in links:
            #if "&action" in href:
                links.append(href)
                tournament_list.append((title, href))
                print(f"Adding report for: {title} {href}")



#unique links
print("Final Links:")
for tournament in tournament_list:
    try:
        with open(f"{tournament[0]}.txt", "x") as f:
            f.write(f"Report for {tournament[0]}: {tournament[1]}")
    except FileExistsError:
        print("Already exists.")

    response = requests.get(tournament[1])
    soup = BeautifulSoup(response.content, "html.parser")

    print("Status Code:", response.status_code)

    content_div = soup.find('div', class_='post_body')
    if content_div:
         for para in content_div.find_all('span'):
             with open(f"{tournament[0]}.txt", "a") as f:
                 f.write(para.text.strip() + "\n")


