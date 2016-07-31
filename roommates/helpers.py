import render

# redirect current page to address
def redirect(self, address, wait_time):
	data = {'url': address}
	self.response.write('<script> setTimeout(function() {window.location = "' + address + '"},' + str(wait_time) + ');</script>')
