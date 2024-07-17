
from data_prestructuring import data_preload
from data_prestructuring import data_init
import fitz
from additional_structures.page_rank import PageRank
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"
BLUE = "\033[34m"


def save_as_pdf(results, search_input, show=False):
    filename = 'search_'
    for one in search_input:
        filename += one + "_"
    filename += ".pdf"

    highlight_words = search_input
    doc = fitz.open()

    for page in results[:10]:  # Only take the first 10 results
        content = page['CONTENT']
        pdf_page = doc.new_page(-1, width=595, height=1500)
        p = fitz.Point(50, 70)
        pdf_page.insert_text(p, content, fontname="Times-Roman", fontsize=12, rotate=0)

        if not show:
            for word in highlight_words:
                text_instances = pdf_page.search_for(word)
                for instance in text_instances:
                    highlight = pdf_page.add_highlight_annot(instance)
                    highlight.set_colors(stroke=[1, 0, 0])  # Setting highlight color to red
                    highlight.update()
        else:
            text_instances = pdf_page.search_for(search_input)
            for instance in text_instances:
                pdf_page.add_highlight_annot(instance)

    output_filename = f"{filename}"
    current_directory = os.getcwd()
    output_path = os.path.join(current_directory, output_filename)

    print(f"Current directory: {current_directory}")
    print(f"Saving file to: {output_path}")

    doc.save(output_path, garbage=4, deflate=True, clean=True)
    doc.close()

    print(f"Saved search results to {output_filename}\n")
    print("\033[42mIt might take some time and you must exit the program to load the file!\033[0m")







def display_results(res, term, results_per_page=5):
    def print_page(page, total_pages):
        start_index = page * results_per_page
        end_index = min(start_index + results_per_page, len(res))

        if start_index >= len(res):
            print("\nNO RESULTS FOUND")
            
            return

        if start_index == 0:
            print("DISPLAYING ALL RESULTS" if len(res) <= results_per_page else f"DISPLAYING FIRST {results_per_page} RESULTS: ")
        else:
            print(f"DISPLAYING RESULTS {start_index + 1} to {end_index}:")

        for i in range(start_index, end_index):
            print(f"{BLUE}------------------------------------------------------------{RESET}")
            print(f"{BLUE}------------------------------------------------------------{RESET}")
            print("RESULT NUMBER: ", f"{YELLOW}{i + 1}{RESET} ")
            for single in term:
                print(f"TERM: {BLUE}{single}{RESET}")
                indexes, total = res[i][single]
                print("\n")
                print(f"On {BLUE}page ", res[i]['NUMBER'], f"{RESET} search term occured: ", len(indexes), " times.")
                print('\n')
                content = res[i]['CONTENT']
                j = 1
                for ind in indexes:
                    snippet = f"...{content[max(0, ind - 30):ind].strip()} {RED}{content[ind:ind + len(single)]}{RESET}{content[ind + len(single):ind + len(single) + 30]}..."
                    print(f"{j}. {snippet}")
                    j += 1
                    #printing only 3 sinppets per page due to the terminal size
                    if j > 3:
                        break
                print("\n")

        print(f"\nPage {page + 1} of {total_pages}")

    total_pages = (len(res) + results_per_page - 1) // results_per_page
    current_page = 0

    while True:
        print_page(current_page, total_pages)
        save_as_pdf(res, term)

        if current_page == total_pages - 1:
            print("End of results.")
            break
        
        user_input = input("Enter 'n' for next page, 'p' for previous page, or 'q' to quit: ").strip().lower()
        if user_input == 'n':
            if current_page < total_pages - 1:
                current_page += 1
            else:
                print("You are on the last page.")
        elif user_input == 'p':
            if current_page > 0:
                current_page -= 1
            else:
                print("You are on the first page.")
        elif user_input == 'q':
            break
        else:
            print("Invalid input. Please enter 'n', 'p', or 'q'.")

def autocomplete(page_rank, search_query):
    terms = page_rank.autocomplete(search_query)
    
    print("Suggestions: ")
    j = 1
    for term in terms:
        print( f"{j}.", term)
        j += 1
        if j == 4:
            break

    pick = eval(input("Enter the number of the term to search by: "))
    while pick < 1 or pick > j:
        print("Invalid input. Please enter a number from the list.")
        pick = eval(input("Enter the number of the term to search by: "))
    
    term = terms[pick - 1]
    res, flag = page_rank.sorted_ranks([term])
    
    return res, [term]





if __name__ == "__main__":

    #data_init() ----> starting initialization of the data
    file_path = "./search_results.pdf"

    if os.path.exists(file_path):
        os.remove(file_path)

    graph  = data_preload()
    page_rank = PageRank(graph)
    print("\n--------\nPROGRAM START\n--------\n")
    while(True):

        search_query = input("ENTER THE SEARCH QUERY OR _ for exit (word|words; 'phrase'; using operators NOT, OR, AND; * - for autocomplete): ")
        if search_query == "_":
            break
        elif search_query[-1:] == "*":
            search_query = search_query[:-1]
            print("\nAttempting to autocomplete...")
            res, query = autocomplete(page_rank, search_query)
            display_results(res, query)
            
        elif "AND" in search_query or "OR" in search_query or "NOT" in search_query:
            res, query = page_rank.complex_query(search_query)
            display_results(res, query)
            
        elif search_query[0] == "\"" and search_query[-1] == "\"":
            query = []
            query.append(search_query[1:-1])
            res, flag = page_rank.sorted_ranks(query)
            display_results(res, query)

        else:
            
            query = []
            if len(search_query.split(" ")) > 1:
                for word in search_query.split(" "):
                    query.append(word.strip())
            else:
                query.append(search_query)

            res, flag = page_rank.sorted_ranks(query)
            
            if flag == False:
                query = [res]
                res, flag = page_rank.sorted_ranks(query)
                
            display_results(res, query)

    print("\n--------\nPROGRAM END\n--------\n")
    
    