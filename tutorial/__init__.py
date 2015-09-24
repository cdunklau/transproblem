from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.i18n import TranslationStringFactory
from pkg_resources import resource_filename
from pyramid.i18n import get_localizer
from pyramid.threadlocal import get_current_request

import deform.widget

import colander


_ = TranslationStringFactory('transproblem')


class MailingSchema(colander.MappingSchema):
    email = colander.SchemaNode(
        colander.String(),
        validator=colander.Email(),
        title=_('Email Address'),
        widget=deform.widget
    )



def hello_world(request):
    print('Incoming request')
    form = deform.Form(
        MailingSchema(),
        buttons=(deform.Button('submit', _('Register')),),
    )
    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            form.validate(controls)
        except deform.ValidationFailure as e:
            rendered_form = e.render()
        else:
            body = '<body><h1>{0}</h1></body>'.format(
                _('Registration Successful!'))
            return Response(body)
    else:
        rendered_form = form.render()
    body = '<body><h1>{0}</h1>{1}</body>'.format(
        _('Register for our mailing list'), rendered_form)
    return Response(body)


def main(global_config, **settings):
    config = Configurator()
    config.add_route('hello', '/')
    config.add_view(hello_world, route_name='hello')

    config.add_translation_dirs(
        'colander:locale',
        'deform:locale',
        'locale/'
    )

    def translator(term):
        return get_localizer(get_current_request()).translate(term)

    deform_template_dir = resource_filename('deform', 'templates/')
    zpt_renderer = deform.ZPTRendererFactory(
        [deform_template_dir], translator=translator)
    deform.Form.set_default_renderer(zpt_renderer)

    return config.make_wsgi_app()
