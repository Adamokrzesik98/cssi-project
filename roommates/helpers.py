import render

# redirect current page to address
def redirect(self, address):
	data = {'url': address}
	self.response.write('<script> location = "' + address + '"</script>')
