from ghost import Ghost
ghost = Ghost()
page, extra_resources = ghost.open("http://www.google.com")
print('\nstatus: {}'.format(page.http_status))
print('\npage: {}'. format(page))
print('\npage.__dir__: {}'. format(page.__dir__))
print('\nextra_resources: {}'. format(extra_resources))
print('\nghost.content: {}'. format(ghost.content))