from django.shortcuts import render, get_object_or_404
import markdown2
from bs4 import BeautifulSoup
from .models import *

def blog_view(request, id):
    # Handle post request here to save to reading list
    blog = get_object_or_404(Blog, id=id)
    body = parse_markdown(blog.body)
    context = {
        'blog':blog,
        'body':body
    }
    return render(request, "blog/blog.html", context)

# Add a parser for markdown to tailwind
def parse_markdown(markdown_text):
    html_content = markdown2.markdown(markdown_text, extras=["fenced-code-blocks", "tables"])
    soup = BeautifulSoup(html_content, 'html.parser')

    # Add Tailwind classes to various HTML elements
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        tag['class'] = tag.get('class', []) + ['font-bold', 'my-4', 'text-gray-900', 'dark:text-gray-100']
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

    for tag in soup.find_all('p'):
        tag['class'] = tag.get('class', []) + ['my-2', 'text-gray-800', 'dark:text-gray-200']

    for tag in soup.find_all('ul'):
        tag['class'] = tag.get('class', []) + ['list-disc', 'ml-5', 'text-gray-800', 'dark:text-gray-200']

    for tag in soup.find_all('ol'):
        tag['class'] = tag.get('class', []) + ['list-decimal', 'ml-5', 'text-gray-800', 'dark:text-gray-200']

    for tag in soup.find_all('code'):
        tag['class'] = tag.get('class', []) + ['bg-gray-100', 'rounded', 'p-1', 'text-red-600', 'dark:bg-gray-800', 'dark:text-red-400']

    for tag in soup.find_all('pre'):
        tag['class'] = tag.get('class', []) + ['bg-gray-100', 'rounded', 'p-4', 'my-4', 'overflow-auto', 'dark:bg-gray-800']

    for tag in soup.find_all('table'):
        tag['class'] = tag.get('class', []) + ['table-auto', 'w-full', 'my-4', 'border-collapse', 'text-gray-800', 'dark:text-gray-200']
        for th in tag.find_all('th'):
            th['class'] = th.get('class', []) + ['border', 'px-4', 'py-2', 'bg-gray-200', 'dark:bg-gray-700', 'dark:text-gray-100']
        for td in tag.find_all('td'):
            td['class'] = td.get('class', []) + ['border', 'px-4', 'py-2', 'dark:border-gray-700']

    return str(soup)
