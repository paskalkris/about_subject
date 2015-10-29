from pyramid.view import view_config
from base64 import b64decode
from .storage import RDFStorage

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'about_subject'}


@view_config(route_name='about', renderer='templates/abouttemplate.pt')
def about_view(request):
    g = RDFStorage()
    subjects = g.get_all_subjects()
    g.close_graph()
    return {'subjects_list': subjects}


@view_config(route_name='about_subject', renderer='templates/aboutsbj.pt')
def about_subject_view(request):
    g = RDFStorage()
    subject = request.matchdict['subject']
    return {'rdf': g,
            'subj': b64decode(bytes(subject, 'utf-8')).decode('utf-8')}