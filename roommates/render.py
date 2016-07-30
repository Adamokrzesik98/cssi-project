# Outside Libraries
import jinja2

# Initialize Jinja Environment
env = jinja2.Environment(loader= jinja2.FileSystemLoader('templates'))


# Takes a html template, page title, and data list to render page
# Must pass self in as an argument
def render_page_with_data(self, page_html, page_title, data):
    # Render header
    header_data = {'title': page_title}
    header = env.get_template('header.html')
    self.response.write(header.render(header_data))
    # Render page contents
    page = env.get_template(page_html)
    self.response.write(page.render(data))
    # Render footer
    footer = env.get_template('footer.html')
    self.response.write(footer.render())


# Takes a html template and page title to render page
# Must pass self in as an argument
def render_page(self, page_html, page_title):
    # Render header
    header_data = {'title': page_title}
    header = env.get_template('header.html')
    self.response.write(header.render(header_data))
    # Render page contents
    page = env.get_template(page_html)
    self.response.write(page.render())
    # Render footer
    footer = env.get_template('footer.html')
    self.response.write(footer.render())