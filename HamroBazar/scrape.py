from helper import scrape_user, write_to_file
from setting import start_Id, stop_Id, min_post_count


for i in range(start_Id, stop_Id):
    url = "https://hamrobazaar.com/useritems.php?user_siteid=" + str(i)
    name, post_count, mobile_no = scrape_user(url)

    if name and int(post_count) > min_post_count and mobile_no:
        write_to_file(name, post_count, mobile_no, url)
    percent = int(i-start_Id/stop_Id-start_Id)
    print(f'{percent} Percent Done')
