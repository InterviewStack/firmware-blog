from django.shortcuts import render, get_object_or_404
import markdown2
from bs4 import BeautifulSoup
import re
from .models import *

def blog_view(request, id):
    # Handle post request here to save to reading list
    blog = get_object_or_404(Blog, id=id)
    body = parse_markdown(blog.body)
    if request.user.is_authenticated:
        userprofile = Userprofile.objects.get(user=request.user)
        context = {
            'blog':blog,
            'body':body,
            'user': userprofile,
        }
    else:
        context = {
            'blog':blog,
            'body':body
        }
    return render(request, "blog/blog.html", context)

# Add a parser for markdown to tailwind
def parse_markdown(markdown_text):
    # Convert Markdown to HTML
    html_content = markdown2.markdown(markdown_text, extras=["fenced-code-blocks", "tables"])
    soup = BeautifulSoup(html_content, 'html.parser')

    # Add DaisyUI classes to various HTML elements
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        tag['class'] = tag.get('class', []) + ['font-bold', 'my-4']
        if tag.name == 'h1':
            tag['class'] += ['text-3xl']
        elif tag.name == 'h2':
            tag['class'] += ['text-2xl']
        elif tag.name == 'h3':
            tag['class'] += ['text-xl']
        elif tag.name == 'h4':
            tag['class'] += ['text-lg']
        elif tag.name == 'h5':
            tag['class'] += ['text-base']
        elif tag.name == 'h6':
            tag['class'] += ['text-sm']

        # Add an ID to the header for anchor links
        if not tag.get('id'):
            # Create an ID from the header text
            header_id = re.sub(r'\W+', '-', tag.get_text(strip=True)).lower()
            tag['id'] = header_id

    for tag in soup.find_all('p'):
        tag['class'] = tag.get('class', []) + ['my-2']

    for tag in soup.find_all('ul'):
        tag['class'] = tag.get('class', []) + ['list-disc', 'ml-5']

    for tag in soup.find_all('ol'):
        tag['class'] = tag.get('class', []) + ['list-decimal', 'ml-5']

    for tag in soup.find_all('code'):
        tag['class'] = tag.get('class', []) + ['px-1']

    for tag in soup.find_all('pre'):
        # Create the mockup-code div
        mockup_code_div = soup.new_tag('div', **{'class': 'mockup-code'})
        
        # Add the DaisyUI classes to the pre tag
        tag['class'] = tag.get('class', []) + ['rounded', 'p-4', 'my-4', 'overflow-auto']
        
        code_tag = tag.find('code')
        if code_tag:
            code_tag.extract()
            tag.append(code_tag)
        tag.wrap(mockup_code_div)

    for tag in soup.find_all('table'):
        tag['class'] = tag.get('class', []) + ['table-auto', 'w-full', 'my-4', 'border-collapse']
        for th in tag.find_all('th'):
            th['class'] = th.get('class', []) + ['border', 'px-4', 'py-2']
        for td in tag.find_all('td'):
            td['class'] = td.get('class', []) + ['border', 'px-4', 'py-2']

    for tag in soup.find_all('a'):
        tag['class'] = tag.get('class', []) + ['hover:text-accent']

    return str(soup)
