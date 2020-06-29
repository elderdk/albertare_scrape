from functions import get_pages, get_property_link, get_property


search_url = "https://search.albertare.com/real-estate/calgary_ab"
page_list = get_pages(search_url)

one_page = page_list[0]

d = get_property_link(one_page)
a = get_property(d[0]) # <- not working
print(a)