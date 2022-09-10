from bs4 import BeautifulSoup
import requests
import pandas as pd

#url = 'https://www.amazon.com/American-Civil-War-Chess-Set/product-reviews/B08CBG12RZ/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber=1'
#url = 'https://www.amazon.com/Wagners-13008-Deluxe-Wild-10-Pound/product-reviews/B00310210I/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=1'
reviewlist = []

def get_soup(url):
    request = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 2})
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup

def get_reviews(soup):
    reviews = soup.find_all('div', {'data-hook': 'review'})
    # This is not the best option for error check. Fix later
    try:
        for item in reviews:
                review = {
                    'product': soup.title.text.replace('Amazon.com: ', '').strip(),
                    'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
                    'rating': float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
                    'body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
                }
                #print(review)
                reviewlist.append(review)
    except:
        pass

# This is for having pages.
for x in range(1, 999):
    soup = get_soup(f'https://www.amazon.com/Wagners-13008-Deluxe-Wild-10-Pound/product-reviews/B00310210I/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
    print(f'Getting page: {x}')
    get_reviews(soup)
    print(len(reviewlist))
    # If it doesn't see the disabled next page button it goes on, else its out the loop if it does
    if not soup.find('li', {'class': 'a-disabled a-list'}):
        pass
    else:
        break

df = pd.DataFrame(reviewlist)
df.to_excel('BeautifulSoupPractice-ChessSet.xlsx', index=False)
print('Finish')




# Below is test. The .replace will look for the text and replace with whatever you ask.The .stripe at the end just removes the blank spaces
# for item in reviews:
#     title = item.find('a', {'data-hook': 'review-title'}).text.strip()
#     rating = float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip())
#     body = item.find('span', {'data-hook': 'review-body'}).text.strip()
#     print(body)

#print(soup.title.text) # Test to make sure it's working