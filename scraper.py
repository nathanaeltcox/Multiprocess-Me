#!/usr/bin/env python
import requests
from multiprocessing import Process, Queue, current_process
import sys
from bs4 import BeautifulSoup

processes = 4
done_queue = Queue()
process_queue = Queue()
domain_list = []

def response_test(resp):
    result = ""
    if resp.status_code == 200:
        result = "Good"
    else:
        result = str(resp.status_code)
    return result

def add_domain():
    dlist = []
    while True:
        get_domain = input("Input domain: ")
        if get_domain == "exit" or get_domain == "":
            break
        if "http" in get_domain:
            dlist.append(get_domain)
        else:
            get_domain = "https://{}".format(get_domain)
            dlist.append(get_domain)
    return dlist

def web_scraper(process_queue, done_queue):
    done_queue.put("{} starting".format(current_process().name))
    for domain in iter(process_queue.get, "STOP"):
        result = requests.get(domain)
        done_queue.put("{}: Domain {} retrieved with {} bytes".format(current_process().name, domain, len(result.text)))
        outie = BeautifulSoup(result.text, "html.parser")
        links = outie.find_all("link" or "a")
        filename = domain_name_pull(domain)
        outie_file = open("{}.txt".format(filename), "w")
        for link in links:
            outie_file.write(link.get("href") + "\n")
    output_file = open("LogFile.txt", "w")
    for message in iter(done_queue.get, "STOP"):
        output_file.write(message + "\n")

def start_process():
    for i in range(processes):
        proc = Process(target=web_scraper, args=(process_queue, done_queue))
        proc.start()
        proc.terminate()
    
    for domain in domain_list:
        process_queue.put(domain)

#    for message in iter(done_queue.get, "STOP"):
#        print(message)
#    output_file = open("LogFile.txt", "w")
#    for message in iter(done_queue.get, "STOP"):
#        output_file.write(message + "\n")

def stop_process():
#    for domain in domain_list:
#        process_queue.put("STOP")
    for i in range(processes):
        Process.terminate()

def display_log():
    log_file = open("LogFile.txt", "r")
    logs_to_print = []
    for line in log_file:
        logs_to_print.append(line)
    logs_to_see = input("\n""There are {} logs. Which would you like to see? ".format(str(len(logs_to_print))))
    try:
        if logs_to_see.strip().lower() == "all":
            print("\n")
            for item in logs_to_print:
                print(item)
        elif "-" in logs_to_see:
            logs_to_see.split("-")
            start = int(logs_to_see[0]) - 1
            end = int(logs_to_see[2]) - 1
            print("\n")
            while start <= end:
                print(logs_to_print[start])
                start += 1
        else:
            print("\n" + logs_to_print[int(logs_to_see) - 1])
    except:
        print("Invalid input.")

def domain_name_pull(url):
    if "http" in url:
        url = url.split("/")
        domain_item = url[2]
        num = domain_item.count(".")
        domain_item = domain_item.split(".")
        product = domain_item[num - 1]
    else:
        url = url.split("/")
        domain_item = url[0]
        num = domain_item.count(".")
        domain_item = domain_item.split(".")
        product = domain_item[num - 1]
    return product

def DoTheThing():
    page = requests.get("https://nationalgeographic.com")
    soup = BeautifulSoup(page.text, "html.parser")
    links = soup.find_all("link")
    filename = domain_name_pull("https://nationalgeographic.com ")
    
    output_file = open("{}.txt".format(filename), "w")
    for link in links:
        output_file.write(link.get("href") + "\n")

def main():
    while True:
        menu_option = input("\n""Select option:""\n"
                            "\n""0. Do the thing"
                            "\n""1. Add a domain name"
                            "\n""2. Start processing queue"
                            "\n""3. Stop processing queue"
                            "\n""4. Display logs"
                            "\n""5. Exit""\n"
                            "\n""Command: ")
        if menu_option == "1":
            dom_list = add_domain()
            for item in dom_list:
                domain_list.append(item)
            print("Domain added""\n")
            print(domain_list)
        elif menu_option == "0":
            print("Doing the thing")
            DoTheThing()
        elif menu_option == "2":
            print("\n""Starting processes""\n")
            start_process()
        elif menu_option == "3":
            print("\n""Stopping processes""\n")
            stop_process()
        elif menu_option == "4":
            display_log()
        elif menu_option == "5" or menu_option == "exit":
            print("\n""Exiting")
            break
        else:
            print("Invalid command. Try again.")

if __name__ == "__main__":
    main()